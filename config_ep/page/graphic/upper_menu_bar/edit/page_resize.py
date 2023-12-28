from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from pywinauto.keyboard import send_keys


class PageGlobal(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        self.global_window = self.graphic_window.child_window(
            **upper_menu_bar.edit_global_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.global_window.child_window(title="关闭", control_type="Button").click_input()

    def size_input(self, size):
        self.global_window.click_input(coords=upper_menu_bar.edit_global_size_input_coord)
        send_keys('^a')
        send_keys(size)

    def click_ok_button(self):
        self.global_window.click_input(coords=upper_menu_bar.edit_global_ok_button_coord)

    def information_click_yes_button(self):
        self.information_window = RunConfig.driver_epcam_ui.window(
            **upper_menu_bar.edit_global_information_window_para)
        self.information_window.click_input(coords=upper_menu_bar.edit_global_information_yes_button_coord)