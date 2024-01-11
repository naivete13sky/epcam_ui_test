import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from config_ep.base.base import MyMouse


class PageNetListAnalyzer(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Netlist Analyzer窗口
        self.netlist_analyzer_window = self.graphic_window.child_window(
            **upper_menu_bar.netlist_analyzer_window_para)

        self.temp_path = RunConfig.temp_path_base

    def capture_image(self, img_name):
        self.netlist_analyzer_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.netlist_analyzer_window.capture_as_image()  # 截图
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
        self.netlist_analyzer_window.child_window(title="关闭", control_type="Button").click_input()

    def click_first_step_button(self):
        """点击第一个step按钮"""
        self.netlist_analyzer_window.click_input(coords=upper_menu_bar.netlist_analyzer_first_step_coords)

    def select_step(self, job_info, step_name):
        """选择step"""

        step_info = job_info.get('step_info')
        step_col = int(step_info.get(step_name.upper())['col'])
        # 切换到Steps Popup子窗口(Steps Popup窗口为主窗口，非子窗口)
        self.steps_pop_window = RunConfig.driver_epcam_ui.window(
            **upper_menu_bar.netlist_analyzer_step_popup_window_para)

        coord_x = upper_menu_bar.netlist_analyzer_step_popup_first_step_coords[0]
        coord_y = upper_menu_bar.netlist_analyzer_step_popup_first_step_coords[1] + (
                step_col - 1) * upper_menu_bar.netlist_analyzer_step_popup_row_coords
        coords = (coord_x, coord_y)
        self.steps_pop_window.double_click_input(coords=coords)


    def click_step_ok_button(self, time_sleep=0.5):
        """点击step popup界面的ok按钮"""

        # 切换到Steps Popup子窗口
        self.steps_pop_window = RunConfig.driver_epcam_ui.window(
            **upper_menu_bar.netlist_analyzer_step_popup_window_para)
        self.steps_pop_window.click_input(coords=upper_menu_bar.netlist_analyzer_step_popup_ok_button_coords)
        time.sleep(time_sleep)

    def click_compare_button(self, time_sleep=0.5):
        """点击compare按钮"""
        self.netlist_analyzer_window.click_input(coords=upper_menu_bar.netlist_analyzer_compare_button_coords)
        time.sleep(time_sleep)

    def click_broken_button(self, time_sleep=0.5):
        """点击broken按钮"""
        self.netlist_analyzer_window.click_input(coords=upper_menu_bar.netlist_analyzer_broken_button_coords)
        time.sleep(time_sleep)

    def select_broken_project(self, time_sleep=0.5):
        """选择broken分析项查看"""
        # 切换到Broken Popup子窗口
        self.broken_popup_window = self.graphic_window.child_window(
            **upper_menu_bar.netlist_analyzer_broken_window_para)
        self.broken_popup_window.click_input(coords=upper_menu_bar.netlist_analyzer_broken_first_project_coords)
        time.sleep(time_sleep)

    def broken_close(self,time_sleep=0.5):
        """点击broken界面的close"""
        self.broken_popup_window = self.graphic_window.child_window(
            **upper_menu_bar.netlist_analyzer_broken_window_para)
        self.broken_popup_window.click_input(coords=upper_menu_bar.netlist_analyzer_broken_close)
        time.sleep(time_sleep)

    def move_window(self):
        self.netlist_analyzer_window.click_input(coords=upper_menu_bar.netlist_analyzer_select_window_coords)
        time.sleep(0.5)
        MyMouse.mouse_simulator(888, 70)



