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

    def is_right(self,img_name, cut_coords, img_standard_str):
        self.graphic_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        dcode_edit_window_pic = self.graphic_window.capture_as_image()  # 截图
        save_path = os.path.join(self.temp_path,img_name + '.png')
        dcode_edit_window_pic.save(save_path)  # 保存到硬盘
        # 显示图像
        # tool_size_edit_window_pic.show()  # PIL方式显示图像
        img = cv2.imread(save_path)
        # img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
        img_cut = img[cut_coords[0]:cut_coords[1], cut_coords[2]:cut_coords[3]]  # 后面的是水平方向
        save_path_cut = os.path.join(self.temp_path,img_name + '_cut.png')
        cv2.imwrite(save_path_cut, img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         img_standard_str)
        img_current_path = save_path_cut
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0
