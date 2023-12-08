import os
import time
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page


class PageViewGraphic(object):
    def __init__(self):
        self.engineering_input_view_graphic_dindow = RunConfig.driver_epcam_ui.window(
            **page.engineering_file_input_view_graphic_window_para
        )
        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.engineering_input_view_graphic_dindow.click_input(
            coords=page.engineering_file_input_view_graphic_close_coord)

    def cut_img(self, img_name, cut_coords = None):
        self.engineering_input_view_graphic_dindow.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.engineering_input_view_graphic_dindow.capture_as_image()  # 截图
        save_path = os.path.join(self.temp_path, img_name + '.png')
        drill_correlation_layer_pic.save(save_path)  # 保存到硬盘
        if cut_coords:
            img = cv2.imread(save_path)
            img_cut = img[cut_coords[0]:cut_coords[1], cut_coords[2]:cut_coords[3]]  # 后面的是水平方向
            save_path_cut = os.path.join(self.temp_path, img_name + '_cut.png')
            cv2.imwrite(save_path_cut, img_cut)
            cv2.waitKey(0)
            return save_path_cut
        # cv2.waitKey(0)
        return save_path

    def is_right(self, save_path_cut, img_standard_str):
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
            img_standard_str)
        img_current_path = save_path_cut
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0