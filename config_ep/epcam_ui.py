import os
import sys
import re
import time
from pathlib import Path

import cv2
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

class Engineering(object):
    def __init__(self):
        self.set_default_ui_para()
        self.engineering_window = RunConfig.driver_epcam_ui.window(**self.engineering_window_para)


    def set_default_ui_para(self):
        pass
        # engineering_window
        self.engineering_window_para = {'title': "Engineering 1.1.7.2"}

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




    # Engineering的方法
    def job_first_is_opened(self):
        pass

        # 截图
        engineering_window_jpg = self.engineering_window.capture_as_image()
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
        img_cut = img[225:307, 46:137]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_job_first.jpg", img_cut)
        cv2.waitKey(0)

        # 加载两张图片
        img_standard = cv2.imread(
            os.path.join(Path(os.path.dirname(__file__)).parent, r'data\pic\engineering\engineering_job_first_opened_standard.jpg'))
        img_current = cv2.imread(r'C:\cc\share\temp\engineering_job_first.jpg')

        # 转换为灰度图像
        gray_a = cv2.cvtColor(img_standard, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(img_current, cv2.COLOR_BGR2GRAY)

        # 计算两张灰度图像的差异
        diff = cv2.absdiff(gray_a, gray_b)

        # 设定差异的阈值，这里使用了一个简单的固定阈值，你可以根据需要进行调整
        threshold = 30
        _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        # 找到差异点的轮廓
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 初始化矩形框计数器
        rectangle_count = 0
        # 自定义矩形框的宽度和高度
        custom_width = 10
        custom_height = 10

        # 在b图上标记差异点
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(img_current, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(img_current, (x, y), (x + custom_width, y + custom_height), (0, 0, 255), 2)
            rectangle_count += 1

        # 输出矩形框的个数
        print(f"矩形框的个数：{rectangle_count}")

        # 保存结果图像
        cv2.imwrite(r'C:\cc\share\temp\diff_with_rectangles.jpg', img_current)

        # 显示结果图像
        # cv2.imshow('Difference Image with Rectangles', img_current)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return rectangle_count == 0

    def close_job_first(self):
        self.engineering_window.click_input(
            coords=self.get_engineering_job_first_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.click_input(button="right", coords=(80,280))
        self.engineering_window.click_input(coords=(80 + 20,280 + 50))
        send_keys("{ENTER}")




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

        # 切换到import job窗口，并点击菜单input path
        engineering_import_window = self.engineering_window.child_window(**self.engineering_import_window_child_window_para)
        engineering_import_window.click_input(coords=self.get_engineering_import_input_path_Coor())# 点击菜单input path





        # 获得选择文件类型控件，并选择ipc2581类型
        engineering_import_input_path_file_type_window=self.engineering_window.child_window(**self.engineering_import_input_path_file_type_window_para)
        engineering_import_input_path_file_type_window.select("ipc2581(*.xml *.cvg)")#根据文本选择下拉列表项

        # 选择文件对象
        engineering_import_input_path_file_path_window=self.engineering_window.child_window(**self.engineering_import_input_path_file_path_window_para)
        engineering_import_input_path_file_path_window.draw_outline(colour = 'red')# 绘制边框以突出显示控件（可以自行指定颜色和宽度）
        engineering_import_input_path_file_path_window.click_input()  # 将焦点设置到控件上
        send_keys(file_path)  # 输入文本

        # 确认选择中的文件
        engineering_import_input_path_confirm_window=self.engineering_window.child_window(**self.engineering_import_input_path_confirm_window_para)
        engineering_import_input_path_confirm_window.click_input()

        # 切换到import job窗口
        engineering_import_window = self.engineering_window.child_window(**self.engineering_import_window_child_window_para)
        engineering_import_window.click_input(coords=self.get_engineering_import_ok_Coor())
        send_keys("{ENTER}")

    def entity_filter(self,job_name):
        pass
        self.engineering_window.click_input(
            coords=self.get_engineering_entity_filter_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        send_keys('^a')
        send_keys('*' + job_name)
        send_keys("{ENTER}")

    def open_job_first_by_double_click(self):
        pass
        # self.engineering_window.set_focus()  # 激活窗口
        self.engineering_window.click_input(
            coords=self.get_engineering_job_first_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.double_click_input(coords=(80, 280))

    def go_up(self):
        pass
        # self.engineering_window.set_focus()  # 激活窗口
        self.engineering_window.click_input(
            coords=self.get_engineering_job_first_Coor(coor_type='relative'))  # 使用鼠标单击按钮，无需主动激活窗口
        self.engineering_window.double_click_input(coords=(80, 280))
        mouse.move(coords=(600,600))






    # 获得坐标

    def getCoor(self,window,wanted_title):
        win_text = get_print_control_identifiers_text(window)
        coor_ok = get_coor_of_object(wanted_title, win_text)
        return coor_ok

    def get_engineering_left_top_Coor(self):
        win_text2 = get_print_control_identifiers_text(self.engineering_window)
        coor_ok = get_coor_of_object('Engineering 1.1.7.2',win_text2)
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

    def get_engineering_import_input_path_Coor(self, coor_type='relative'):
        x = 30
        y = 100  # 变形时，字体太大，异常情况
        y = 80
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_import_ok_Coor(self, coor_type='relative'):
        x = 30
        y = 200#变形时，字体太大，异常情况
        y = 180
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_entity_filter_Coor(self,coor_type = 'absolute'):
        x = 120
        y = 120
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)

    def get_engineering_job_first_Coor(self,coor_type = 'absolute'):
        x = 80
        y = 180
        if coor_type == 'absolute':
            engineering_left_top_Coor = self.get_engineering_left_top_Coor()
            return (engineering_left_top_Coor[0] + x,engineering_left_top_Coor[1] + y)
        if coor_type == 'relative':
            return (x, y)





