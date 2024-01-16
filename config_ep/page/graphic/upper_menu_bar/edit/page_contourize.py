from pywinauto.keyboard import send_keys

from config import RunConfig
from config_ep import page
from config_ep.base.base import MyGw
from config_ep.page.graphic import upper_menu_bar


class PageContourize(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        self.contourize_window = self.graphic_window.child_window(
            **upper_menu_bar.edit_reshape_contourize_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.contourize_window.child_window(title="关闭", control_type="Button").click_input()

    def run_contourize_ok(self, accuracy, max_size, island='yes', mode=1):
        self.contourize_window.click_input(coords=upper_menu_bar.edit_reshape_contourize_accuracy_input_coord)
        send_keys('^a')
        send_keys(accuracy)
        self.contourize_window.click_input(coords=upper_menu_bar.edit_reshape_contourize_max_size_input_coord)
        send_keys('^a')
        send_keys(max_size)
        if island == 'no':
            self.contourize_window.click_input(coords=upper_menu_bar.edit_reshape_contourize_separate2islands_box_coord)
            self.contourize_window.click_input(coords=upper_menu_bar.edit_reshape_contourize_separate2islands_no_coord)
        if mode == 1:
            self.contourize_window.click_input(coords=upper_menu_bar.edit_reshape_contourize_mode1_coord)
        elif mode == 2:
            self.contourize_window.click_input(coords=upper_menu_bar.edit_reshape_contourize_mode2_coord)
        elif mode == 3:
            self.contourize_window.click_input(coords=upper_menu_bar.edit_reshape_contourize_mode3_coord)
        self.contourize_window.click_input(coords=upper_menu_bar.edit_reshape_contourize_ok_button_coord)

    def information_yes(self):
        self.information_window = RunConfig.driver_epcam_ui.window(**upper_menu_bar.information_window_para)
        self.information_window.click_input(coords=upper_menu_bar.edit_reshape_contourize_information_yes_button_coord)
