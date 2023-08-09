import sys
import re
import time

from pywinauto import mouse
from pywinauto.keyboard import send_keys
from config import RunConfig


class TextArea(object):
    def __init__(self):
        self.buffer = []
    def write(self,*args,**kwargs):
        self.buffer.append(args)

def get_print_control_identifiers_text(object_print_control_identifiers):
    stdout = sys.stdout
    sys.stdout = TextArea()
    object_print_control_identifiers.print_control_identifiers()
    text_area, sys.stdout = sys.stdout, stdout
    # print('text_area.buffer:',text_area.buffer)
    return text_area.buffer

def get_coor_of_object(text_wanted,text_from):
    pass
    for tup in text_from:
        i = tup[0].find(text_wanted)
        if i > 0:
            pattern = re.compile(r"(\(L\d+, T\d+, R\d+, B\d+\))")
            result = pattern.findall(tup[0])
            tup_coor = result[0]
    coor_file_w = int(tup_coor.split(",")[0][2:]) + 1
    coor_file_h = int(tup_coor.split(",")[1][2:]) + 1
    return (coor_file_w, coor_file_h)

class EPCAM(object):
    def __init__(self):
        pass
        self.engineering_window = RunConfig.driver_epcam_ui.window(title="Engineering 1.1.7.2")

    def delete_all_jobs(self):
        # 清空料号，ctrl + A 全选料号，然后 ctrl + B删除
        self.engineering_window.set_focus()  # 激活窗口
        send_keys("^a")  # 发送 Ctrl + A 快捷键，全选
        send_keys("^b")  # 发送 Ctrl + B 快捷键，删除
        send_keys("{ENTER}")  # 发送回车键，删除
        send_keys("{ENTER}")  # 发送回车键，确认删除所有
        time.sleep(3)


    def import_ipc2581(self,file_path):
        #点击菜单File(F)--import
        self.engineering_window.click_input(coords=self.get_engineering_file_Coor(coor_type='relative'))# 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(coords=self.get_engineering_import_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口

        # 切换到import job窗口
        engineering_import_window = self.engineering_window.child_window(title="Import Job", control_type="Window")
        engineering_import_window.click_input(coords=(30,100))# 点击菜单input path

        # 获得选择文件类型控件
        engineering_import_input_path_file_type_window=self.engineering_window.child_window(title="文件类型(T):", auto_id="1136", control_type="ComboBox")
        engineering_import_input_path_file_type_window.select("ipc2581(*.xml *.cvg)")#根据文本选择下拉列表项

        # 选择文件对象
        engineering_import_input_path_file_path_window=self.engineering_window.child_window(title="文件名(N):", auto_id="1148", control_type="ComboBox")
        engineering_import_input_path_file_path_window.draw_outline(colour = 'red')# 绘制边框以突出显示控件（可以自行指定颜色和宽度）
        engineering_import_input_path_file_path_window.click_input()  # 将焦点设置到控件上
        send_keys(file_path)  # 输入文本

        # 确认选择中的文件
        engineering_import_input_path_confirm_window=self.engineering_window.child_window(title="打开(O)", auto_id="1", control_type="Button")
        engineering_import_input_path_confirm_window.click_input()

        # 切换到import job窗口
        engineering_import_window = self.engineering_window.child_window(title="Import Job", control_type="Window")
        engineering_import_window.click_input(coords=(30,200))
        send_keys("{ENTER}")


    def open_job_by_double_click(self):
        pass
        self.engineering_window.set_focus()  # 激活窗口


    def go_up(self):
        pass
        self.engineering_window.set_focus()  # 激活窗口


    def get_engineering_left_top_Coor(self):
        win_text2 = get_print_control_identifiers_text(self.engineering_window)
        coor_ok = get_coor_of_object('Engineering 1.1.7.2',win_text2)
        return coor_ok


    def getCoor(self,window,wanted_title):
        win_text = get_print_control_identifiers_text(window)
        coor_ok = get_coor_of_object(wanted_title, win_text)
        return coor_ok

    def get_engineering_file_Coor(self,coor_type = 'absolute'):
        x = 20
        y = 40
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)


    def get_engineering_import_Coor(self,coor_type = 'absolute'):
        x = 20
        y = 210
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)