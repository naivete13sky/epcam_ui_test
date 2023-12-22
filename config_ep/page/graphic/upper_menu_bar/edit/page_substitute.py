from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from pywinauto.keyboard import send_keys


class PageSubstitute(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        self.substitute_window = self.graphic_window.child_window(
            **upper_menu_bar.edit_reshape_substitute_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.substitute_window.child_window(title="关闭", control_type="Button").click_input()

    def symbol_input(self, symbol):
        self.substitute_window.click_input(coords=upper_menu_bar.edit_reshape_substitute_symbol_input_coord)
        send_keys(symbol)

    def click_ok_button(self):
        self.substitute_window.click_input(coords=upper_menu_bar.edit_reshape_substitute_ok_button_coord)

    def information_click_ok_button(self):
        self.information_window = self.graphic_window.child_window(
            **upper_menu_bar.edit_reshape_substitute_information_window_para)
        self.information_window.click_input(coords=upper_menu_bar.edit_reshape_substitute_information_ok_button_coord)
