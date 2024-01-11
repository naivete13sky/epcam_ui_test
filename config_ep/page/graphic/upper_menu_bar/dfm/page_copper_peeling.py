import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from pywinauto.keyboard import send_keys
from config_ep.base.base import MyGw


class PageCopperPeeling(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到basic_etch_compensation窗口
        self.copper_peeling_window = self.graphic_window.child_window(
            **upper_menu_bar.dfm_copper_peeling_window_para)

        self.temp_path = RunConfig.temp_path_base

    def capture_image(self, img_name):
        self.copper_peeling_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.copper_peeling_window.capture_as_image()  # 截图
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
        self.copper_peeling_window.child_window(title="关闭", control_type="Button").click_input()

    def click_layer_button(self):
        self.copper_peeling_window.click_input(coords=upper_menu_bar.dfm_copper_peeling_layer_coords)

    def select_layer_name(self, job_info, layer_name):
        """
        点击copper peeling窗口的layer按钮打开Layer Popup窗口
        :param job_info:
        :paramm layer_name:
        """
        layer_info = job_info.get('layer_info')
        for layer in layer_name:
            layer_row = int(layer_info.get(layer.upper())['row'])
            # 切换到Layers Popup子窗口
            self.copper_peeling_layer_window = self.graphic_window.child_window(
                **upper_menu_bar.dfm_copper_peeling_layer_window_para)

            coord_x = upper_menu_bar.dfm_copper_peeling_layer_popup_first_layer_row_coords[0]
            # （分析layer弹窗内多了一个.affect选项，所以不需要减1）
            coord_y = upper_menu_bar.dfm_copper_peeling_layer_popup_first_layer_row_coords[1] + layer_row \
                      * upper_menu_bar.dfm_copper_peeling_layer_popup_row_spacing
            coords = (coord_x, coord_y)
            self.copper_peeling_layer_window.click_input(coords=coords)

    def click_layer_popup_ok_button(self):
        # 切换到Layers Popup子窗口
        self.copper_peeling_layer_window = self.graphic_window.child_window(
            **upper_menu_bar.dfm_copper_peeling_layer_window_para)
        self.copper_peeling_layer_window.click_input(
            coords=upper_menu_bar.dfm_copper_peeling_layer_popup_ok_button_coords)

    def check_fix_bridge_by_line(self):
        """勾选copper_peeling界面的fix bridge by line参数"""
        self.copper_peeling_window.click_input(coords=upper_menu_bar.dfm_copper_peeling_fix_bridge_by_line_coords)


    def set_copper_peeling_text(self,copper_width_max=0, line_to_surface=0, pth_pad_to_surface=0,
    via_pad_to_surface=0, smd_pad_to_surface=0, bga_pad_to_surface=0, laser_via_pad_to_surface=0):
        self.set_text(upper_menu_bar.dfm_copper_peeling_copper_width_max_parameter_coords, copper_width_max)
        self.set_text(upper_menu_bar.dfm_copper_peeling_line_to_surface_coords, line_to_surface)
        self.set_text(upper_menu_bar.dfm_copper_peeling_pth_pad_to_surface_coords, pth_pad_to_surface)
        self.set_text(upper_menu_bar.dfm_copper_peeling_via_pad_to_surface_coords, via_pad_to_surface)
        self.set_text(upper_menu_bar.dfm_copper_peeling_smd_pad_to_surface_coords, smd_pad_to_surface)
        self.set_text(upper_menu_bar.dfm_copper_peeling_bga_pad_to_surface_coords, bga_pad_to_surface)
        self.set_text(upper_menu_bar.dfm_copper_peeling_laser_via_pad_to_surface_coords, laser_via_pad_to_surface)



    def set_text(self,coords,text):
        self.copper_peeling_window.click_input(coords=coords)
        send_keys('^a')
        send_keys(str(text))

    def cilck_run_globally_button(self, time_sleep):
        self.copper_peeling_window.click_input(coords=upper_menu_bar.dfm_copper_peeling_run_globally_coords)
        time.sleep(time_sleep)





