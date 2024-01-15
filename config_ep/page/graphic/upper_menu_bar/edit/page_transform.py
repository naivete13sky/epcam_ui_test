import time
from config_ep.base.base import MyGw
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from pywinauto.keyboard import send_keys

class PageTransform(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        self.transform_window = self.graphic_window.child_window(
            **upper_menu_bar.transform_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.transform_window.child_window(title="关闭", control_type="Button").click_input()

    def tansform_features(self,scale:bool, xscale:float, yscale:float):
        if scale:
            self.transform_window.click_input(coords=upper_menu_bar.transform_operation_scale_checkbox_button_coords)
            if xscale:
                self.transform_window.click_input(coords=upper_menu_bar.transform_x_scale_text_coords)
                self.set_value_to_text(xscale)
            if yscale:
                self.transform_window.click_input(coords=upper_menu_bar.transform_y_scale_text_coords)
                self.set_value_to_text(yscale)

    def set_value_to_text(self,text):
        """向文本框中输入值"""
        send_keys("^a")
        send_keys(str(text))

    def click_apply_button(self,time_sleep=0.5):
        self.transform_window.click_input(coords=upper_menu_bar.transform_apply_button_coords)
        time.sleep(time_sleep)

    def click_information_yes_button(self,time_sleep=0.5):
        coords = MyGw.get_information_window_ok_button_coords(upper_menu_bar.information_yes_button_right_bot_coords)
        self.information_window = self.graphic_window.child_window(
            **upper_menu_bar.information_window_para)
        self.information_window.click_input(coords=coords)
        time.sleep(time_sleep)

    def click_information_ok_button(self, time_sleep=0.5):
        coords = MyGw.get_information_window_ok_button_coords(upper_menu_bar.information_ok_button_right_bot_coords)
        self.information_window = self.graphic_window.child_window(
            **upper_menu_bar.information_window_para)
        self.information_window.click_input(coords=coords)
        time.sleep(time_sleep)