import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from pywinauto.keyboard import send_keys


class PageConnection(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Create UserSymbol窗口
        self.connection_window = self.graphic_window.child_window(
            **upper_menu_bar.edit_connection_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.connection_window.child_window(title="关闭", control_type="Button").click_input()

    def click_apply_button(self):
        self.connection_window.click_input(coords=upper_menu_bar.edit_connection_apply_coord)
