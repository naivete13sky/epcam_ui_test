import os
import time
import cv2
from config_ep import page
from config import RunConfig
from cc.cc_method import opencv_compare
from pywinauto.keyboard import send_keys

from config_ep.base.base import MyGw
from config_ep.page.graphic import upper_menu_bar


class PageCreate(object):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数
        self.engineering_window = RunConfig.driver_epcam_ui.window(**page.engineering_window_para)

        self.create_window = self.engineering_window.child_window(
            **page.engineering_create_window_para)

        self.create_information_window = self.engineering_window.child_window(
            **page.engineering_create_information_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.create_window.child_window(title="关闭", control_type="Button").click_input()

    def create_window_is_closed(self):
        engineering_file_create_entity_pic = self.engineering_window.capture_as_image()  # 截图
        engineering_file_create_entity_pic.save(r'C:\cc\share\temp\create_window_is_closed_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\create_window_is_closed_pic.png')
        img_cut = img[55:780, 200:810]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\create_window_is_closed_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\create_window_is_closed_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\create_window_is_closed_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def entity_name_input(self, text):
        self.create_window.click_input(coords=page.create_entity_name_input_coord)
        send_keys(text)
        send_keys('{TAB}')  # Tab切走，光标影响截图

    def database_input(self, text):
        self.clear_database_name()
        send_keys(text)

    def clear_entity_name(self):
        self.create_window.click_input(coords=page.create_entity_name_input_coord)
        send_keys('^a')
        send_keys('{BACK}')

    def clear_database_name(self):
        self.create_window.click_input(coords=page.create_database_input_coord)
        send_keys('^a')
        send_keys('{BACK}')

    def database_reset(self):
        self.create_window.click_input(coords=page.create_database_button_coord)

    def create_job(self, job_name, button, job='False'):
        self.clear_entity_name()
        send_keys(job_name)
        if job == 'False':
            if button == 'ok':
                self.create_window.click_input(coords=page.create_ok_button_coord)
                self.create_information_window.click_input(coords=page.create_information_yes_button_coord)
            elif button == 'apply':
                self.create_window.click_input(coords=page.create_apply_button_coord)
                self.create_information_window.click_input(coords=page.create_information_yes_button_coord)
                self.close()
        elif job == 'True':
            if button == 'ok':
                self.create_window.click_input(coords=page.create_ok_button_coord)
                self.click_information_ok_button()
            elif button == 'apply':
                self.create_window.click_input(coords=page.create_apply_button_coord)
                self.click_information_ok_button()
                self.close()

    def click_information_ok_button(self):
        coord = MyGw.get_information_window_ok_button_coords(upper_menu_bar.information_ok_button_right_bot_coords)
        self.information_window = self.create_window.child_window(
            **page.engineering_create_information_window_para)
        self.information_window.click_input(coords=coord)
