import os
import sys
import re
import time
from pathlib import Path
import cv2
from PIL import Image
from pywinauto import mouse
from pywinauto.keyboard import send_keys
from cc.cc_method import get_print_control_identifiers_text, get_coor_of_object, opencv_compare
from config_ep import page
from config import RunConfig
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 根据你的Tesseract安装路径设置
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

class PageEngineering(object):
    def __init__(self):
        self.set_default_ui_para()
        self.engineering_window = RunConfig.driver_epcam_ui.window(**self.engineering_window_para)

    def set_default_ui_para(self):
        pass
        # engineering_window
        self.engineering_window_para = {'title': RunConfig.driver_epcam_ui_engineering_title}

        # import job窗口
        self.engineering_import_window_child_window_para = {'title': "Import Job", 'control_type': "Window"}

        # import job窗口，获得选择文件类型控件
        self.engineering_import_input_path_file_type_window_para = {'title': "文件类型(T):", 'auto_id': "1136",
                                                               'control_type': "ComboBox"}

        # 选择文件窗口中的文件路径对象
        self.engineering_import_input_path_file_path_window_para = {'title': "文件名(N):", 'auto_id': "1148",
                                                               'control_type': "ComboBox"}

        # 确认选择中的文件
        self.engineering_import_input_path_confirm_window_para = {'title': "打开(O)", 'auto_id': "1",
                                                             'control_type': "Button"}

        # input job窗口
        self.engineering_input_window_child_window_para = {'title': "Input", 'control_type': "Window"}

        # input 选择文件窗口中的文件路径对象
        self.engineering_input_path_file_path_window_para = {'title': "Open", 'control_type': "Window"}



    def job_first_is_opened(self):
        self.engineering_window.set_focus()  # 激活窗口
        # 截图
        engineering_window_jpg = self.engineering_window.capture_as_image()
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window.png')
        # img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
        img_cut = img[225:307, 46:137]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_job_first.png", img_cut)
        cv2.waitKey(0)

        # 加载两张图片
        img_standard_path = os.path.join(Path(os.path.dirname(__file__)).parent,
                                         r'data\pic\engineering\engineering_job_first_opened_standard.jpg')
        img_current_path = r'C:\cc\share\temp\engineering_job_first.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)

        return rectangle_count == 0

    def close_job_first(self):
        self.engineering_window.click_input(coords=page.engineering_jobList_first)  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(button="right", coords=page.engineering_jobList_first)
        self.engineering_window.click_input(coords=(page.engineering_jobList_first[0] + 20,page.engineering_jobList_first[1] + 50))
        send_keys("{ENTER}")