import os
import sys
import re
import time
from pathlib import Path

import cv2
from PIL import Image

from pywinauto import mouse
from pywinauto.keyboard import send_keys

from cc.cc_method import get_print_control_identifiers_text, get_coor_of_object, opencv_compare
from config import RunConfig

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 根据你的Tesseract安装路径设置
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

class Engineering(object):
    def __init__(self):
        self.set_default_ui_para()
        self.engineering_window = RunConfig.driver_epcam_ui.window(**self.engineering_window_para)

    def set_default_ui_para(self):
        pass
        # engineering_window
        self.engineering_window_para = {'title': RunConfig.driver_epcam_ui_engineering_title}

        # import job窗口
        self.engineering_import_window_child_window_para = {'title': "Import Job", 'control_type': "Window"}

        # import job窗口，获得选择文件类型控件
        self.engineering_import_input_path_file_type_window_para = {'title': "文件类型(T):", 'auto_id': "1136",
                                                               'control_type': "ComboBox"}

        # 选择文件窗口中的文件路径对象
        self.engineering_import_input_path_file_path_window_para = {'title': "文件名(N):", 'auto_id': "1148",
                                                               'control_type': "ComboBox"}

        # 确认选择中的文件
        self.engineering_import_input_path_confirm_window_para = {'title': "打开(O)", 'auto_id': "1",
                                                             'control_type': "Button"}

        # input job窗口
        self.engineering_input_window_child_window_para = {'title': "Input", 'control_type': "Window"}

        # input 选择文件窗口中的文件路径对象
        self.engineering_input_path_file_path_window_para = {'title': "Open", 'control_type': "Window"}


    # Engineering的方法





    def file_input(self,file_path):
        # 点击菜单File(F)--input
        self.engineering_window.click_input(
            coords=self.get_engineering_file_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(
            coords=self.get_engineering_file_input_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口

        # 切换到input job窗口
        engineering_input_window = RunConfig.driver_epcam_ui.window(**self.engineering_input_window_child_window_para)
        # engineering_input_window.print_control_identifiers()
        engineering_input_window.click_input(
            coords=self.get_engineering_file_input_path_Coor())  # 点击菜单input path

        self.top_window = RunConfig.driver_epcam_ui.window(**self.engineering_input_path_file_path_window_para)
        self.top_window.print_control_identifiers()

        # # 选择文件对象
        # engineering_import_input_path_file_path_window = self.engineering_window.child_window(
        #     **self.engineering_import_input_path_file_path_window_para)
        # engineering_import_input_path_file_path_window.draw_outline(colour='red')  # 绘制边框以突出显示控件（可以自行指定颜色和宽度）
        # engineering_import_input_path_file_path_window.click_input()  # 将焦点设置到控件上
        # send_keys(file_path)  # 输入文本



    # 获得坐标
    def getCoor(self,window,wanted_title):
        win_text = get_print_control_identifiers_text(window)
        coor_ok = get_coor_of_object(wanted_title, win_text)
        return coor_ok

    def get_engineering_left_top_Coor(self):
        win_text2 = get_print_control_identifiers_text(self.engineering_window)
        coor_ok = get_coor_of_object(RunConfig.driver_epcam_ui_engineering_title,win_text2)
        return coor_ok

    def get_engineering_file_Coor(self,coor_type = 'absolute'):
        x = 20
        y = 40
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_file_save_Coor(self,coor_type = 'absolute'):
        x = 20
        y = 250
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_file_import_Coor(self, coor_type ='absolute'):
        x = 20
        y = 210
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_file_import_input_path_Coor(self, coor_type='relative'):
        x = 30
        y = 100  # 变形时，字体太大，异常情况
        y = 80
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_file_import_ok_Coor(self, coor_type='relative'):
        x = 30
        y = 200#变形时，字体太大，异常情况
        y = 180
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_entity_filter_Coor(self,coor_type = 'absolute'):
        x = 120
        y = 120
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_job_first_Coor(self,coor_type = 'absolute'):
        x = 80
        # y = 180
        y = 280
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_go_up_Coor(self,coor_type = 'absolute'):
        x = 80
        y = 250
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_action_Coor(self,coor_type = 'absolute'):
        x = 80
        y = 40
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_action_open_Coor(self,coor_type = 'absolute'):
        x = 80
        y = 90
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_action_select_coor(self,coor_type = 'absolute'):
        x = 80
        y = 70
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_action_select_unselect_all_coor(self,coor_type = 'absolute'):
        x = 280
        y = 95
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_option_Coor(self,coor_type = 'absolute'):
        x = 190
        y = 40
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_option_language_Coor(self,coor_type = 'absolute'):
        x = 190
        y = 60
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_option_EP_Default_Coor(self,coor_type = 'absolute'):
        x = 390
        y = 60
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_option_language_Simplified_Chinese_Coor(self,coor_type = 'absolute'):
        x = 390
        y = 110
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_job_steps_coor(self,coor_type = 'absolute'):
        x = 80 + 260
        y = 250
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x, engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_job_steps_step_first_coor(self,coor_type = 'absolute'):
        x = 80 + 130
        y = 250
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x, engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)


    def get_engineering_file_close_Coor(self,coor_type = 'absolute'):
        x = 20
        y = 275
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)


    def get_engineering_file_input_Coor(self, coor_type ='absolute'):
        x = 20
        y = 160
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_file_input_path_Coor(self, coor_type='relative'):
        x = 30
        y = 55
        if coor_type == 'relative':
            return (x, y)


class Graphic(object):
    pass
    def __init__(self):
        self.set_default_ui_para()
        self.graphic_window = RunConfig.driver_epcam_ui.window(**self.graphic_window_para)
        # self.graphic_window = RunConfig.driver_epcam_ui.top_window()
        # self.graphic_window.print_control_identifiers()

    def set_default_ui_para(self):
        pass
        # engineering_window
        self.graphic_window_para = {'title': RunConfig.driver_epcam_ui_graphic_title,'control_type':"Window"}
        # print('self.graphic_window_para:',self.graphic_window_para)


    def close(self):
        self.graphic_window.child_window(title="关闭", control_type="Button").click_input()