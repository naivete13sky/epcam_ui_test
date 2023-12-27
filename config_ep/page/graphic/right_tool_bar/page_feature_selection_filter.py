from config import RunConfig
from config_ep import page
from config_ep.page.graphic import right_tool_bar
from pywinauto.keyboard import send_keys


class PageFeatureSelectionFilter(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        self.feature_selection_filter_window = self.graphic_window.child_window(
            **right_tool_bar.feature_selection_filter_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.feature_selection_filter_window.child_window(title="关闭", control_type="Button").click_input()

    def click_line_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_line_button_coord)

    def click_pad_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_pad_button_coord)

    def click_surface_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_surface_button_coord)

    def click_arc_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_arc_button_coord)

    def click_text_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_text_button_coord)

    def click_positive_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_positive_button_coord)

    def click_negative_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_negative_button_coord)

    def click_reset_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_reset_button_coord)

    def click_select_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_select_button_coord)

    def click_unselect_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_unselect_button_coord)

    def click_high_light_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_high_light_button_coord)

    def click_turn_off_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_turn_off_button_coord)

    def click_close_reset_button(self):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_close_reset_button_coord)

    def include_symbol_input(self, text):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_include_symbol_input_coord)
        send_keys('^a')
        send_keys(text)

    def exclude_symbol_input(self, text):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_exclude_symbol_input_coord)
        send_keys('^a')
        send_keys(text)

    def include_attributes_input(self, text):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_include_attributes_input_coord)
        send_keys('^a')
        send_keys(text)

    def exclude_attributes_input(self, text):
        self.feature_selection_filter_window.click_input(
            coords=right_tool_bar.feature_selection_filter_exclude_attributes_input_coord)
        send_keys('^a')
        send_keys(text)

