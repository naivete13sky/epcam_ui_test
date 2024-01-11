from config import RunConfig
from config_ep import page
from pywinauto.keyboard import send_keys
from config_ep.base.base import MyGw
from config_ep.page.graphic import upper_menu_bar


class PageStepAndRepeatEditAddStep(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        self.step_and_repeat_edit_add_step_window = self.graphic_window.child_window(
            **upper_menu_bar.step_and_repeat_edit_add_step_window_para)

        self.add_step_steps_popup_window = RunConfig.driver_epcam_ui.window(
            **upper_menu_bar.step_and_repeat_edit_add_step_steps_popup_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.step_and_repeat_edit_add_step_window.child_window(title="关闭", control_type="Button").click_input()

    def click_close_button(self):
        self.step_and_repeat_edit_add_step_window.click_input(
            coords=upper_menu_bar.step_and_repeat_edit_add_step_close_button_coord)

    def click_step_button(self):
        self.step_and_repeat_edit_add_step_window.click_input(
            coords=upper_menu_bar.step_and_repeat_edit_add_step_step_button_coord)

    def click_information_ok_button(self):
        coord = MyGw.get_information_window_ok_button_coords(upper_menu_bar.information_ok_button_right_bot_coords)
        self.information_window = self.step_and_repeat_edit_add_step_window.child_window(
            **upper_menu_bar.information_window_para)
        self.information_window.click_input(coords=coord)

