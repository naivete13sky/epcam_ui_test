from config import RunConfig
from config_ep import page


class PageGraphic(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)


    def close(self):
        self.graphic_window.child_window(title="关闭", control_type="Button").click_input()