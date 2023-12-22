import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import left_layer_bar
from pywinauto.keyboard import send_keys

class PageMrakNote(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Multi Layer Copy子窗口
        self.mark_note_window = self.graphic_window.child_window(
            **left_layer_bar.right_mark_note_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.mark_note_window.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.mark_note_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.mark_note_window.capture_as_image()  # 截图
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

    def click_move_note_button(self, time_sleep=0.5):
        """点击Mark Note窗口的移动按钮"""
        self.mark_note_window.click_input(coords=left_layer_bar.right_mark_note_move_note_coords)
        time.sleep(time_sleep)

    def click_copy_note_button(self, time_sleep=0.5):
        """点击Mark Note窗口的复制按钮"""
        self.mark_note_window.click_input(coords=left_layer_bar.right_mark_note_copy_note_coords)
        time.sleep(time_sleep)

    def click_add_note_button(self, time_sleep=0.5):
        """点击Mark Note窗口的新增note按钮"""
        self.mark_note_window.click_input(coords=left_layer_bar.right_mark_note_add_new_note_coords)
        time.sleep(time_sleep)

    def click_delete_note_by_mouse_button(self, time_sleep=0.5):
        """点击Mark Note窗口的删除鼠标点击的note"""
        self.mark_note_window.click_input(coords=left_layer_bar.right_mark_note_delete_note_by_mouse_coords)
        time.sleep(time_sleep)


    def click_delete_all_notes_button(self, time_sleep=0.5):
        """
        点击Mark Note窗口的删除所有note标记按钮
        """
        self.mark_note_window.click_input(coords=left_layer_bar.right_mark_note_click_box_note_coords)
        self.mark_note_window.click_input(coords=left_layer_bar.right_mark_note_delete_all_notes_from_the_list_coords)
        time.sleep(time_sleep)

    def click_no_note_information(self):
        """层别无note标记，点击提示框的ok"""
        self.mark_no_note_information_window = self.graphic_window.child_window(
            **left_layer_bar.right_mark_note_no_note_information_window_para)
        self.mark_no_note_information_window.click_input(coords=left_layer_bar.
                                                         right_mark_note_no_note_information_ok_button_coords)

    def click_delete_note_information_ok(self):
        """层别有note标记，点击删除所有note标记提示框的ok"""
        self.mark_delete_note_information_window = self.graphic_window.child_window(
            **left_layer_bar.right_mark_note_delete_note_information_window_para)
        self.mark_delete_note_information_window.click_input(coords=left_layer_bar.
                                                             right_mark_note_delete_note_information_ok_button_coords)


