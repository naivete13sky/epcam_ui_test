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
        self.set_path(file_path)  # 选择文件对象

    def set_path(self,file_path):
        self.engineering_input_window.click_input(coords=page.engineering_file_input_path_coord)  # 点击菜单input path
        self.engineering_file_input_path_window = RunConfig.driver_epcam_ui.window(
            **page.engineering_file_input_path_window_para)
        self.engineering_file_input_path_window.click_input(coords=page.engineering_file_input_path_file_name_coord)  # 选择文件对象
        send_keys(file_path)  # 输入文本
        send_keys("{ENTER}")  # 这个时候可以鼠标点击gerber文件夹了
        self.engineering_file_input_path_window.click_input(coords=page.engineering_file_input_path_first_folder_coord)  # 点击第一个文件夹
        self.engineering_file_input_path_window.click_input(coords=page.engineering_file_input_path_open_coord)  # 点击open

    def set_new_job_name(self,job_name):
        pass
        self.engineering_input_window.click_input(coords=page.engineering_file_input_job_lineedit_coord)  # 点击job后面的文本框
        send_keys('^a')
        send_keys('*' + job_name)
        send_keys("{ENTER}")  # 在输入框中确认名称完成输入字符
        send_keys("{ENTER}")  # 弹窗确认

    def set_new_step_name(self,step_name):
        pass
        self.engineering_input_window.click_input(coords=page.engineering_file_input_step_lineedit_coord)  # 点击step后面的文本框
        send_keys('^a')
        send_keys('*' + step_name)
        send_keys("{ENTER}")  # 在输入框中确认名称完成输入字符
        send_keys("{ENTER}")  # 弹窗确认
