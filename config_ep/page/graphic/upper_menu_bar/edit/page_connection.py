from pywinauto.keyboard import send_keys

from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar


class PageConnection(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Create UserSymbol窗口
        self.connection_window = self.graphic_window.child_window(
            **upper_menu_bar.edit_connection_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.connection_window.child_window(title="关闭", control_type="Button").click_input()

    def connection_mode(self, mode, radius=None):
        if mode == 'corner':
            self.connection_window.click_input(coords=upper_menu_bar.edit_connection_corner_coord)
        elif mode == 'round':
            self.connection_window.click_input(coords=upper_menu_bar.edit_connection_round_coord)
            self.connection_window.click_input(coords=upper_menu_bar.edit_connection_round_radius_coord)
            send_keys('^a')
            send_keys(radius)
        self.connection_window.click_input(coords=upper_menu_bar.edit_connection_apply_coord)
