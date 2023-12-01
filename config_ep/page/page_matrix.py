from config import RunConfig
from config_ep import page
import time
import cv2
import os
from cc.cc_method import opencv_compare


class PageMatrix(object):
    def __init__(self):
        self.matrix_window = RunConfig.driver_epcam_ui.window(**page.matrix_window_pare)
        self.matrix_window_scroll_coord = None

    def drill_correlation_layer_is_right(self):
        self.matrix_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.matrix_window.capture_as_image()  # 截图
        drill_correlation_layer_pic.save(r'C:\cc\share\temp\drill_correlation_layer.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\drill_correlation_layer.png')
        img_cut = img[190:700, 17:187]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\drill_correlation_layer_cute.png", img_cut)
        # cv2.waitKey(0)
        # # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'matrix\drill_correlation_layer_cute_standard.png')
        img_current_path = r'C:\cc\share\temp\drill_correlation_layer_cute.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def close(self):
        self.matrix_window.child_window(title="关闭", control_type="Button").click_input()  #关闭matrix窗口

    def select_drill_layer(self):
        self.matrix_window.click_input(coords=page.matrix_drill_layer_coord) # 选中drill层

    def select_drill_correlation_top(self, time_sleep = 0.5):
        self.matrix_window.click_input(coords=page.matrix_drill_correlation_top_coord) # 选中drill关联线的顶部
        time.sleep(time_sleep)

    def select_drill_correlation_bot(self, time_sleep = 0.5):
        self.matrix_window.click_input(coords=page.matrix_drill_correlation_bot_coord) # 选中drill关联线的底部
        time.sleep(time_sleep)