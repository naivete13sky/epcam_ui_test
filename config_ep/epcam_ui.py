from cc.cc_method import get_print_control_identifiers_text, get_coor_of_object
from config import RunConfig

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 根据你的Tesseract安装路径设置
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

class Engineering(object):
    # 获得坐标
    def getCoor(self,window,wanted_title):
        win_text = get_print_control_identifiers_text(window)
        coor_ok = get_coor_of_object(wanted_title, win_text)
        return coor_ok

    def get_engineering_left_top_Coor(self):
        win_text2 = get_print_control_identifiers_text(self.engineering_window)
        coor_ok = get_coor_of_object(RunConfig.driver_epcam_ui_engineering_title,win_text2)
        return coor_ok

