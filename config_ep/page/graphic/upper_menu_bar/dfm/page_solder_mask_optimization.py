import os
import time
import cv2
import pyautogui
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from config_ep.base.base import MyGw
from pywinauto.keyboard import send_keys
from config_ep.base.base import MyMouse

class PageSolderMaskOptimization(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到solder_mask_optimization窗口
        self.solder_mask_optimization = self.graphic_window.child_window(
            **upper_menu_bar.solder_mask_optimization_window)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.solder_mask_optimization.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.solder_mask_optimization.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.solder_mask_optimization.capture_as_image()  # 截图
        save_path = os.path.join(self.temp_path, img_name + '.png')
        drill_correlation_layer_pic.save(save_path)  # 保存到硬盘
        return save_path

    def cut_img(self, img_path, img_name, cut_coords):
        img = cv2.imread(img_path)
        img_cut = img[cut_coords[0]:cut_coords[1], cut_coords[2]:cut_coords[3]]  # 后面的是水平方向
        save_path_cut = os.path.join(self.temp_path, img_name + '_cut.png')
        cv2.imwrite(save_path_cut, img_cut)
        cv2.waitKey(0)
        return save_path_cut

    def is_right(self,save_path_cut, img_standard_str):
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         img_standard_str)
        img_current_path = save_path_cut
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def move_window(self):
        self.solder_mask_optimization.click_input(coords=upper_menu_bar.solder_mask_optimization_move_window_coords)
        time.sleep(0.5)
        MyMouse.mouse_simulator(910, 77)

    def click_layer_button(self):
        self.solder_mask_optimization.click_input(
            coords=upper_menu_bar.solder_mask_optimization_layer_button_coords)

    def select_layer(self,job_info, layer):
        """
        点击solder_mask_optimization窗口的Layer选择
        :param job_info:
        :param layer:
        """
        layer_info = job_info.get('layer_info')
        for layer in layer:
            layer_row = int(layer_info.get(layer.upper())['row'])
            # 切换到Layers Popup子窗口
            self.layer_popup_window = self.graphic_window.child_window(
                **upper_menu_bar.solder_mask_optimization_layer_popup_window)

            coord_x = upper_menu_bar.solder_mask_optimization_layer_popup_first_row_coords[0]

            coord_y = upper_menu_bar.solder_mask_optimization_layer_popup_first_row_coords[1] + \
                      layer_row * upper_menu_bar.solder_mask_optimization_layer_popup_row_spacing_coords
            coords = (coord_x, coord_y)
            self.layer_popup_window.click_input(coords=coords)

    def click_layer_popup_ok_button(self):
        # 切换到Layers Popup子窗口
        self.layer_popup_window = self.graphic_window.child_window(
            **upper_menu_bar.solder_mask_optimization_layer_popup_window)
        self.layer_popup_window.click_input(
            coords=upper_menu_bar.solder_mask_optimization_layer_popup_ok_button_coords)

    def set_clearance_parameter(self, clearance_min, clearance_opt):
        self.set_text(upper_menu_bar.solder_mask_optimization_clearance_min_coords, clearance_min)
        self.set_text(upper_menu_bar.solder_mask_optimization_clearance_opt_coords, clearance_opt)

    def set_coverage_parameter(self, coverage_min, coverage_opt):
        self.set_text(upper_menu_bar.solder_mask_optimization_coverage_min_coords, coverage_min)
        self.set_text(upper_menu_bar.solder_mask_optimization_coverage_opt_coords, coverage_opt)

    def set_bridge_parameter(self, bridge_min, bridge_opt):
        self.set_text(upper_menu_bar.solder_mask_optimization_bridge_min_coords, bridge_min)
        self.set_text(upper_menu_bar.solder_mask_optimization_bridge_opt_coords, bridge_opt)

    def set_text(self, coords, text):
        self.solder_mask_optimization.click_input(coords=coords)
        send_keys('^a')
        send_keys(str(text))

    def click_run_on_features_on_screen_only(self, time_sleep=0.5):
        self.solder_mask_optimization.click_input(
            coords=upper_menu_bar.solder_mask_optimization_run_on_features_on_screen_only_button_coords)
        time.sleep(time_sleep)