import re
from pathlib import Path
import pyautogui
from config import RunConfig
from config_ep import page
import time
import cv2
import os
from cc.cc_method import opencv_compare
from cc.cc_method import PictureMethod
from config_ep.base.base import Base
from config_ep.base.base import MyMouse


class PageMatrix(Base,MyMouse):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数
        self.matrix_window = RunConfig.driver_epcam_ui.window(**page.matrix_window_pare)
        self.matrix_window_scroll_coord = None
        self.temp_path = RunConfig.temp_path_base

    def cut_img(self, img_name, cut_coords = None):
        self.matrix_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.matrix_window.capture_as_image()  # 截图
        save_path = os.path.join(self.temp_path, img_name + '.png')
        drill_correlation_layer_pic.save(save_path)  # 保存到硬盘
        if cut_coords:
            img = cv2.imread(save_path)
            img_cut = img[cut_coords[0]:cut_coords[1], cut_coords[2]:cut_coords[3]]  # 后面的是水平方向
            save_path_cut = os.path.join(self.temp_path, img_name + '_cut.png')
            cv2.imwrite(save_path_cut, img_cut)
            return save_path_cut
        # cv2.waitKey(0)
        return save_path

    def is_right(self, save_path_cut, img_standard_str):
        # # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         img_standard_str)
        img_current_path = save_path_cut
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def close(self):
        self.matrix_window.child_window(title="关闭", control_type="Button").click_input()  #关闭matrix窗口

    def select_drill_layer(self):
        self.matrix_window.click_input(coords=page.matrix_drill_layer_coord) # 选中drill层

    def select_drill_correlation(self, large_pic_path, small_pic_str, time_sleep = 0.5):
        small_pic_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                     small_pic_str)
        top_left, bottom_right = PictureMethod.get_small_pic_position_from_large_pic(small_pic_path, large_pic_path)
        x = int((top_left[0] + bottom_right[0]) / 2)
        y = int((top_left[1] + bottom_right[1]) / 2)
        print('x,y:', x, y)
        self.matrix_window.click_input(coords=(x,y)) # 选中drill关联线的顶部
        time.sleep(time_sleep)
        return x, y

    def change_drill_cross(self,job_info,layer, start_name, end_name):
        layer_info = job_info.get('layer_info')
        layer_name_row = int(layer_info.get(layer.upper())['row'])
        coords = (110, 200 + (layer_name_row - 1) * 30)
        self.click_layer(coords)

        img_name = 'matrix_window'
        save_path = self.cut_img(img_name)  # 截图

        small_pic_str = r"matrix\drill_top.png"
        x, y = self.select_drill_correlation(save_path, small_pic_str)  # 选中drill关联线的顶部
        start_name_row = int(layer_info.get(start_name.upper())['row'])
        start_coord_y = 200 + (start_name_row - 1) * 30
        MyMouse.mouse_simulator(440 + x, 106 + start_coord_y) # 移动孔带顶部

        small_pic_str = r"matrix\drill_bot.png"
        x, y = self.select_drill_correlation(save_path, small_pic_str)  # 选中drill关联线的底部
        end_name_row = int(layer_info.get(end_name.upper())['row'])
        end_coord_y = 200 + (end_name_row - 1) * 30
        MyMouse.mouse_simulator(440 + x, 106 + end_coord_y) # 移动孔带底部

    def double_click_layer_has_step(self, time_sleep = 0.5):
        self.matrix_window.double_click_input(coords=page.matrix_double_click_layer_has_step_coord) # 双击有step的layer单元格
        time.sleep(time_sleep)

    def double_click_step(self, time_sleep = 0.5):
        self.matrix_window.double_click_input(coords=page.matrix_double_click_step_coord) # 双击step
        time.sleep(time_sleep)

    def click_layer(self,coords, time_sleep = 0.5):
        self.matrix_window.click_input(coords=coords) # 单击layer
        time.sleep(time_sleep)
