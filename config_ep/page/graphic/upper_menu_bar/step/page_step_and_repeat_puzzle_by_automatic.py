from config import RunConfig
from config_ep import page
from pywinauto.keyboard import send_keys
from config_ep.base.base import MyGw
from config_ep.page.graphic import upper_menu_bar


class PageStepAndRepeatPuzzleByAutomatic(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        self.step_and_repeat_puzzle_by_automatic_window = self.graphic_window.child_window(
            **upper_menu_bar.step_and_repeat_puzzle_by_automatic_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.step_and_repeat_puzzle_by_automatic_window.child_window(title="关闭", control_type="Button").click_input()

    def click_ok_button(self):
        self.step_and_repeat_puzzle_by_automatic_window.click_input(
            coords=upper_menu_bar.step_and_repeat_puzzle_by_automatic_ok_button_coord)

    def step_name_input(self, step_name):
        self.step_and_repeat_puzzle_by_automatic_window.click_input(
            coords=upper_menu_bar.step_and_repeat_puzzle_by_automatic_step_name_input_coord)
        send_keys(step_name)

    def panel_x_min_input(self, x_min):
        self.step_and_repeat_puzzle_by_automatic_window.click_input(
            coords=upper_menu_bar.step_and_repeat_puzzle_by_automatic_panel_x_min_input_coord)
        send_keys('^a')
        send_keys(x_min)

    def panel_y_min_input(self, y_min):
        self.step_and_repeat_puzzle_by_automatic_window.click_input(
            coords=upper_menu_bar.step_and_repeat_puzzle_by_automatic_panel_y_min_input_coord)
        send_keys('^a')
        send_keys(y_min)

    def click_information_ok_button(self):
        coord = MyGw.get_information_window_ok_button_coords(upper_menu_bar.information_ok_button_right_bot_coords)
        self.information_window = self.step_and_repeat_puzzle_by_automatic_window.child_window(
            **upper_menu_bar.information_window_para)
        self.information_window.click_input(coords=coord)
