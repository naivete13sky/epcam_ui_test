import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from pywinauto.keyboard import send_keys


class PageConstructPad(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到construct_pad窗口
        self.construct_pad_window = self.graphic_window.child_window(
            **upper_menu_bar.dfm_construct_pad_window_para)

        self.temp_path = RunConfig.temp_path_base

    def capture_image(self, img_name):
        self.construct_pad_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.construct_pad_window.capture_as_image()  # 截图
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
        self.construct_pad_window.child_window(title="关闭", control_type="Button").click_input()

    def click_run_all_button(self, time_sleep=0.5):
        self.construct_pad_window.click_input(coords=upper_menu_bar.dfm_construct_pad_run_all_coords)
        time.sleep(time_sleep)

    def click_layer_button(self):
        self.construct_pad_window.click_input(coords=upper_menu_bar.dfm_construct_pad_layer_coords)

    def layer_popup_close(self):
        # 切换到layer_popup子窗口
        self.construct_pad_layer_popup_window = self.graphic_window.child_window(
            **upper_menu_bar.construct_pad_layer_popup_window_para)
        self.construct_pad_layer_popup_window.child_window(title="关闭", control_type="Button").click_input()

    def layer_popup_select(self, job_info, layers=None):
        """
        点击construct_pad窗口的layer按钮打开Layer Popup窗口
        :param job_info:
        :paramm layers:
        """
        layer_info = job_info.get('layer_info')
        for layer in layers:
            layer_row = int(layer_info.get(layer.upper())['row'])
            # 切换到Layers Popup子窗口
            self.construct_pad_layer_popup_window = self.graphic_window.child_window(
                **upper_menu_bar.construct_pad_layer_popup_window_para)

            coord_x = upper_menu_bar.construct_pad_layer_popup_first_row_coords[0]
            # （分析layer弹窗内多了一个.affect选项，所以不需要减1）
            coord_y = upper_menu_bar.construct_pad_layer_popup_first_row_coords[1] + layer_row \
                      * upper_menu_bar.construct_pad_layer_popup_row_spacing
            coords = (coord_x, coord_y)
            self.construct_pad_layer_popup_window.click_input(coords=coords)

    def layer_popup_ok(self):
        """
        点击Layer Popup窗口的ok按钮
        """
        self.construct_pad_layer_popup_window.click_input(coords=upper_menu_bar.construct_pad_layer_popup_ok_button_coords)
