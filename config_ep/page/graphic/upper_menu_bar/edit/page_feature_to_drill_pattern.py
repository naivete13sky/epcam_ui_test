from pywinauto.keyboard import send_keys

from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar


class PageFeatureToDrillPattern(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Create UserSymbol窗口
        self.feature2drl_pattern_window = self.graphic_window.child_window(
            **upper_menu_bar.edit_feature2drl_pattern_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.feature2drl_pattern_window.child_window(title="关闭", control_type="Button").click_input()

    def target_layer_input(self, layer_name):
        self.feature2drl_pattern_window.click_input(
            coords=upper_menu_bar.edit_feature2drl_pattern_target_layer_input_coord)
        send_keys('^a')
        send_keys(layer_name)

    def drill_size_input(self, size):
        self.feature2drl_pattern_window.click_input(
            coords=upper_menu_bar.edit_feature2drl_pattern_drill_size_input_coord)
        send_keys('^a')
        send_keys(size)

    def pitch_input(self, size):
        self.feature2drl_pattern_window.click_input(coords=upper_menu_bar.edit_feature2drl_pattern_pitch_input_coord)
        send_keys('^a')
        send_keys(size)

    def click_apply_button(self):
        self.feature2drl_pattern_window.click_input(coords=upper_menu_bar.edit_feature2drl_pattern_apply_button_coord)
