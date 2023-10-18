import os
from pathlib import Path

import pywinauto
from py.xml import html
from config import RunConfig
import pytest
from config_g.g_cc_method import G
from pywinauto.application import Application

# 项目目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = BASE_DIR + "/test_report/"


# 定义基本测试环境
@pytest.fixture(scope='function')
def base_url():
    return RunConfig.url


# 设置用例描述表头
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()


# 设置用例描述表格
def pytest_html_results_table_row(report, cells):
    pass
    cells.insert(2, html.td(report.description))
    cells.pop()


# FAILURES_FILE = Path() / "failures.txt"
FAILURES_FILE = Path(os.path.join(BASE_DIR, 'test_report', "failures.txt"))


@pytest.hookimpl()
def pytest_sessionstart():
    print("自定义单独的报告存放位置")
    if FAILURES_FILE.exists():
        FAILURES_FILE.unlink()
    FAILURES_FILE.touch()


# @pytest.mark.hookwrapper
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = description_html(item.function.__doc__)
    extra = getattr(report, 'extra', [])

    # <editor-fold desc="自定义结果存储">
    # if report.when == "call" and report.failed:
    if report.when == "call":
        try:
            with open(str(FAILURES_FILE), "a") as f:
                f.write(str(report.nodeid) + ':' + str(report.outcome) + "\n")
        except Exception as e:
            print("ERROR", e)
            pass
    # </editor-fold>

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            case_path = report.nodeid.replace("::", "_") + ".png"
            if "[" in case_path:
                case_name = case_path.split("-")[0] + "].png"
            else:
                case_name = case_path
            capture_screenshots(case_name)
            img_path = "image/" + case_name.split("/")[-1]
            if img_path:
                html_local = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                             'onclick="window.open(this.src)" align="right"/></div>' % img_path
                extra.append(pytest_html.extras.html(html_local))
        report.extra = extra


def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == '\n':
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]

    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")),
        html.body(
            [html.p(line) for line in desc_lines]))
    return desc_html


def capture_screenshots(case_name):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    :return:
    """

    file_name = case_name.split("/")[-1]
    if RunConfig.NEW_REPORT is None:
        pass
        # raise NameError('没有初始化测试报告目录')
    else:
        image_dir = os.path.join(RunConfig.NEW_REPORT, "image", file_name)
        print(image_dir)
        # RunConfig.driver.save_screenshot(image_dir)


# 加载g
@pytest.fixture(scope='session', autouse=False)
def g():
    """
    全局定义epcam驱动
    :return:
    """

    if RunConfig.driver_type_g == "g":
        driver_g_local = G(RunConfig.gateway_path)  # 拿到G软件

    else:
        raise NameError("driver_g驱动类型定义错误！")

    RunConfig.driver_g = driver_g_local

    return driver_g_local


@pytest.fixture(scope='function', autouse=False)
def prepare_test_job_clean_g():
    # 删除所有料号
    # g = G(RunConfig.gateway_path)
    g = RunConfig.driver_g
    g.clean_g_all_pre_get_job_list(r'//vmware-host/Shared Folders/share/job_list.txt')
    g.clean_g_all_do_clean(r'C:\cc\share\job_list.txt')

    # yield前是前置操作
    yield


# 打开epcam UI
@pytest.fixture(scope='session', autouse=False)
def epcam_ui_start():
    """
    全局定义epcam ui驱动
    :return:
    """

    if RunConfig.driver_type == "epcam_ui":
        try:
            # 先看一下是否已存在EP-CAM主窗口，根据窗口名称判断
            app = Application(backend="uia").connect(title=RunConfig.driver_epcam_ui_engineering_title)
            driver_epcam_ui = app

        except pywinauto.application.AppStartError as e:
            print(e)
            print('\n未获取到EP-CAM程序，新生成EP-CAM程序')
            # 获取.exe文件所在的目录路径
            exe_dir = os.path.dirname(RunConfig.driver_epcam_ui_exe_path)
            # 切换当前工作目录为.exe所在目录,只有在.exe所在目录下才能正常启动EP-CAM
            os.chdir(exe_dir)
            # 使用Application类来启动.exe程序
            app = Application(backend="uia").start(RunConfig.driver_epcam_ui_exe_path)
            driver_epcam_ui = app

    else:
        raise NameError("driver驱动类型定义错误！")
    RunConfig.driver_epcam_ui = app

    # 获取主窗口
    main_window = app.window(title=RunConfig.driver_epcam_ui_engineering_title)
    # 打印窗口的属性
    print("\nWindow Title:", main_window.window_text())

    return driver_epcam_ui



@pytest.fixture(scope='session', autouse=False)
def epcam_ui_import():
    pass


def pytest_configure(config):
    marker_list = [
        'input_output', 'output', 'test', 'cc', 'testcc', 'example', 'input', 'coding'
    ]
    for markers in marker_list:
        config.addinivalue_line('markers', markers)


if __name__ == "__main__":
    capture_screenshots("test_dir/test_baidu_search.test_search_python.png")
