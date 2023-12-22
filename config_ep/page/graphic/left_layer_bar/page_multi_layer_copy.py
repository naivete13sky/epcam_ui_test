import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import left_layer_bar
from pywinauto.keyboard import send_keys

class PageMultiLayerCopy(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Multi Layer Copy子窗口
        self.multi_layer_copy_window = self.graphic_window.child_window(
            **left_layer_bar.multi_layer_copy_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.multi_layer_copy_window.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.multi_layer_copy_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.multi_layer_copy_window.capture_as_image()  # 截图
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

    def multi_layer_copy_case_4651(self,job_info,soure_job=None,soure_step=None,add_layers:list=None,prefix=None,suffix=None):
        if soure_job:
            print("123")
        if soure_step:
            self.multi_layer_copy_window.click_input(coords=left_layer_bar.multi_layer_copy_source_step_button_coords)
            self.open_steps_pop_window(job_info,soure_step)
        if suffix:
            self.multi_layer_copy_window.click_input(coords=left_layer_bar.multi_layer_copy_suffix_text_coords)
            send_keys(suffix)
        if add_layers:
            self.multi_layer_copy_window.click_input(coords=left_layer_bar.multi_layer_copy_add_layers_button_coords)
            self.open_layers_pop_window(job_info, add_layers)

        self.click_ok_button()
        self.information_pop_window()
        self.information_pop_window()
        time.sleep(5)

    def open_steps_pop_window(self,job_info,step):
        """
        点击Source step按钮打开Steps Popup窗口
        :param job_info:
        :param step:
        """
        step_info = job_info.get('step_info')
        step_col = int(step_info.get(step.upper())['col'])
        # 切换到Steps Popup子窗口
        self.steps_pop_window = self.graphic_window.child_window(
            **left_layer_bar.multi_layer_copy_steps_pop_window_para)

        coord_x = left_layer_bar.multi_layer_copy_steps_pop_first_row_coords[0]
        coord_y = left_layer_bar.multi_layer_copy_steps_pop_first_row_coords[1] + (
                step_col - 1) * left_layer_bar.multi_layer_copy_steps_pop_row_spacing
        coords = (coord_x, coord_y)
        self.steps_pop_window.double_click_input(coords=coords)

    def open_layers_pop_window(self,job_info,layers):
        """
        点击Add Layers按钮打开Layer Popup窗口
        :param job_info:
        :paramm layers:
        """
        layer_info = job_info.get('layer_info')
        for layer in layers:
            layer_row = int(layer_info.get(layer.upper())['row'])
            # 切换到Layers Popup子窗口
            self.layers_pop_window = self.graphic_window.child_window(
                **left_layer_bar.multi_layer_copy_layers_pop_window_para)

            coord_x = left_layer_bar.multi_layer_copy_layers_pop_first_row_coords[0]
            coord_y = left_layer_bar.multi_layer_copy_layers_pop_first_row_coords[1] + (
                    layer_row - 1) * left_layer_bar.multi_layer_copy_layers_pop_row_spacing
            coords = (coord_x, coord_y)
            self.layers_pop_window.click_input(coords=coords)
        self.layers_pop_window.click_input(coords=left_layer_bar.multi_layer_copy_layers_pop_ok_button_coords)

    def click_ok_button(self):
        """
        点击Ok按钮
        """
        self.multi_layer_copy_window.click_input(coords=left_layer_bar.multi_layer_copy_ok_button_coords)

    def information_pop_window(self):
        """
        点击提示框的Ok按钮
        """
        # 切换到Information子窗口
        self.information_window = self.graphic_window.child_window(
            **left_layer_bar.information_window_para)
        self.information_window.click_input(coords=left_layer_bar.information_ok_button_coords)

