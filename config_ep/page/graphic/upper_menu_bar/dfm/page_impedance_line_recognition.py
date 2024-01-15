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

class PageImpedanceLineRecognition(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Split Layer子窗口
        self.Ipimpedance_line_recognition_window = self.graphic_window.child_window(
            **upper_menu_bar.dfm_cleanup_impedance_line_recognition_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.Ipimpedance_line_recognition_window.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.Ipimpedance_line_recognition_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.Ipimpedance_line_recognition_window.capture_as_image()  # 截图
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

    def click_layer_button(self):
        self.Ipimpedance_line_recognition_window.click_input(
            coords=upper_menu_bar.impedance_line_recognition_click_layer_coords)

    def select_layer(self, job_info, layer_name=None):
        """
        点击pimpedance_line_recognition窗口的Layer选择
        :param job_info:
        :param layer_name:
        """
        layer_info = job_info.get('layer_info')
        for layer in layer_name:
            layer_row = int(layer_info.get(layer.upper())['row'])
            # 切换到Layers Popup子窗口
            self.pimpedance_line_recognition_layer_window = self.graphic_window.child_window(
                **upper_menu_bar.impedance_line_recognition_layer_popup_window_para)

            coord_x = upper_menu_bar.impedance_line_recognition_layer_popup_first_row_coords[0]

            coord_y = upper_menu_bar.impedance_line_recognition_layer_popup_first_row_coords[1] + (
                    layer_row - 1) * upper_menu_bar.impedance_line_recognition_layer_popup_row_spacing
            coords = (coord_x, coord_y)
            self.pimpedance_line_recognition_layer_window.click_input(coords=coords)

    def click_layer_popup_ok_button(self):
        self.pimpedance_line_recognition_layer_window = self.graphic_window.child_window(
            **upper_menu_bar.impedance_line_recognition_layer_popup_window_para)
        self.pimpedance_line_recognition_layer_window.click_input(
            coords=upper_menu_bar.impedance_line_recognition_layer_popup_ok_button_coords
        )

    def click_differential(self):
        """点击differential功能，切换到此功能界面"""
        self.Ipimpedance_line_recognition_window.click_input(
            coords=upper_menu_bar.impedance_line_recognition_click_differential_coords)

    def click_plus_butoon(self):
        """点击 + 按钮"""
        self.Ipimpedance_line_recognition_window.click_input(
            coords=upper_menu_bar.impedance_line_recognition_click_plus_coords
        )

    def input_parameter(self, line_width=0, line_spacing=0):
        """填写line width、line spacing参数值"""
        self.set_text(upper_menu_bar.impedance_line_recognition_line_width_parameter_coords, line_width)
        self.set_text(upper_menu_bar.impedance_line_recognition_line_spacing_parameter_coords, line_spacing)

    def set_text(self, coords, text):
        self.Ipimpedance_line_recognition_window.click_input(coords=coords)
        send_keys('^a')
        send_keys(str(text))

    def click_dropdown(self):
        self.Ipimpedance_line_recognition_window.click_input(
            coords=upper_menu_bar.impedance_line_recognition_reference_layer_dropdown_coords)


    def click_ok_button(self, press = None, time_sleep=2):
        self.Ipimpedance_line_recognition_window.click_input(
            coords=upper_menu_bar.impedance_line_recognition_ok_button_coords
        )

        if press:
            if press == 'f1':
                time.sleep(2)
                pyautogui.press('f1')
                time.sleep(3)
                self.information_window_close()
            else:
                raise ValueError("parameter 'press' must be 'f1'")
        time.sleep(time_sleep)

    # def click_ok_button(self, time_sleep=2):
    #     self.pimpedance_line_recognition_window.click_input(
    #         coords=upper_menu_bar.impedance_line_recognition_ok_button_coords
    #     )
    #     time.sleep(time_sleep)

    def information_window_close(self):
        self.information_window = RunConfig.driver_epcam_ui.window(
            **upper_menu_bar.information_window_para)
        coords = MyGw.get_information_window_ok_button_coords(upper_menu_bar.information_ok_button_right_bot_coords)
        self.information_window.click_input(coords=coords)



