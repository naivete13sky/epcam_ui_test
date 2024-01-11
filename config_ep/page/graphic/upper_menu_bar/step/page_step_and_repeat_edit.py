import time
from config import RunConfig
from config_ep import page
from pywinauto.keyboard import send_keys
from config_ep.base.base import MyGw
from config_ep.page.graphic import upper_menu_bar


class PageStepAndRepeatEdit(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        self.step_and_repeat_edit_window = self.graphic_window.child_window(
            **upper_menu_bar.step_and_repeat_edit_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.step_and_repeat_edit_window.child_window(title="关闭", control_type="Button").click_input()

    def gap_input(self, horize_gap, vert_gap):
        self.step_and_repeat_edit_window.click_input(
            coords=upper_menu_bar.step_and_repeat_edit_horize_gap_input_coord)
        send_keys('^a')
        send_keys(horize_gap)
        self.step_and_repeat_edit_window.click_input(
            coords=upper_menu_bar.step_and_repeat_edit_vert_gap_input_coord)
        send_keys('^a')
        send_keys(vert_gap)

    def get_edit_tool_bar_button_coords(self, col_row: list):  # 获取排版编辑按钮坐标
        row = col_row[0]
        col = col_row[1]
        if 1 <= col <= 4 and 1 <= row <= 8:
            coord_x = upper_menu_bar.step_and_repeat_edit_first_button_coord[0] + (
                        col - 1) * upper_menu_bar.step_and_repeat_edit_button_x_spacing
            coord_y = upper_menu_bar.step_and_repeat_edit_first_button_coord[1] + (
                        row - 1) * upper_menu_bar.step_and_repeat_edit_button_y_spacing
            return coord_x, coord_y
        elif 4 <= col <= 1:
            raise ValueError("parameter 'col' must be 1 - 4")
        elif 8 <= row <= 1:
            raise ValueError("parameter 'row' must be 1 - 8")

    def click_add_step_button(self):
        coord = self.get_edit_tool_bar_button_coords(
            upper_menu_bar.step_and_repeat_edit_add_step_button_coord)
        self.step_and_repeat_edit_window.click_input(coords=coord)

    def click_pack_left_and_right_button(self):
        coord = self.get_edit_tool_bar_button_coords(
            upper_menu_bar.step_and_repeat_edit_pack_left_and_right_button_coord)
        self.step_and_repeat_edit_window.click_input(coords=coord)
        time.sleep(0.5)

    def click_pack_top_and_bottom_button(self):
        coord = self.get_edit_tool_bar_button_coords(
            upper_menu_bar.step_and_repeat_edit_pack_top_and_bottom_button_coord)
        self.step_and_repeat_edit_window.click_input(coords=coord)
        time.sleep(0.5)

    def click_pack_to_center_horizontally_button(self):
        coord = self.get_edit_tool_bar_button_coords(
            upper_menu_bar.step_and_repeat_edit_pack_to_center_horizontally_button_coord)
        self.step_and_repeat_edit_window.click_input(coords=coord)
        time.sleep(0.5)
