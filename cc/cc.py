import os


def f1():
    pass
    from pywinauto.application import Application

    # 定义.exe程序的路径
    exe_path = r"C:\cc\ep_local\product\EP-CAM\version\20230717\EPCAM_1.1.7.2_release_r12827_jiami_3\Release\EP-CAM.exe"

    # 获取.exe文件所在的目录路径
    exe_dir = os.path.dirname(exe_path)

    # 切换当前工作目录为.exe所在目录
    os.chdir(exe_dir)

    # 使用Application类来启动.exe程序
    app = Application(backend="uia").start(exe_path)

    # 使用窗口标题来连接到应用程序的主窗口
    main_window = app.window(title="Engineering 1.1.7.2")

    # 可以通过main_window来执行其他操作，如点击按钮、输入文本等
    main_window.print_control_identifiers()

    # 等待一段时间或执行其他操作

def f2():
    pass
    import os

    exe_path = r"C:\cc\ep_local\product\EP-CAM\version\20230717\EPCAM_1.1.7.2_release_r12827_jiami_3\Release\EP-CAM.exe"

    # 获取.exe文件所在的目录路径
    exe_dir = os.path.dirname(exe_path)

    # 切换当前工作目录为.exe所在目录
    os.chdir(exe_dir)


    # 使用os.system启动应用程序
    os.system(exe_path)


if __name__ == '__main__':
    pass
    f1()

