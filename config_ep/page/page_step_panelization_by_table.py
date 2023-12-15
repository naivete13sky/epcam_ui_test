import os
import time
import cv2
from cc.cc_method import opencv_compare
from cc.cc_method import PictureMethod
from config import RunConfig
from config_ep import page

class PageSetpAndRepeatPuzzleByTabel(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Step And Repeat P_panelization_by_table子窗口
        self.setp_and_repeat_puzzle_by_tabel = self.graphic_window.child_window(
            **page.graphic_step_panelization_by_table_window_para)

        self.temp_path = RunConfig.temp_path_base

    def capture_image(self, img_name):
        self.setp_and_repeat_puzzle_by_tabel.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.setp_and_repeat_puzzle_by_tabel.capture_as_image()  # 截图
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