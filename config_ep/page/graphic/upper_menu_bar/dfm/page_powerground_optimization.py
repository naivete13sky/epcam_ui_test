import os
import time
import cv2
import pyautogui
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from config_ep.base.base import MyGw

class PagePowerGroundOptimization(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Split Layer子窗口
        self.powerground_optimization_window = self.graphic_window.child_window(
            **upper_menu_bar.powerground_optimization_window)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.powerground_optimization_window.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.powerground_optimization_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.powerground_optimization_window.capture_as_image()  # 截图
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

    def click_run_globally_button(self,press:str=None,time_sleep = 2):
        """
        点击Run blobally按钮
        """
        self.powerground_optimization_window.click_input(
            coords=upper_menu_bar.powerground_optimization_run_globally_button_coords)
        if press:
            if press == 'f1':
                time.sleep(1)
                pyautogui.press('f1')
                self.information_window_close()
            else:
                raise ValueError("parameter 'press' must be 'f1'")
        time.sleep(time_sleep)

    def information_window_close(self):
        self.information_window = self.graphic_window.child_window(
            **upper_menu_bar.information_window_para)
        coords = MyGw.get_information_window_ok_button_coords(upper_menu_bar.information_ok_button_right_bot_coords)
        self.information_window.click_input(coords=coords)