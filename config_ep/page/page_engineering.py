import os
import time
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from pywinauto import mouse
from pywinauto.keyboard import send_keys
from cc.cc_method import opencv_compare
from config_ep import page
from config import RunConfig
from config_ep.base.base import Base
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 根据你的Tesseract安装路径设置
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'


class PageEngineering(Base):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数
        self.engineering_window = RunConfig.driver_epcam_ui.window(**page.engineering_window_para)

    def job_first_is_opened(self):
        self.engineering_window.set_focus()  # 激活窗口
        # 截图
        engineering_window_jpg = self.engineering_window.capture_as_image()
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window.png')
        # img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
        img_cut = img[225:307, 46:137]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_job_first.png", img_cut)
        cv2.waitKey(0)

        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_job_first_opened_standard.jpg')
        img_current_path = r'C:\cc\share\temp\engineering_job_first.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)

        return rectangle_count == 0

    def close_job_first(self):
        self.engineering_window.click_input(coords=page.engineering_jobList_first_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(button="right", coords=page.engineering_jobList_first_coord)
        self.engineering_window.click_input(
            coords=(page.engineering_jobList_first_coord[0] + 20, page.engineering_jobList_first_coord[1] + 50))
        send_keys("{ENTER}")

    def delete_all_jobs(self):
        # 清空料号，ctrl + A 全选料号，然后 ctrl + B删除
        self.engineering_window.set_focus()  # 激活窗口
        send_keys("^a")  # 发送 Ctrl + A 快捷键，全选
        send_keys("^b")  # 发送 Ctrl + B 快捷键，删除
        send_keys("{ENTER}")  # 发送回车键，删除
        send_keys("{ENTER}")  # 发送回车键，确认删除所有
        time.sleep(1)

    def entity_filter(self, job_name):
        self.engineering_window.click_input(coords=page.engineering_entity_filter_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        send_keys('^a')
        send_keys('*' + job_name)
        send_keys("{ENTER}")

    def open_job_first_by_double_click(self):
        self.engineering_window.click_input(coords=page.engineering_jobList_first_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.double_click_input(coords=page.engineering_jobList_first_coord)

    def open_job_first_by_context_menu(self):
        pass
        self.engineering_window.right_click_input(coords=page.engineering_jobList_first_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        my_engineering_context_menu = RunConfig.driver_epcam_ui.window(class_name="Qt5QWindowPopupDropShadowSaveBits")
        my_engineering_context_menu.click_input(coords=page.engineering_job_right_click_open_coord)  # 点击Open

    def go_up(self, method='click'):
        """
        有2种操作方式：
        1、鼠标：
        2、菜单：
        """
        self.engineering_window.click_input(coords=page.engineering_inJob_go_up_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        if method == 'click':
            self.engineering_window.double_click_input(coords=page.engineering_jobList_first_coord)
        if method == 'menu':
            pass
            # 点击菜单Action--Open
            self.engineering_window.click_input(coords=page.engineering_action_coord)  # 使用鼠标单击按钮，无需主动激活窗口
            self.engineering_window.click_input(coords=page.engineering_action_open_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        mouse.move(coords=page.engineering_jobList_onlyOneJob_empty_coord)

    def language_switch(self, language='english'):
        self.engineering_window.set_focus()  # 激活窗口
        self.engineering_window.click_input(coords=page.engineering_option_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=page.engineering_option_language_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        if language == 'EP Default':
            self.engineering_window.click_input(coords=page.engineering_option_language_EP_Default_coord)
        if language == 'Simplified Chinese':
            self.engineering_window.click_input(coords=page.engineering_option_language_Simplified_Chinese_coord)

    def language_is_simplified_chinese(self):
        send_keys("{ESC}")  # 先按一下ESC键，防止有时因为按过Alt键导致菜单栏有下划线，这个会影响比对结果
        engineering_window_jpg = self.engineering_window.capture_as_image()  # 截图
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window.png')
        img_cut = img[30:55, 10:46]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese_file.png", img_cut)
        # text = pytesseract.image_to_string(img_cut)
        im = Image.open(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese_file.png")
        # 使用Tesseract进行文字识别,使用简体中文语言包
        text_file = pytesseract.image_to_string(im, config=tessdata_dir_config, lang='chi_sim_cc')
        print('text_file:', text_file)

        img_cut = img[30:55, 80:105]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese_file_action.png", img_cut)
        # text = pytesseract.image_to_string(img_cut)
        im = Image.open(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese_file_action.png")
        text_action = pytesseract.image_to_string(im, config=tessdata_dir_config, lang='chi_sim_cc')
        print('text_action:', text_action)

        img_cut = img[30:55, 140:200]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese_file_option.png", img_cut)
        # text = pytesseract.image_to_string(img_cut)
        im = Image.open(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese_file_option.png")
        text_option = pytesseract.image_to_string(im, config=tessdata_dir_config, lang='chi_sim_cc')
        print('text_option:', text_option)

        return ('文件' in text_file) & ('全局' in text_action)
        # return ('文件' in text_file) & ('全局' in text_action) & ('全局设置' in text_option)

    def select_first_job(self):
        self.engineering_window.click_input(coords=page.engineering_jobList_first_coord)

    def file_save(self):
        self.engineering_window.set_focus()  # 激活窗口
        self.engineering_window.click_input(coords=page.engineering_file_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=page.engineering_file_save_coord)  # 使用鼠标单击按钮，无需主动激活窗口

    def action_select_unselect_all(self):
        # self.engineering_window.set_focus()  # 激活窗口
        self.engineering_window.click_input(coords=page.engineering_action_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=page.engineering_action_select_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=page.engineering_action_select_unselect_all_coord)

    def file_close(self):
        self.engineering_window.set_focus()  # 激活窗口
        self.engineering_window.click_input(coords=page.engineering_file_coord)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=page.engineering_file_close_coord)

    def job_first_is_closed(self):
        self.engineering_window.set_focus()  # 激活窗口
        # 截图
        engineering_window_jpg = self.engineering_window.capture_as_image()
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window_job_closed.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window_job_closed.png')
        # img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
        img_cut = img[225:307, 46:140]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_window_job_closed_first.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
            r'engineering\engineering_window_job_closed_first_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_window_job_closed_first.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def job_list_click_empty(self):
        self.engineering_window.click_input(coords=page.engineering_jobList_empty_coord)  # 鼠标点击空白处，不选择料号

    def job_list_in_job_click_empty(self):
        self.engineering_window.click_input(coords=page.engineering_job_list_in_job_empty_coord)  # 鼠标点击空白处，不选择料号

    def open_steps_by_double_click(self):
        self.engineering_window.double_click_input(coords=page.engineering_inJob_steps_coord)  # 双击打开steps

    def open_first_step_by_double_click(self, time_sleep=0.5):
        self.engineering_window.double_click_input(coords=page.engineering_inJob_steps_step_first_coord)
        time.sleep(time_sleep)  # 打开graphic要等一会儿

    def open_fourth_step_by_double_click(self, time_sleep=0.5):
        self.engineering_window.double_click_input(coords=page.engineering_inJob_steps_step_fourth_coord)
        time.sleep(time_sleep)  # 打开graphic要等一会儿

    def open_matrix_by_double_click(self, time_sleep=0.5):
        self.engineering_window.double_click_input(coords=page.engineering_inJob_matrix_coord)
        time.sleep(time_sleep)

    def open_step_by_double_click(self, job_info, step):
        step_info = job_info.get('step_info')
        step_col = int(step_info.get(step.upper())['col']) + 1
        result = step_col / 7
        # 得到step在第几行
        if result % 1 != 0:
            row = int(result) + 1
        else:
            row = int(result)
        col = step_col - int(result) * 7 #得到step在第几列
        print(step, "在第", row, "行的第", col, "列")
        coord_x = page.engineering_jobList_first_coord[0] + (col - 1) * page.engineering_jobList_col_space
        coord_y = page.engineering_jobList_first_coord[1] + (row - 1) * page.engineering_jobList_row_space
        coords = (coord_x,  coord_y)
        self.engineering_window.double_click_input(coords=coords)
        time.sleep(0.5)
