import os
import time
import cv2
from pywinauto.keyboard import send_keys
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import left_layer_bar

class PageSplitLayer(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Split Layer子窗口
        self.split_layer_window = self.graphic_window.child_window(
            **left_layer_bar.split_layer_window_para)

        self.temp_path = RunConfig.temp_path_base
        self.layer = None

    def close(self):
        self.split_layer_window.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.split_layer_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.split_layer_window.capture_as_image()  # 截图
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

    def information_pop_window(self,time_sleep=0.5):
        """
        点击提示框的Ok按钮
        """
        # 切换到MLayers Popup子窗口
        self.information_window = self.graphic_window.child_window(
            **left_layer_bar.information_window_para)
        self.information_window.click_input(coords=left_layer_bar.information_ok_button_coords)
        time.sleep(time_sleep)

    def set_layer(self,layer:str=None):
        """
        输入layer
        :param layer:
        """
        if layer:
            self.layer = layer
            self.split_layer_window.click_input(coords=left_layer_bar.split_layer_text_para)
            send_keys('^a')
            send_keys(layer)

    def click_attribute_button(self,job_info:dict):
        """
        单击Attribute按钮
        :param job_info:
        """
        # self.graphic_window.click_input(coords=(690, 300))
        # img_name = 'split_layer'
        # save_path = self.capture_image(img_name)
        # cut_coords = [44,65,105,250]
        # save_path_cut = self.cut_img(save_path,img_name,cut_coords)
        # text = PictureMethod.get_text_from_img(save_path_cut, 3, 3)
        layer_info = job_info.get("layer_info")
        self.split_layer_window.click_input(coords=left_layer_bar.split_layer_attribute_button_coodrs)
        if self.layer and self.layer.upper() not in layer_info:
            self.information_pop_window()