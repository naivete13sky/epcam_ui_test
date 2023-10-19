from pywinauto.keyboard import send_keys
from config import RunConfig
from config_ep import page


class PageImport(object):
    def __init__(self):
        self.engineering_window = RunConfig.driver_epcam_ui.window(**page.engineering_window_para)
        # 点击菜单File(F)--import
        self.engineering_window.click_input(coords=page.engineering_file_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=page.engineering_file_import_coord)  # 使用鼠标单击按钮，无需主动激活窗口

        # 切换到import job窗口
        self.engineering_import_window = self.engineering_window.child_window(
            **page.engineering_import_window_child_window_para)

    def import_job(self, file_path, job_org_type='odb_tgz'):
        # 点击菜单input path
        self.engineering_import_window.click_input(coords=page.engineering_file_import_input_path_coord)

        if job_org_type == 'ipc2581':
            # 获得选择文件类型控件，并选择ipc2581类型
            engineering_import_input_path_file_type_window = self.engineering_window.child_window(
                **page.engineering_import_input_path_file_type_window_para)
            engineering_import_input_path_file_type_window.select("ipc2581(*.xml *.cvg)")  # 根据文本选择下拉列表项
        else:
            pass

        # 选择文件对象
        engineering_import_input_path_file_path_window = self.engineering_window.child_window(
            **page.engineering_import_input_path_file_path_window_para)
        engineering_import_input_path_file_path_window.draw_outline(colour='red')  # 绘制边框以突出显示控件（可以自行指定颜色和宽度）
        engineering_import_input_path_file_path_window.click_input()  # 将焦点设置到控件上
        send_keys(file_path)  # 输入文本

        # 确认选择中的文件
        engineering_import_input_path_confirm_window = self.engineering_window.child_window(
            **page.engineering_import_input_path_confirm_window_para)
        engineering_import_input_path_confirm_window.click_input()

        # 切换到import job窗口
        engineering_import_window = self.engineering_window.child_window(
            **page.engineering_import_window_child_window_para)
        engineering_import_window.click_input(coords=page.engineering_file_import_ok_coord)
        send_keys("{ENTER}")
