import os
from pathlib import Path

import cv2

from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page


class PageToolSizeEdit(object):
    def __init__(self):
        self.engineering_input_tool_size_edit_window = RunConfig.driver_epcam_ui.window(
            **page.engineering_file_input_tool_size_edit_window_para)

    def close(self):
        pass
        self.engineering_input_tool_size_edit_window.click_input(
            coords=page.engineering_file_input_tool_size_edit_close_coord)


    def is_right(self):
        tool_size_edit_window_pic = self.engineering_input_tool_size_edit_window.capture_as_image()  # 截图
        tool_size_edit_window_pic.save(r'C:\cc\share\temp\tool_size_edit_window.png')  # 保存到硬盘
        # 显示图像
        # tool_size_edit_window_pic.show()  # PIL方式显示图像
        img = cv2.imread(r'C:\cc\share\temp\tool_size_edit_window.png')
        # img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
        img_cut = img[0:732, 8:808]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\tool_size_edit_window_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(
            Path(os.path.dirname(__file__)).parent.parent,
            r'data\pic\engineering\tool_size_edit_window_standard.png')
        img_current_path = r'C:\cc\share\temp\tool_size_edit_window_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0