import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar


class PageUndo(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到undo_information窗口
        self.undo_window = self.graphic_window.child_window(
            **upper_menu_bar.edit_undo_information_window_para)

        self.temp_path = RunConfig.temp_path_base

    def capture_image(self, img_name):
        self.undo_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.undo_window.capture_as_image()  # 截图
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
        self.undo_window.child_window(title="关闭", control_type="Button").click_input()

    def click_yes_button(self, time_sleep=0.5):
        """点击undo_information弹窗的yes按钮"""
        self.undo_window.click_input(coords=upper_menu_bar.edit_undo_information_yes_button_coord)
        time.sleep(time_sleep)

    def click_no_button(self, time_sleep=0.5):
        """点击undo_information弹窗的no按钮"""
        self.undo_window.click_input(coords=upper_menu_bar.edit_undo_information_no_button_coord)
        time.sleep(time_sleep)

    def click_no_revocable_button(self, time_sleep=0.5):
        """无撤销操作的弹窗提示，点击no按钮"""

        self.undo_window.click_input(coords=upper_menu_bar.undo_revocable_no_button_coord)



