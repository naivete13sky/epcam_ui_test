import os
import time
import cv2
from cc.cc_method import opencv_compare
from cc.cc_method import PictureMethod
from config import RunConfig
from config_ep import page

class PageCopperExposedArea(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到copper/exposed area子窗口
        self.copper_exposed_area_window = self.graphic_window.child_window(
            **page.graphic_left_layer_bar_copper_exposed_area_window_para)

        self.temp_path = RunConfig.temp_path_base

    def capture_image(self, img_name):
        self.copper_exposed_area_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.copper_exposed_area_window.capture_as_image()  # 截图
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

    def warning_window_capture_image(self, img_name):
        self.warning_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.warning_window.capture_as_image()  # 截图
        save_path = os.path.join(self.temp_path, img_name + '.png')
        drill_correlation_layer_pic.save(save_path)  # 保存到硬盘
        return save_path

    def is_right(self,save_path_cut, img_standard_str):
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         img_standard_str)
        img_current_path = save_path_cut
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def apply_exposed_area(self,layer_1="name",mask_1=None,layer_2=None,mask_2=None):
        """
        执行exposed_area
        :param layer_1:
        :param mask_1:
        :param layer_2:
        :param mask_2:
        :return:
        """
        self.copper_exposed_area_window.click_input(coords=page.graphic_copper_exposed_area_measurement_exposed_area_coords)
        self.warning_window = RunConfig.driver_epcam_ui.window(
            **page.graphic_copper_exposed_area_warning_window_para)
        self.copper_exposed_area_window.click_input(coords=page.graphic_copper_exposed_area_apply_button_coords)
        if layer_1:
            if mask_1:
                print("mask_1")
            else:
                img_name = 'warning'
                img_path = self.warning_window_capture_image(img_name)
                cut_coords = [30, 70, 30, 150]
                save_path_cut = self.cut_img(img_path, img_name, cut_coords)
                text = PictureMethod.get_text_from_img(save_path_cut)
                self.warning_window.child_window(title="关闭", control_type="Button").click_input()
                self.copper_exposed_area_window.child_window(title="关闭", control_type="Button").click_input()
                return text
        else:
            print("layer_1")
        if layer_2:
            if mask_2:
                print("mask_2")
            else:
                print("warning")




