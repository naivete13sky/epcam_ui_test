from config import RunConfig
from config_ep import page
import time
import cv2
import os
from cc.cc_method import opencv_compare


class PageGraphic(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)
        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.graphic_window.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.graphic_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.graphic_window.capture_as_image()  # 截图
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
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         img_standard_str)
        img_current_path = save_path_cut
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def open_copper_exposed_area_dindow(self):
        """
        打开Copper/Exposed Area 窗口
        """
        self.graphic_left_layer_bar_right_click_menu_window = RunConfig.driver_epcam_ui.window(
            **page.graphic_left_layer_bar_right_click_menu_window_para)
        self.graphic_left_layer_bar_right_click_menu_window.click_input(
            coords=page.graphic_left_layer_bar_right_click_menu_copper_exposed_area_coords)

    def open_measurement_mark_window(self):
        """
        打开Measurement Mark窗口
        """
        self.graphic_canvas_right_click_menu_window = RunConfig.driver_epcam_ui.window(
            **page.graphic_left_layer_bar_right_click_menu_window_para)
        self.graphic_canvas_right_click_menu_window.click_input(
            coords=page.graphic_canvas_right_click_menu_measure_coords)

    def click_layer(self,job_info,layer,time_sleep=0.5):
        """
        单击层别
        :param job_info:
        :param layer:
        """
        layer_info = job_info.get('layer_info')
        layer_row = int(layer_info.get(layer.upper())['row'])
        coord_x, coord_y = page.graphic_left_layer_bar_first_row_coord
        row_height = page.engineering_file_input_file_row_height
        coord_y = coord_y + (layer_row - 1) * row_height
        layer_coord = (coord_x, coord_y)
        self.graphic_window.click_input(coords=layer_coord) # 左击layer
        time.sleep(time_sleep)

    def right_click_layer(self,job_info,layer,time_sleep=0.5):
        """
        右击层别
        :param job_info:
        :param layer:
        """
        layer_info = job_info.get('layer_info')
        layer_row = int(layer_info.get(layer.upper())['row'])
        coord_x, coord_y = page.graphic_left_layer_bar_first_row_coord
        row_height = page.engineering_file_input_file_row_height
        coord_y = coord_y + (layer_row - 1) * row_height
        layer_coord = (coord_x, coord_y)
        self.graphic_window.click_input(button='right',coords=layer_coord)  # 右击layer
        time.sleep(time_sleep)

    def click_canvas(self,coord_x=page.graphic_canvas_centre_coord[0],
                           coord_y=page.graphic_canvas_centre_coord[1],time_sleep = 0.5):
        """
        右击画布
        :param coord_x:
        :param coord_y:
        """
        coords= (coord_x, coord_y)
        self.graphic_window.click_input(coords=coords)  # 右击画布
        time.sleep(time_sleep)

    def open_step_panelization_by_table(self):
        self.graphic_window.click_input(coords=page.graphic_step_coord)
        self.graphic_window.click_input(coords=page.graphic_step_panelzation_coord)
        self.graphic_window.click_input(coords=page.graphic_step_panelization_by_table_coord)

    def close_by_table_window(self):
        self.graphic_window.click_input(coords=page.graphic_by_table_window_close_coord)

    def add_new_step_by_table_mirror(self):
        self.graphic_window.click_input(coords=page.graphic_by_table_new_step_coord)
        self.graphic_window.click_input(coords=page.graphic_by_table_new_step_pcs_coord)
        self.graphic_window.click_input(coords=page.graphic_by_table_new_step_pcs_ok_coord)
        self.graphic_window.click_input(coords=page.graphic_by_table_new_step_mirror_coord)
        self.graphic_window.click_input(coords=page.graphic_by_table_new_step_mirror_yes_coord)


    def right_click_canvas(self,coord_x=page.graphic_canvas_centre_coord[0],
                           coord_y=page.graphic_canvas_centre_coord[1],time_sleep = 0.5):
        """
        右击画布
        :param coord_x:
        :param coord_y:
        """
        coords= (coord_x, coord_y)
        self.graphic_window.click_input(button='right', coords=coords)  # 右击画布
        time.sleep(time_sleep)