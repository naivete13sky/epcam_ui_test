from config import RunConfig
from config_ep import page


class PageInput(object):
    def __init__(self):
        self.engineering_window = RunConfig.driver_epcam_ui.window(**page.engineering_window_para)
        self.top_window = None
        # 点击菜单File(F)--import
        self.engineering_window.click_input(coords=page.engineering_file_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=page.engineering_file_input_coord)  # 使用鼠标单击按钮，无需主动激活窗口

        # 切换到input job窗口
        self.engineering_input_window = RunConfig.driver_epcam_ui.window(
            **page.engineering_input_window_child_window_para)

    def input_job(self, file_path):
        self.engineering_input_window.click_input(coords=page.engineering_file_input_path_coord)  # 点击菜单input path
        self.top_window = RunConfig.driver_epcam_ui.window(**page.engineering_input_path_file_path_window_para)
        self.top_window.print_control_identifiers()

        print(file_path)
        # # 选择文件对象
        # engineering_import_input_path_file_path_window = self.engineering_window.child_window(
        #     **self.engineering_import_input_path_file_path_window_para)
        # engineering_import_input_path_file_path_window.draw_outline(colour='red')  # 绘制边框以突出显示控件（可以自行指定颜色和宽度）
        # engineering_import_input_path_file_path_window.click_input()  # 将焦点设置到控件上
        # send_keys(file_path)  # 输入文本
