import os
from pathlib import Path
import cv2
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page


class PageInputViewAscii(object):
    def __init__(self):
        self.engineering_input_view_ascii_window = RunConfig.driver_epcam_ui.window(
            **page.engineering_file_input_view_ascii_window_para)


    def close(self):
        self.engineering_input_view_ascii_window.click_input(
            coords=page.engineering_file_input_view_ascii_close_coord)


    def is_right(self):
        input_view_ascii_window_pic = self.engineering_input_view_ascii_window.capture_as_image()  # 截图
        input_view_ascii_window_pic.save(r'C:\cc\share\temp\input_view_ascii_window.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\input_view_ascii_window.png')
        img_cut = img[0:822, 8:1005]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\input_view_ascii_window_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(
            Path(os.path.dirname(__file__)).parent.parent,
            r'data\pic\engineering\input_view_ascii_window_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\input_view_ascii_window_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def minimize(self):
        self.engineering_input_view_ascii_window.child_window(title="最小化", control_type="Button").click_input()