import os
import time
from pathlib import Path

import cv2
from pywinauto.keyboard import send_keys

from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page


class PageInput(object):
    def __init__(self):
        self.engineering_window = RunConfig.driver_epcam_ui.window(**page.engineering_window_para)
        self.top_window = None
        self.engineering_file_input_path_window = None
        self.engineering_input_file_right_click_menu_window = None
        # 点击菜单File(F)--import
        self.engineering_window.click_input(coords=page.engineering_file_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=page.engineering_file_input_coord)  # 使用鼠标单击按钮，无需主动激活窗口

        # 切换到input job窗口
        self.engineering_input_window = RunConfig.driver_epcam_ui.window(
            **page.engineering_input_window_child_window_para)

    def input_job(self, file_path):
        self.set_path(file_path)  # 选择文件对象

    def set_path(self, file_path):
        self.engineering_input_window.click_input(coords=page.engineering_file_input_path_coord)  # 点击菜单input path
        self.engineering_file_input_path_window = RunConfig.driver_epcam_ui.window(
            **page.engineering_file_input_path_window_para)
        # 选择文件对象
        self.engineering_file_input_path_window.click_input(coords=page.engineering_file_input_path_file_name_coord)
        send_keys(file_path)  # 输入文本
        send_keys("{ENTER}")  # 这个时候可以鼠标点击gerber文件夹了
        # 点击第一个文件夹
        self.engineering_file_input_path_window.click_input(coords=page.engineering_file_input_path_first_folder_coord)
        # 点击open
        self.engineering_file_input_path_window.click_input(coords=page.engineering_file_input_path_open_coord)

    def set_new_job_name(self, job_name):
        pass
        self.engineering_input_window.click_input(coords=page.engineering_file_input_job_lineedit_coord)  # 点击job后面的文本框
        send_keys('^a')
        send_keys('*' + job_name)
        send_keys("{ENTER}")  # 在输入框中确认名称完成输入字符
        send_keys("{ENTER}")  # 弹窗确认

    def set_new_step_name(self, step_name):
        # 点击step后面的文本框
        self.engineering_input_window.click_input(coords=page.engineering_file_input_step_lineedit_coord)
        send_keys('^a')
        send_keys('*' + step_name)
        send_keys("{ENTER}")  # 在输入框中确认名称完成输入字符
        send_keys("{ENTER}")  # 弹窗确认

    def identify(self):
        self.engineering_input_window.click_input(coords=page.engineering_file_input_identify_coord)  # 点击identify

    def translate(self, time_sleep=0.5):
        self.engineering_input_window.click_input(coords=page.engineering_file_input_translate_coord)  # 点击translate
        time.sleep(time_sleep)

    def clear(self):
        self.engineering_input_window.click_input(
            button='right', coords=page.engineering_file_input_file_first_right_coord)
        self.engineering_input_file_right_click_menu_window = RunConfig.driver_epcam_ui.window(
            **page.engineering_file_input_file_right_click_menu_window_para)
        self.engineering_input_file_right_click_menu_window.click_input(
            coords=page.engineering_file_input_file_right_click_menu_clear_coord)

    def is_all_file_cleared(self):
        pass
        # 截图
        engineering_file_input_window_png = self.engineering_input_window.capture_as_image()
        engineering_file_input_window_png.save(r'C:\cc\share\temp\engineering_file_input_window_png.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_input_window_png.png')
        # img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
        img_cut = img[315:335, 20:40]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_input_window_png_cleared.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(
            Path(os.path.dirname(__file__)).parent.parent,
            r'data\pic\engineering\engineering_file_input_window_png_cleared_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_input_window_png_cleared.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def close(self):
        self.engineering_input_window.click_input(coords=page.engineering_file_input_close_coord)  # 点击translate

    def unselect_file(self, index=1):
        coord_x, coord_y = page.engineering_file_input_file_first_select_coord
        self.engineering_input_window.click_input(
            coords=(coord_x, coord_y + page.engineering_file_input_file_row_height * (index - 1)))

    def select_all(self):
        self.engineering_input_window.click_input(
            button='right', coords=page.engineering_file_input_file_first_right_coord)
        self.engineering_input_file_right_click_menu_window = RunConfig.driver_epcam_ui.window(
            **page.engineering_file_input_file_right_click_menu_window_para)
        self.engineering_input_file_right_click_menu_window.click_input(
            coords=page.engineering_file_input_file_right_click_menu_select_all_coord)

    def is_selected_all(self):
        # 截图
        engineering_file_input_window_png = self.engineering_input_window.capture_as_image()
        engineering_file_input_window_png.save(r'C:\cc\share\temp\engineering_file_input_window_png.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_input_window_png.png')
        img_cut = img[315:335, 20:40]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_input_window_png_select_all.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(
            Path(os.path.dirname(__file__)).parent.parent,
            r'data\pic\engineering\engineering_file_input_window_png_select_all_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_input_window_png_select_all.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0