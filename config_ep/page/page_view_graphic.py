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

    def close(self):
        self.engineering_input_view_graphic_dindow.click_input(
            coords=page.engineering_file_input_view_graphic_close_coord)

    def is_right(self):
        self.engineering_input_view_graphic_dindow.set_focus()  # 激活窗口
        time.sleep(0.1)
        dcode_edit_window_pic = self.engineering_input_view_graphic_dindow.capture_as_image()  # 截图
        dcode_edit_window_pic.save(r'C:\cc\share\temp\view_graphic_window.png')  # 保存到硬盘
        # 显示图像
        # tool_size_edit_window_pic.show()  # PIL方式显示图像
        img = cv2.imread(r'C:\cc\share\temp\view_graphic_window.png')
        # img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
        img_cut = img[0:511, 8:648]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\view_graphic_window_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
            r'engineering\view_graphic_window_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\view_graphic_window_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0