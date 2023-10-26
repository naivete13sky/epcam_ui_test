from pywinauto.keyboard import send_keys

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
        self.engineering_file_input_path_window = RunConfig.driver_epcam_ui.window(**page.engineering_file_input_path_window_para)
        # self.engineering_file_input_path_window.print_control_identifiers()
        self.set_path(file_path)  # 选择文件对象

    def set_path(self,file_path):
        self.engineering_file_input_path_window.click_input(coords=(100, 395))  # 选择文件对象
        send_keys(file_path)  # 输入文本
        send_keys("{ENTER}")  # 这个时候可以鼠标点击gerber文件夹了
        self.engineering_file_input_path_window.click_input(coords=(170, 100))  # 点击第一个文件夹
        self.engineering_file_input_path_window.click_input(coords=(600, 400))  # 点击open
