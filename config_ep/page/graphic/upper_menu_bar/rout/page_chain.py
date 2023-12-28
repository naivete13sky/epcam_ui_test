import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from pywinauto.keyboard import send_keys

class PageChain(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Chain子窗口
        self.chain_window = self.graphic_window.child_window(
            **upper_menu_bar.chain_window_para)

        self.temp_path = RunConfig.temp_path_base

    def capture_image(self, img_name):
        self.chain_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.chain_window.capture_as_image()  # 截图
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
        self.chain_window.child_window(title="关闭", control_type="Button").click_input()

    def set_rout_layer(self,rout_layer:str):
        """
        输入rout layer
        :param rout_layer:
        """
        self.chain_window.click_input(coords=upper_menu_bar.chain_layer_text_coords)
        send_keys('^a')
        send_keys(rout_layer)

    def set_tool_size(self, tool_size:float):
        """
        输入tool size
        """
        self.chain_window.click_input(coords=upper_menu_bar.chain_tool_size_text_coords)
        send_keys('^a')
        send_keys(str(tool_size))

    def create_chain(self,rout_layer:str,tool_size:float):
        """
        创建捞
        :param rout_layer:
        :param tool_size
        """
        self.set_rout_layer(rout_layer)
        self.set_tool_size(tool_size)
        self.chain_window.click_input(coords=upper_menu_bar.chain_ok_button_coords)
        self.chain_dialog_box_window = self.graphic_window.child_window(**upper_menu_bar.chain_dialog_box_window_para)
        self.chain_dialog_box_window.click_input(coords=upper_menu_bar.chain_dialog_box_yes_button_coords)

    def get_chain_menu_bar_coords(self, coords):
        x = upper_menu_bar.chain_button_menu_first_button_coord[0]
        y = upper_menu_bar.chain_button_menu_first_button_coord[1]
        x_spacing = upper_menu_bar.chain_button_menu_spacing
        x = x + x_spacing * (coords - 1)
        coord = (x, y)
        return coord

    def set_compensation(self, para):
        if para == 'Right':
            self.chain_window.click_input(coords=upper_menu_bar.chain_create_chain_compensation_coord)
            self.chain_window.click_input(coords=upper_menu_bar.chain_create_chain_compensation_right_coord)
        elif para == 'Left':
            self.chain_window.click_input(coords=upper_menu_bar.chain_create_chain_compensation_coord)
            self.chain_window.click_input(coords=upper_menu_bar.chain_create_chain_compensation_left_coord)

    def click_set_plunge_button(self):
        coord = self.get_chain_menu_bar_coords(coords=upper_menu_bar.chain_set_plunge_button_coord)
        self.chain_window.click_input(coords=coord)

    def click_set_plunge_type_open(self):
        self.chain_window.click_input(coords=upper_menu_bar.chain_set_plunge_type_open_coord)

    def click_ok_button(self):
        self.chain_window.click_input(coords=upper_menu_bar.chain_ok_button_coords)
