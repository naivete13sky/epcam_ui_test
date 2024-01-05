import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import left_layer_bar
from pywinauto.keyboard import send_keys


class PageFeatureHistogram(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        self.feature_histogram_window = self.graphic_window.child_window(
            **left_layer_bar.features_histogram_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.feature_histogram_window.child_window(title="关闭", control_type="Button").click_input()
