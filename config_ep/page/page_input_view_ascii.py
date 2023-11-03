import os
import time
from pathlib import Path
import cv2
import pyautogui
from pywinauto.keyboard import send_keys
from pywinauto.mouse import click,release
from cc.cc_method import opencv_compare, PictureMethod
from config import RunConfig
from config_ep import page


class PageInputViewAscii(object):
    def __init__(self):
        self.engineering_input_view_ascii_window = RunConfig.driver_epcam_ui.window(
            **page.engineering_file_input_view_ascii_window_para)
        self.engineering_input_view_ascii_window_scroll_coord = None


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

    def maximize(self):
        send_keys('%{TAB}')  # 模拟按下 Alt + Tab,可以将最小化的窗口再恢复。

    def scroll(self):
        large_pic_path = r'C:\cc\share\temp\input_view_ascii_window.png'
        if not os.path.exists(large_pic_path):
            engineering_input_view_ascii_window= self.engineering_input_view_ascii_window.capture_as_image()
            engineering_input_view_ascii_window.save(large_pic_path)
        small_pic_path = r"data\pic\engineering\input_view_ascii_window_scroll_standard.png"
        top_left, bottom_right = PictureMethod.get_small_pic_position_from_large_pic(small_pic_path, large_pic_path)
        x = int((top_left[0] + bottom_right[0])/2)
        y = int((top_left[1] + bottom_right[1])/2)
        print('x,y:',x,y)
        self.engineering_input_view_ascii_window.click_input(coords=(x, y))
        pyautogui.mouseDown()  # 按下鼠标
        pyautogui.moveTo(452 + x, 85 + y + 10, duration=2)  # 移动鼠标以模拟拖动滚动条垂直方向移动10像素，duration控制拖动速度
        pyautogui.mouseUp()  # 释放鼠标左键，完成滚动操作
        time.sleep(100)

