import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from pywinauto.keyboard import send_keys


class PageBasicEtchCompensation(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到basic_etch_compensation窗口
        self.basic_etch_compensation_window = self.graphic_window.child_window(
            **upper_menu_bar.basic_etch_compensation_window_para)

        self.temp_path = RunConfig.temp_path_base

    def capture_image(self, img_name):
        self.basic_etch_compensation_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.basic_etch_compensation_window.capture_as_image()  # 截图
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

    def is_right(self, save_path_cut, img_standard_str):
        """
        验证两张图片是否一致
        :param save_path_cut:
        :param img_standard_str:
        :return:
        """
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         img_standard_str)
        img_current_path = save_path_cut
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def close(self):
        self.basic_etch_compensation_window.child_window(title="关闭", control_type="Button").click_input()

    def click_layer_button(self):

        self.basic_etch_compensation_window.click_input(coords=upper_menu_bar.basic_etch_compensation_layer_coord)

    def layer_popup_close(self):
        # 切换到layer_popup子窗口
        self.basic_etch_compensation_layer_popup_window = self.graphic_window.child_window(
            **upper_menu_bar.basic_etch_compensation_layer_popup_window_para)
        self.basic_etch_compensation_layer_popup_window.child_window(title="关闭", control_type="Button").click_input()

    def layer_popup_select(self, job_info, layers=None):
        """
        点击basic_etch_compensation窗口的layer按钮打开Layer Popup窗口
        :param job_info:
        :paramm layers:
        """
        layer_info = job_info.get('layer_info')
        for layer in layers:
            layer_row = int(layer_info.get(layer.upper())['row'])
            # 切换到Layers Popup子窗口
            self.basic_etch_compensation_layer_popup_window = self.graphic_window.child_window(
                **upper_menu_bar.basic_etch_compensation_layer_popup_window_para)

            coord_x = upper_menu_bar.basic_etch_compensation_layer_popup_first_row_coords[0]
            # （分析layer弹窗内多了一个.affect选项，所以不需要减1）
            coord_y = upper_menu_bar.basic_etch_compensation_layer_popup_first_row_coords[1] +layer_row \
                      * upper_menu_bar.basic_etch_compensation_layer_popup_row_spacing
            coords = (coord_x, coord_y)
            self.basic_etch_compensation_layer_popup_window.click_input(coords=coords)

    def click_layer_ok_button(self):
        # 切换到Layers Popup子窗口
        self.basic_etch_compensation_layer_popup_window = self.graphic_window.child_window(
            **upper_menu_bar.basic_etch_compensation_layer_popup_window_para)
        self.basic_etch_compensation_layer_popup_window.click_input(coords=
            upper_menu_bar.basic_etch_compensation_layer_popup_ok_button_coords)


    def line_arc_parameter(self, parameter):
        """填写line_arc的参数"""
        self.basic_etch_compensation_window.click_input(coords=
            upper_menu_bar.basic_etch_compensation_line_arc_parameter_coords)
        send_keys('^a')
        send_keys(parameter)

    def pad_parameter(self, parameter):
        """填写pad的参数"""
        self.basic_etch_compensation_window.click_input(coords=
            upper_menu_bar.basic_etch_compensation_pad_parameter_coords)
        send_keys('^a')
        send_keys(parameter)

    def surface_parameter(self, parameter):
        """填写surface的参数"""
        self.basic_etch_compensation_window.click_input(coords=
            upper_menu_bar.basic_etch_compensation_surface_parameter_coords)
        send_keys('^a')
        send_keys(parameter)


    def min_spacing_parameter(self, parameter):
        """填写min_spacing的参数"""
        self.basic_etch_compensation_window.click_input(coords=
            upper_menu_bar.basic_etch_compensation_min_spacing_coords)
        send_keys('^a')
        send_keys(parameter)

    def click_run_globally(self, time_sleep):
        """点击run globally执行按钮"""
        self.basic_etch_compensation_window.click_input(coords=
            upper_menu_bar.basic_etch_compensation_run_globally_coords)
        time.sleep(time_sleep)



