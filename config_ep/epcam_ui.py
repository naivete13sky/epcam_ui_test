import os
import sys
import re
import time
from pathlib import Path

import cv2
from pywinauto import mouse
from pywinauto.keyboard import send_keys

from cc.cc_method import get_print_control_identifiers_text, get_coor_of_object, opencv_compare
from config import RunConfig




class Engineering(object):
    def __init__(self):
        self.set_default_ui_para()
        self.engineering_window = RunConfig.driver_epcam_ui.window(**self.engineering_window_para)


    def set_default_ui_para(self):
        pass
        # engineering_window
        self.engineering_window_para = {'title': "Engineering 1.1.7.2"}

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




    # Engineering的方法
    def job_first_is_opened(self):
        pass

        # 截图
        engineering_window_jpg = self.engineering_window.capture_as_image()
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
        img_cut = img[225:307, 46:137]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_job_first.jpg", img_cut)
        cv2.waitKey(0)

        # 加载两张图片
        img_standard_path = os.path.join(Path(os.path.dirname(__file__)).parent, r'data\pic\engineering\engineering_job_first_opened_standard.jpg')
        img_current_path = r'C:\cc\share\temp\engineering_job_first.jpg'
        rectangle_count = opencv_compare(img_standard_path,img_current_path)

        return rectangle_count == 0

    def close_job_first(self):
        self.engineering_window.click_input(
            coords=self.get_engineering_job_first_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(button="right", coords=(80,280))
        self.engineering_window.click_input(coords=(80 + 20,280 + 50))
        send_keys("{ENTER}")

    def delete_all_jobs(self):
        # 清空料号，ctrl + A 全选料号，然后 ctrl + B删除
        self.engineering_window.set_focus()  # 激活窗口
        send_keys("^a")  # 发送 Ctrl + A 快捷键，全选
        send_keys("^b")  # 发送 Ctrl + B 快捷键，删除
        send_keys("{ENTER}")  # 发送回车键，删除
        send_keys("{ENTER}")  # 发送回车键，确认删除所有
        time.sleep(1)

    def import_ipc2581(self,file_path):
        #点击菜单File(F)--import
        self.engineering_window.click_input(coords=self.get_engineering_file_Coor(coor_type='relative'))# 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=self.get_engineering_file_import_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口

        # 切换到import job窗口，并点击菜单input path
        engineering_import_window = self.engineering_window.child_window(**self.engineering_import_window_child_window_para)
        engineering_import_window.click_input(coords=self.get_engineering_file_import_input_path_Coor())# 点击菜单input path





        # 获得选择文件类型控件，并选择ipc2581类型
        engineering_import_input_path_file_type_window=self.engineering_window.child_window(**self.engineering_import_input_path_file_type_window_para)
        engineering_import_input_path_file_type_window.select("ipc2581(*.xml *.cvg)")#根据文本选择下拉列表项

        # 选择文件对象
        engineering_import_input_path_file_path_window=self.engineering_window.child_window(**self.engineering_import_input_path_file_path_window_para)
        engineering_import_input_path_file_path_window.draw_outline(colour = 'red')# 绘制边框以突出显示控件（可以自行指定颜色和宽度）
        engineering_import_input_path_file_path_window.click_input()  # 将焦点设置到控件上
        send_keys(file_path)  # 输入文本

        # 确认选择中的文件
        engineering_import_input_path_confirm_window=self.engineering_window.child_window(**self.engineering_import_input_path_confirm_window_para)
        engineering_import_input_path_confirm_window.click_input()

        # 切换到import job窗口
        engineering_import_window = self.engineering_window.child_window(**self.engineering_import_window_child_window_para)
        engineering_import_window.click_input(coords=self.get_engineering_file_import_ok_Coor())
        send_keys("{ENTER}")

    def entity_filter(self,job_name):
        pass
        self.engineering_window.click_input(
            coords=self.get_engineering_entity_filter_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        send_keys('^a')
        send_keys('*' + job_name)
        send_keys("{ENTER}")

    def open_job_first_by_double_click(self):
        pass
        # self.engineering_window.set_focus()  # 激活窗口
        self.engineering_window.click_input(
            coords=self.get_engineering_job_first_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.double_click_input(coords=(80, 280))

    def go_up(self,method='click'):
        '''
        有2种操作方式：
        1、鼠标：
        2、菜单：
        '''
        self.engineering_window.click_input(
            coords=self.get_engineering_go_up_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        if method == 'click':
            self.engineering_window.double_click_input(coords=(80, 280))
        if method == 'menu':
            pass
            # 点击菜单Action--Open
            self.engineering_window.click_input(
                coords=self.get_engineering_action_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
            self.engineering_window.click_input(
                coords=self.get_engineering_action_open_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        mouse.move(coords=(600,600))

    def language_switch(self,language = 'english'):
        self.engineering_window.set_focus()  # 激活窗口
        self.engineering_window.click_input(
            coords=self.get_engineering_option_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(
            coords=self.get_engineering_option_language_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        if language == 'EP Default':
            pass
            self.engineering_window.click_input(
                coords=self.get_engineering_option_EP_Default_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        if language == 'Simplified Chinese':
            pass
            self.engineering_window.click_input(
                coords=self.get_engineering_option_language_Simplified_Chinese_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口

    def language_is_Simplified_Chinese(self):
        send_keys("{ESC}")  # 先按一下ESC键，防止有时因为按过Alt键导致菜单栏有下划线，这个会影响比对结果
        engineering_window_jpg = self.engineering_window.capture_as_image()# 截图
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img_cut = img[30:60, 10:250]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu.jpg", img_cut)
        cv2.waitKey(0)

        # 加载两张图片
        img_standard_path = os.path.join(Path(os.path.dirname(__file__)).parent, r'data\pic\engineering\engineering_menu_language_Simplified_Chinese_standard.jpg')
        img_current_path = r'C:\cc\share\temp\engineering_menu.jpg'
        rectangle_count = opencv_compare(img_standard_path,img_current_path)

        return rectangle_count == 0

    def file_save(self):
        self.engineering_window.set_focus()  # 激活窗口
        self.engineering_window.click_input(
            coords=self.get_engineering_file_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口

        self.engineering_window.click_input(
            coords=self.get_engineering_file_save_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口



    # 获得坐标

    def getCoor(self,window,wanted_title):
        win_text = get_print_control_identifiers_text(window)
        coor_ok = get_coor_of_object(wanted_title, win_text)
        return coor_ok

    def get_engineering_left_top_Coor(self):
        win_text2 = get_print_control_identifiers_text(self.engineering_window)
        coor_ok = get_coor_of_object('Engineering 1.1.7.2',win_text2)
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
        y = 180
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