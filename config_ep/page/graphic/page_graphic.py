from config import RunConfig
from config_ep import page
from config_ep.page import graphic
from config_ep.page.graphic import left_layer_bar
from config_ep.page.graphic import central_canvas
import time
import cv2
import os
from cc.cc_method import opencv_compare
from pywinauto.keyboard import send_keys
import pyautogui


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
            **left_layer_bar.right_click_menu_window_para)
        self.graphic_left_layer_bar_right_click_menu_window.click_input(
            coords=left_layer_bar.right_click_menu_copper_exposed_area_coords)

    def open_measurement_mark_window(self):
        """
        打开Measurement Mark窗口
        """
        self.graphic_canvas_right_click_menu_window = RunConfig.driver_epcam_ui.window(
            **central_canvas.right_click_menu_window_para)
        self.graphic_canvas_right_click_menu_window.click_input(
            coords=central_canvas.right_click_menu_measure_coords)

    def click_layer(self,job_info:dict,layer:str, max_layer_row:int = graphic.left_layer_bar_max_layer_row,
                    min_layer_row:int = graphic.left_layer_bar_min_layer_row, button_type:str = 'left',
                    time_sleep:float=0.5):
        """
        单击层别
        :param job_info:
        :param layer:
        :param max_layer_row:
        :param min_layer_row:
        :param button_type:
        :param time_sleep:
        :return:
        """
        layer_info = job_info.get('layer_info')
        layer_row = int(layer_info.get(layer.upper())['row'])
        coord_x, coord_y = graphic.left_layer_bar_first_row_coord
        row_height = graphic.left_layer_bar_row_height
        # coord_y = 165 + layer_row * row_height - 15
        layer_coord_y = coord_y + (layer_row -1) * row_height
        if (layer_row <= graphic.left_layer_bar_max_layer_row and
                max_layer_row == graphic.left_layer_bar_max_layer_row and
                min_layer_row == graphic.left_layer_bar_min_layer_row):
            self.graphic_window.click_input(button=button_type, coords=(coord_x, layer_coord_y))
        else:
            if layer_row > max_layer_row:
                layer_coord_y = coord_y + (graphic.left_layer_bar_max_layer_row -1 ) * row_height
                diff = layer_row - max_layer_row
                for num in range(diff):
                    self.graphic_window.click_input(coords=graphic.left_layer_bar_scroll_bar_bot_button_coords)
                max_layer_row = layer_row
                min_layer_row = min_layer_row + diff
            elif layer_row < min_layer_row:
                layer_coord_y = coord_y
                diff = min_layer_row - layer_row
                for num in range(diff):
                    self.graphic_window.click_input(coords=graphic.left_layer_bar_scroll_bar_top_button_coords)
                max_layer_row = max_layer_row - diff
                min_layer_row = min_layer_row - diff
            else:
                layer_coord_y = coord_y + (layer_row - min_layer_row) * row_height
            self.graphic_window.click_input(button=button_type, coords=(coord_x, layer_coord_y))
        time.sleep(time_sleep)
        print("最大row:{}".format(max_layer_row))
        print("最小row:{}".format(min_layer_row))
        return max_layer_row, min_layer_row

    def click_affected_layer(self, job_info: dict, layer: str, max_layer_row: int = graphic.left_layer_bar_max_layer_row
                             , min_layer_row: int = graphic.left_layer_bar_min_layer_row, button_type: str = 'left',
                             time_sleep: float = 0.5):
        """
        单击层别
        :param job_info:
        :param layer:
        :param max_layer_row:
        :param min_layer_row:
        :param button_type:
        :param time_sleep:
        :return:
        """
        layer_info = job_info.get('layer_info')
        layer_row = int(layer_info.get(layer.upper())['row'])
        coord_x, coord_y = graphic.left_layer_bar_first_row_affected_layer_coord
        row_height = graphic.left_layer_bar_row_height
        # coord_y = 165 + layer_row * row_height - 15
        layer_coord_y = coord_y + (layer_row -1) * row_height
        if (layer_row <= graphic.left_layer_bar_max_layer_row and
                max_layer_row == graphic.left_layer_bar_max_layer_row and
                min_layer_row == graphic.left_layer_bar_min_layer_row):
            self.graphic_window.click_input(button=button_type, coords=(coord_x, layer_coord_y))
        else:
            if layer_row > max_layer_row:
                layer_coord_y = coord_y + (graphic.left_layer_bar_max_layer_row - 1) * row_height
                diff = layer_row - max_layer_row
                for num in range(diff):
                    self.graphic_window.click_input(coords=graphic.left_layer_bar_scroll_bar_bot_button_coords)
                max_layer_row = layer_row
                min_layer_row = min_layer_row + diff
            elif layer_row < min_layer_row:
                layer_coord_y = coord_y
                diff = min_layer_row - layer_row
                for num in range(diff):
                    self.graphic_window.click_input(coords=graphic.left_layer_bar_scroll_bar_top_button_coords)
                max_layer_row = max_layer_row - diff
                min_layer_row = min_layer_row - diff
            else:
                layer_coord_y = coord_y + (layer_row - min_layer_row) * row_height
            self.graphic_window.click_input(button=button_type, coords=(coord_x, layer_coord_y))
        time.sleep(time_sleep)
        print("最大row:{}".format(max_layer_row))
        print("最小row:{}".format(min_layer_row))
        return max_layer_row, min_layer_row

    def click_canvas(self,coord_x:float=graphic.canvas_centre_coord[0],
                           coord_y:float=graphic.canvas_centre_coord[1],
                     button_type:str='left', time_sleep:float = 0.5):
        """
        点击画布
        :param coord_x:
        :param coord_y:
        :param button_type:
        :param time_sleep:
        """
        coords= (coord_x, coord_y)
        self.graphic_window.click_input(button=button_type,coords=coords)  # 点击画布
        time.sleep(time_sleep)

    def double_click_canvas(self,coord_x:float=graphic.canvas_centre_coord[0],
                           coord_y:float=graphic.canvas_centre_coord[1],button_type='left', time_sleep = 0.5):
        """
        点击画布
        :param coord_x:
        :param coord_y:
        """
        coords= (coord_x, coord_y)
        self.graphic_window.double_click_input(button=button_type,coords=coords)  # 双击
        time.sleep(time_sleep)

    def open_step_and_repeat_puzzle_by_automatic_window(self):
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_step_coord)
        self.graphic_window.click_input(coords=graphic.step_panelization_coord)
        self.graphic_window.click_input(coords=graphic.step_panelization_step_and_repeat_puzzle_by_automatic_coord)

    def open_step_and_repeat_puzzle_by_table_window(self):
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_step_coord)
        self.graphic_window.click_input(coords=graphic.step_panelization_coord)
        self.graphic_window.click_input(coords=graphic.step_panelization_step_and_repeat_puzzle_by_table_coord)

    def open_step_and_repeat_edit_window(self):
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_step_coord)
        self.graphic_window.click_input(coords=graphic.step_panelization_coord)
        self.graphic_window.click_input(coords=graphic.step_panelization_step_and_repeat_edit_coord)

    def open_multi_layer_copy_window(self):
        """
        打开Multi Layer Copy窗口
        """
        self.graphic_left_layer_bar_right_click_menu_window = RunConfig.driver_epcam_ui.window(
            **left_layer_bar.right_click_menu_window_para)
        self.graphic_left_layer_bar_right_click_menu_window.click_input(
            coords=left_layer_bar.right_click_menu_multi_layer_copy_coords)

    def feature_selection(self):
        coord = self.get_right_tool_bar_button_coords(graphic.right_tool_bar_feature_selection_coord)
        self.graphic_window.click_input(coords=coord)

    def zoom_home(self):
        coord = self.get_right_tool_bar_button_coords(graphic.right_tool_bar_zoom_home_coord)
        self.graphic_window.click_input(coords=coord)

    def area_zoom(self):
        coord = self.get_right_tool_bar_button_coords(graphic.right_tool_bar_area_zoom_coord)
        self.graphic_window.click_input(coords=coord)

    def feature_selection_filter(self):
        coord = self.get_right_tool_bar_button_coords(graphic.right_tool_bar_feature_selection_filter_coord)
        self.graphic_window.click_input(coords=coord)

    def select_by_net(self):
        coord = self.get_right_tool_bar_button_coords(graphic.right_tool_bar_select_by_net_coord)
        self.graphic_window.click_input(coords=coord)

    def open_angle_for_usersymbol_ok(self):
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_edit_coord)
        self.graphic_window.click_input(coords=graphic.edit_usersymbol_coord)
        self.graphic_window.click_input(coords=graphic.edit_usersymbol_angle_for_usersymbol_coord)
        self.graphic_window.click_input(coords=graphic.edit_usersymbol_angle_for_usersymbol_ok_coord)

    def open_create_usersymbol(self):
        """
        打开edit菜单栏下的Creat_UserSymbol窗口
        """
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_edit_coord)
        self.graphic_window.click_input(coords=graphic.edit_usersymbol_coord)
        self.graphic_window.click_input(coords=graphic.edit_usersymbol_create_usersymbol_coord)

    def open_analysis_signal_layer_check_windows(self):
        self.graphic_window.click_input(coords=page.graphic_analysis_coord)
        self.graphic_window.click_input(coords=page.graphic_analysis_signal_layer_check_coord)

    def open_robotcam(self):
        """打开step菜单栏下的robotcam窗口"""
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_step_coord)
        self.graphic_window.click_input(coords=graphic.step_robotcam_coords)

    def open_mrc(self):
        """打开Analysis菜单栏下的mrc窗口"""
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_analysis_coords)
        self.graphic_window.click_input(coords=graphic.analysis_mrc_coords)

    def click_unit_british_system(self):
        """切换graphic主界面的单位"""
        self.graphic_window.click_input(coords=graphic.right_tool_bar_unit_british_system_coords)

    def open_add_solt_by_drillmap_window(self):
        self.graphic_window.click_input(coords=page.graphic.upper_menu_bar_edit_coord)
        self.graphic_window.click_input(coords=page.graphic.edit_add_solt_by_drillmap_coord)

    def open_chain(self):
        """
        打开上方菜单栏ROUT的chain功能
        """
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_rout_coords)
        self.graphic_window.click_input(coords=graphic.rout_chain_coords)

    def click_delete_feature(self,delete_type:int=0):
        """
        点击右侧工具栏delete_feature功能
        :param delete_type:0代表delete feature类型,1代表delete_to_intresetion类型
        """
        if delete_type in (0, 1):
            if delete_type == 0:
                self.graphic_window.click_input(coords=graphic.right_tool_bar_delete_feature_coords)
            else:
                self.graphic_window.click_input(button="right",coords=graphic.right_tool_bar_delete_feature_coords)
                self.graphic_window.click_input(coords=graphic.right_tool_bar_delete_to_intresetion_coords)
        else:
            raise ValueError("Parameter must be 0 or 1")

    def execute_delete_to_intresetion(self,coord_x:float,coord_y:float,key_downs:int=0,time_sleep:float=0.5):
        """
        使用delete_to_intresetion功能
        :param coord_x:
        :param coord_y:
        :param key_downs:
        :param time_sleep:
        """
        self.graphic_window.click_input(coords=(coord_x,coord_y))
        time.sleep(time_sleep)
        for key in range(key_downs):
            pyautogui.keyDown('n')
        time.sleep(time_sleep)
        self.graphic_window.double_click_input(coords=(coord_x, coord_y))

    def click_move_feature(self, time_sleep=0.5):
        """点击右侧工具栏的move feature功能"""
        self.graphic_window.click_input(coords=graphic.right_tool_bar_move_feature_coords)
        time.sleep(time_sleep)

    def click_copy_feature(self, time_sleep=0.5):
        """点击右侧工具栏的copy feature功能"""
        coords = self.get_right_tool_bar_button_coords(graphic.right_tool_bar_copy_feature_coords)
        self.graphic_window.click_input(coords=coords)
        time.sleep(time_sleep)


    def open_connection_window(self):
        self.graphic_window.click_input(coords=page.graphic.upper_menu_bar_edit_coord)
        self.graphic_window.click_input(coords=page.graphic.edit_connection_coord)

    def open_contour2pad_window(self):
        self.graphic_window.click_input(coords=page.graphic.upper_menu_bar_edit_coord)
        self.graphic_window.click_input(coords=page.graphic.edit_reshape_coord)
        self.graphic_window.click_input(coords=page.graphic.edit_reshape_contour2pad_coord)

    def open_substitute_window(self):
        self.graphic_window.click_input(coords=page.graphic.upper_menu_bar_edit_coord)
        self.graphic_window.click_input(coords=page.graphic.edit_reshape_coord)
        self.graphic_window.click_input(coords=page.graphic.edit_reshape_substitute_coord)

    def open_split_layer_window(self):
        """
        打开Split Layer窗口
        """
        self.graphic_left_layer_bar_right_click_menu_window = RunConfig.driver_epcam_ui.window(
            **left_layer_bar.right_click_menu_window_para)
        self.graphic_left_layer_bar_right_click_menu_window.click_input(
            coords=left_layer_bar.right_click_menu_split_layer_coords)
        # self.graphic_left_layer_bar_right_click_menu_window.click_input(
        #     coords=(30, 285)) # 2.29.055_s17版本坐标

    def open_dynamic_etch_compensation_window(self):
        """
        打开dynamic_etch_compensation窗口
        """
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_dfm_coords)
        self.graphic_window.click_input(coords=graphic.dfm_yield_improvement_coords)
        self.graphic_window.click_input(coords=graphic.dfm_yield_improvement_dynamic_etch_compensation_coords)

    def open_mark_note_window(self):
        """
        打开Mark Note窗口
        """
        self.graphic_left_layer_bar_right_click_menu_window = RunConfig.driver_epcam_ui.window(
            **left_layer_bar.right_click_menu_window_para)
        self.graphic_left_layer_bar_right_click_menu_window.click_input(
            coords=left_layer_bar.right_click_menu_mark_note_coords)

    def add_double_click(self, double_x, double_y, time_sleep=0.8):
        """
        双击画布，添加mark note
        :param double_x: 双击的横坐标
        :param double_y: 双击的纵坐标
        """
        coords = (double_x, double_y)
        self.graphic_window.double_click_input(coords=coords)
        time.sleep(time_sleep)

    def open_dfm_cleanup_construct_pad_window(self):
        """打开DFM菜单栏下的construct_pad窗口"""
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_dfm_coords)
        self.graphic_window.click_input(coords=graphic.dfm_cleanup_coords)
        self.graphic_window.click_input(coords=graphic.construct_pad_coords)

    def click_undo_button(self):
        """点击edit菜单栏下的undo"""
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_edit_coord)
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_edit_undo_coords)

    def open_global_window(self):
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_edit_coord)
        self.graphic_window.click_input(coords=graphic.edit_resize_coord)
        self.graphic_window.click_input(coords=graphic.edit_resize_global_coord)

    def file_close(self):
        self.graphic_window.click_input(coords=graphic.file_coord)
        self.graphic_window.click_input(coords=graphic.file_close_coord)

    def open_powerground_optimization_window(self):
        """
        打开PowerGround_Optimization窗口
        """
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_dfm_coords)
        self.graphic_window.click_input(coords=graphic.dfm_optimization_coords)
        self.graphic_window.click_input(coords=graphic.dfm_powerground_optimization_coords)

    def get_right_tool_bar_button_coords(self,col_row:list):
        """
        获取右侧工具栏按钮坐标
        """
        col = col_row[0]
        row = col_row[1]
        if 1 <= col <= 4 and 1 <= row <= 11:
            coord_x = graphic.right_tool_bar_first_button_corrds[0] + (
                        col - 1) * graphic.right_tool_bar_button_x_spacing
            coord_y = graphic.right_tool_bar_first_button_corrds[1] + (
                        row - 1) * graphic.right_tool_bar_button_y_spacing
            return coord_x,coord_y
        elif 4 <= col <= 1:
            raise ValueError("parameter 'col' must be 1 - 4")
        elif 11 <= row <= 1:
            raise ValueError("parameter 'row' must be 1 - 11")

    def click_add_feature(self):
        """点击Add Feature按钮"""
        coords = self.get_right_tool_bar_button_coords(graphic.right_tool_bar_add_feature_coords)
        self.graphic_window.click_input(coords=coords)

    def click_job_matrix_button(self):
        """在Graphic界面通过job_matrix按钮打开Matrix界面"""
        self.graphic_window.click_input(coords=graphic.open_job_matrix)

    def click_edit_delete_button(self, time_sleep=0.5):
        """点击edit菜单栏的delete功能"""
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_edit_coord)
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_edit_delete_coords)
        time.sleep(time_sleep)


    def click_drill_check_window(self):
        """打开Analysis菜单栏下的drill check窗口"""
        self.graphic_window.click_input(coords=graphic.upper_menu_bar_analysis_coords)
        self.graphic_window.click_input(coords=graphic.analysis_drill_check_coords)
