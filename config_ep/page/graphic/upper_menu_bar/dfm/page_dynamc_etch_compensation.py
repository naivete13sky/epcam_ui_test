import os
import time
import cv2
from pywinauto.keyboard import send_keys
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import upper_menu_bar
from config_ep.base.base import MyODB


class PageDynamicEtchCompensation(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Split Layer子窗口
        self.dynamic_etch_compensation_window = self.graphic_window.child_window(
            **upper_menu_bar.dynamic_etch_compensation_window_para)

        self.dynamc_compensate_range_window = self.graphic_window.child_window(
            **upper_menu_bar.dynamic_etch_compensation_dynamc_compensate_range_window_para)

        self.add_window = self.graphic_window.child_window(**upper_menu_bar.add_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.dynamic_etch_compensation_window.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.dynamic_etch_compensation_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.dynamic_etch_compensation_window.capture_as_image()  # 截图
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

    def click_compensation_functions_button(self,col:int,row:int):
        # img_name  = "dynamic_etch_compensation_window"
        # self.capture_image(img_name)

        if 1 <= col <= 4 and 1 <= row <= 5:
            coord_x,coord_y = upper_menu_bar.dynamic_etch_compensation_compensation_functions_first_button_coords
            x_spacing = upper_menu_bar.dynamic_etch_compensation_compensation_functions_x_spacing
            y_spacing = upper_menu_bar.dynamic_etch_compensation_compensation_functions_y_spacing
            coord_x = coord_x + (col - 1) * x_spacing
            coord_y = coord_y + (row - 1) * y_spacing
            self.dynamic_etch_compensation_window.click_input(coords=(coord_x,coord_y))
        elif not (1 <= col <= 4):
            raise ValueError("parameter 'col' must be 1 - 4")
        elif not (1 <= row <= 5):
            raise ValueError("parameter 'row' must be 1 - 5")

    def save_as_json(self,json_name:str="newERF",col:int=1,row:int=1):
        """
        save as一个json
        """
        ranges = MyODB.get_dynamic_compensate_ranges()
        self.click_compensation_functions_button(col,row)

        self.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_save_as_button_coords)
        self.save_as_window = self.graphic_window.child_window(
            **upper_menu_bar.save_as_window)
        self.save_as_window.click_input(coords=upper_menu_bar.erf_name_text_coords)
        send_keys('^a')
        send_keys(json_name)
        self.save_as_window.click_input(coords=upper_menu_bar.erf_name_ok_button_coords)
        if json_name + '.json' in ranges:
            information_window =  self.graphic_window.child_window(
            **upper_menu_bar.information_window_para)
            information_window.click_input(coords=upper_menu_bar.information_ok_button_coords)
        self.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_ok_button_coords)

    def add_new_json(self, json_name):
        self.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_add_button_coords)
        self.add_window.click_input(coords=upper_menu_bar.erf_name_text_coords)
        send_keys('^a')
        send_keys(json_name)
        self.add_window.click_input(coords=upper_menu_bar.erf_name_ok_button_coords)

    def delete_json(self,json_name:str,col:int=1,row:int=1):
        """
        delete一个json
        """
        self.click_compensation_functions_button(col, row)
        ranges = MyODB.get_dynamic_compensate_ranges()
        json_name = json_name + '.json'
        if json_name in ranges:
            json_index = int(ranges.get(json_name)['index'])
            coord_x,coord_y = upper_menu_bar.dynamic_compensate_range_first_json_coords
            spacing = upper_menu_bar.dynamic_compensate_range_json_spacing
            self.dynamc_compensate_range_window.click_input(coords=(coord_x,coord_y+json_index*spacing))
            self.dynamc_compensate_range_window.click_input(
                coords=upper_menu_bar.dynamic_compensate_range_delete_button_coords)
            self.warning_window = self.graphic_window.child_window(
                **upper_menu_bar.warning_window_para)
            self.warning_window.click_input(coords=upper_menu_bar.warning_yes_button)
            self.dynamc_compensate_range_window.click_input(
                coords=upper_menu_bar.dynamic_compensate_range_ok_button_coords)

    def get_all_json_input_coords(self, col=4, row=5):
        x1 = upper_menu_bar.dynamic_etch_compensation_pad_pad_input_coord[0]
        y1 = upper_menu_bar.dynamic_etch_compensation_pad_pad_input_coord[1]
        row_spacing = upper_menu_bar.dynamic_etch_compensation_compensation_functions_x_spacing
        col_spacing = upper_menu_bar.dynamic_etch_compensation_compensation_functions_y_spacing
        coords = []
        for i in range(1, col + 1):
            for j in range(1, row + 1):
                x = x1 + (i - 1) * row_spacing
                y = y1 + (j - 1) * col_spacing
                coords.append((x, y))
        return coords

    def run_on_selected_features_yes(self):
        self.dynamic_etch_compensation_window.click_input(
            coords=upper_menu_bar.dynamic_etch_compensation_run_on_selected_features_yes_coord)

    def run_operation(self, mode, time_sleep=8):
        if mode == 1:  # run on all feature
            self.dynamic_etch_compensation_window.click_input(
                coords=upper_menu_bar.dynamic_etch_compensation_run_globally_button_coord)
        elif mode == 2:  # run on feature on screen
            self.dynamic_etch_compensation_window.click_input(
                coords=upper_menu_bar.dynamic_etch_compensation_run_on_features_on_screen_only_button_coord)
        elif mode == 3:  # run on feature on inside profile
            self.dynamic_etch_compensation_window.click_input(
                coords=upper_menu_bar.dynamic_etch_compensation_run_on_features_inside_profile_button_coord)
        time.sleep(time_sleep)
