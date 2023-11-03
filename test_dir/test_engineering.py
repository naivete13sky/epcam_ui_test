import os
import time
from pathlib import Path
import numpy as np
import pytest
import pytesseract
import rarfile
from pywinauto.keyboard import send_keys, SendKeys
from PIL import Image
from config import RunConfig
from cc.cc_method import GetTestData, PictureMethod
from config_ep import page
import cv2
from config_ep.base.base import Base
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.page_input import PageInput
from config_ep.page.page_graphic import PageGraphic
from config_ep.page.page_tool_size_edit import PageToolSizeEdit
from config_ep.page.page_dcode_edit import PageDcodeEdit
from config_ep.page.page_input_view_ascii import PageInputViewAscii


@pytest.mark.input
class TestUI:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()  # 激活窗口

    def test_ui_all(self, epcam_ui_start):
        engineering_window_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        img_cut = engineering_window_pic.crop((10, 30, 42, 60))  # 截取图像# PIL裁剪坐标是左上右下
        text = pytesseract.image_to_string(img_cut)  # 使用Tesseract进行文字识别
        assert text == 'File\n'
        # 截取图像# PIL裁剪坐标是左上右下。img_cut = img[30:60, 70:120]这种方式颜色有时会有问题。
        img_cut = engineering_window_pic.crop((70, 30, 120, 60))
        text = pytesseract.image_to_string(img_cut)  # 使用Tesseract进行文字识别
        assert text == 'Action\n'

        img_cut = engineering_window_pic.crop((155, 30, 205, 60))
        text = pytesseract.image_to_string(img_cut)  # 使用Tesseract进行文字识别
        assert text == 'Option\n'

    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Engineering'))
    def test_go_up(self, job_id, epcam_ui_start,
                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道用例ID：1505
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        job_org_type = 'ipc2581'
        # 下载料号
        download_file_compressed_entity_filter_delete_all_jobs_import(job_id, job_org_type)  # 调用 fixture 并传递参数值
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.go_up()  # 鼠标点击
        assert self.engineering.job_first_is_opened()

        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.go_up(method='menu')  # 通过菜单action-open
        assert self.engineering.job_first_is_opened()

    def test_option_language(self, epcam_ui_start):
        """
        禅道用例ID：1506
        :param epcam_ui_start:
        :return:
        """
        self.engineering.language_switch(language='Simplified Chinese')
        assert self.engineering.language_is_simplified_chinese()
        self.engineering.language_switch(language='EP Default')

    def test_file_save_no_job_select(self, epcam_ui_start):
        """
        禅道用例ID：3552
        :param epcam_ui_start:
        :return:
        """
        self.engineering.job_list_click_empty()  # 鼠标点击空白处，不选择料号
        self.engineering.file_save()
        engineering_file_save_job_no_select_dialog = RunConfig.driver_epcam_ui.window(
            **page.engineering_file_save_window_para)
        engineering_file_save_job_no_select_jpg = engineering_file_save_job_no_select_dialog.capture_as_image()  # 截图
        # Convert the PIL image to a numpy array,此方法不需要把截图保存到硬盘的。
        img = np.array(engineering_file_save_job_no_select_jpg)
        img_cut = img[35:60, 35:205]  # 后面的是水平方向
        text = pytesseract.image_to_string(img_cut)
        print('text:', text)
        assert text == 'No elements were selected!\n'
        send_keys("{ENTER}")  # 确认关闭弹窗

    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Save'))
    def test_open_job(self, job_id, epcam_ui_start, download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道ID：2479
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号#
        self.engineering.open_job_first_by_context_menu()  # 右击打开料号
        self.engineering.job_list_in_job_click_empty()  # 鼠标指示放到空白处
        engineering_window_job_info = self.engineering.engineering_window.capture_as_image()  # 截图
        img = np.array(engineering_window_job_info)
        x_s, x_e = 30, 830  # x_s,x_e分别是层别列表的x方向开始与结束像素。
        y_s, y_e = 210, 350  # y_s,y_e分别是层别列表的y方向开始与结束像素
        img_cut = img[y_s:y_e, x_s:x_e]  # 后面的是水平方向,file
        # cv2.imshow("Cropped Image", img_cut)
        # cv2.waitKey(0)  # 等待按键按下后关闭图像窗口
        cv2.imwrite(r"C:\cc\share\temp\engineering_window_job_info.png", img_cut)
        # 关闭所有窗口
        # cv2.destroyAllWindows()

        # 使用Tesseract进行文字识别
        text = pytesseract.image_to_string(img_cut)
        # 打印识别出的文本
        print('text:', text)
        assert '(GO Up) matrix steps symbols' in text
        self.engineering.go_up()  # 鼠标点击，返回到了job list界面


class TestFile:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()  # 激活窗口

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Save'))
    def test_file_save_no_changed(self, job_id, epcam_ui_start,
                                  download_file_compressed_entity_filter_delete_all_jobs_import,
                                  graphic_close_engineering_save_first_job):
        """
        禅道用例ID：3553。
        :param epcam_ui_start:
        :return:
        """
        # 调用 fixture 并传递参数值,下载料号#
        download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()  # 双击打开steps
        self.engineering.open_first_step_by_double_click(time_sleep=0.1)  # 打开第1个step
        self.graphic = PageGraphic()
        graphic_close_engineering_save_first_job(job_id)
        engineering_file_save_job_no_changed_dialog = self.engineering.engineering_window.child_window(
            title="Information", control_type="Window")
        engineering_file_save_job_no_changed_dialog = engineering_file_save_job_no_changed_dialog.capture_as_image()
        img = np.array(engineering_file_save_job_no_changed_dialog)
        img_cut = img[35:60, 55:210]  # 后面的是水平方向
        # 使用Tesseract进行文字识别
        text = pytesseract.image_to_string(img_cut)
        # 打印识别出的文本
        print('text:', text)
        assert text in 'Job does not changed !\n'
        send_keys("{ENTER}")  # 确认关闭弹窗

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Save'))
    def test_file_save_job_changed(self, job_id, epcam_ui_start,
                                   download_file_compressed_entity_filter_delete_all_jobs_import,
                                   graphic_close_engineering_save_first_job):
        """
        禅道用例ID：3594、3557。
        :param epcam_ui_start:
        :return:
        """
        # 调用 fixture 并传递参数值,下载料号
        download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()  # 双击打开steps
        self.engineering.open_first_step_by_double_click(time_sleep=0.1)  # 打开第1个step
        self.graphic = PageGraphic()
        graphic_window_pic = self.graphic.graphic_window.capture_as_image()  # 截图
        img = np.array(graphic_window_pic)
        x_s, x_e = 58, 230  # x_s,x_e分别是层别列表的x方向开始与结束像素。
        y_s, y_e = 160, 750  # y_s,y_e分别是层别列表的y方向开始与结束像素
        img_cut = img[y_s:y_e, x_s:x_e]  # 后面的是水平方向,file
        cv2.imwrite(r"C:\cc\share\temp\graphic_window_layers.png", img_cut)
        # 读取图片并进行 OCR
        image = Image.open(r"C:\cc\share\temp\graphic_window_layers.png")  # 打开图像
        image = image.convert('L')  # Convert image to grayscale,# 图像灰度化： 将彩色图像转换为灰度图像可以减少颜色干扰。
        threshold_value = 130  # 阈值化会将图像的像素值映射到两个值之间（例如，黑色和白色）.二值化： 将灰度图像转换为二值图像可以使文字与背景更明显。
        # Apply thresholding to convert gray areas to white
        image = image.point(lambda p: 255 if p > threshold_value else p)
        output_image_path = r'C:\cc\share\temp\graphic_window_layers_for_ocr.png'
        image.save(output_image_path)  # 保存
        target_word = 'smt'
        target_word_coord_percentage = PictureMethod.get_word_pos_of_picture(output_image_path, target_word)
        print('target_word_coord_percentage:', target_word_coord_percentage)
        assert target_word_coord_percentage[0] > -1
        graphic_layer_size = (x_e - x_s, y_e - y_s)  # x,y
        my_coord = (int(graphic_layer_size[0] * target_word_coord_percentage[0]) + x_s + 10,
                    int(graphic_layer_size[1] * target_word_coord_percentage[1]) + y_s)
        self.graphic.graphic_window.click_input(coords=my_coord)  # 点击 smt层
        send_keys('^b')  # 删除层别物件
        send_keys("{ENTER}")
        graphic_close_engineering_save_first_job(job_id)
        engineering_file_save_job_no_changed_dialog = self.engineering.engineering_window.child_window(
            title="Information", control_type="Window")
        engineering_file_save_job_no_changed_dialog = engineering_file_save_job_no_changed_dialog.capture_as_image()
        img = np.array(engineering_file_save_job_no_changed_dialog)
        img_cut = img[35:60, 55:360]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\cc.png", img_cut)
        # 使用Tesseract进行文字识别
        text = pytesseract.image_to_string(img_cut)
        # 打印识别出的文本
        print('text:', text)
        assert 'will be saved, continue?' in text
        send_keys("{ENTER}")  # 确认关闭弹窗

        #  验证用例3557
        send_keys('^y')  # 不选中任何料号
        self.engineering.close_job_first() if self.engineering.job_first_is_opened() else None  # 如果料号是打开状态，要先关闭料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()  # 双击打开steps
        self.engineering.open_first_step_by_double_click(time_sleep=0.1)  # 打开第1个step
        self.graphic = PageGraphic()
        self.graphic.graphic_window.click_input(coords=my_coord)  # 点击 smt层
        graphic_window_dialog = self.graphic.graphic_window.capture_as_image()  # 截个图
        img = np.array(graphic_window_dialog)
        pil_image = Image.fromarray(img)  # 将图像转换为PIL图像对象
        width, height = pil_image.size  # 获取图像尺寸
        img_cut = img[height-35:height-15, 20:235]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\cc.png", img_cut)
        # 使用Tesseract进行文字识别
        text = pytesseract.image_to_string(img_cut)
        # 打印识别出的文本
        print('text:', text)
        assert 'Selected: 0' in text

        self.graphic.close()  # 关闭Graphic窗口
        self.engineering.go_up()  # 鼠标点击
        self.engineering.go_up()  # 鼠标点击，返回到了job list界面

    # @pytest.mark.skip
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Save'))
    def test_file_close(self, job_id, epcam_ui_start,
                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道用例ID：4076。
        :param epcam_ui_start:
        :return:
        """
        download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.file_close()  # File-close关闭料号
        time.sleep(1)
        send_keys("{ENTER}")  # 确认关闭弹窗
        assert self.engineering.job_first_is_closed()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_clear(self, job_id, epcam_ui_start):
        """
        禅道用例ID：4054
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        # 下载料号
        job_name, file_compressed_path = Base.get_file_compressed_job_name_by_job_id_from_dms(job_id)
        # 解压rar
        rf = rarfile.RarFile(file_compressed_path)
        rf.extractall(Path(file_compressed_path).parent)
        # 删除压缩包
        os.remove(file_compressed_path) if os.path.exists(file_compressed_path) else None

        self.engineering.entity_filter('760')  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除筛选出的料号
        self.input_job = PageInput()
        # file_path = os.path.join(Path(file_compressed_path).parent,os.listdir(Path(file_compressed_path).parent)[0])
        file_path = str(Path(file_compressed_path).parent)
        self.input_job.set_path(file_path)  # 选择料号路径
        self.input_job.set_new_job_name('760')
        self.input_job.set_new_step_name('orig')
        self.input_job.identify()
        self.input_job.translate(time_sleep=0.2)
        self.input_job.clear()
        assert self.input_job.is_all_file_cleared()
        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_select_all(self, job_id, epcam_ui_start):
        """
        禅道用例ID：4053
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        # 下载料号
        job_name, file_compressed_path = Base.get_file_compressed_job_name_by_job_id_from_dms(job_id)
        # 解压rar
        rf = rarfile.RarFile(file_compressed_path)
        rf.extractall(Path(file_compressed_path).parent)
        # 删除压缩包
        os.remove(file_compressed_path) if os.path.exists(file_compressed_path) else None
        self.engineering.entity_filter('760')  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除筛选出的料号
        self.input_job = PageInput()
        file_path = str(Path(file_compressed_path).parent)
        self.input_job.set_path(file_path)  # 选择料号路径
        self.input_job.set_new_job_name('760')
        self.input_job.set_new_step_name('orig')
        self.input_job.identify()
        self.input_job.translate(time_sleep=0.2)
        self.input_job.unselect_file()
        self.input_job.unselect_file(index=2)
        self.input_job.select_all()
        assert self.input_job.is_selected_all()
        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_tool_size_close(self, job_id, epcam_ui_start):
        """
        禅道用例ID：4052,4051
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        # 下载料号
        job_name, file_compressed_path = Base.get_file_compressed_job_name_by_job_id_from_dms(job_id)
        # 解压rar
        rf = rarfile.RarFile(file_compressed_path)
        rf.extractall(Path(file_compressed_path).parent)
        # 删除压缩包
        os.remove(file_compressed_path) if os.path.exists(file_compressed_path) else None
        self.engineering.entity_filter('760')  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除筛选出的料号
        self.input_job = PageInput()
        file_path = str(Path(file_compressed_path).parent)
        self.input_job.set_path(file_path)  # 选择料号路径
        self.input_job.set_new_job_name('760')
        self.input_job.set_new_step_name('orig')
        self.input_job.identify()
        self.input_job.translate(time_sleep=0.2)
        self.input_job.tool_size_edit_open()
        self.tool_size_edit = PageToolSizeEdit()
        assert self.tool_size_edit.is_right()
        self.tool_size_edit.close()
        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_dcode_edit_close(self, job_id, epcam_ui_start):
        """
        禅道用例ID：4050,4049
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        # 下载料号
        job_name, file_compressed_path = Base.get_file_compressed_job_name_by_job_id_from_dms(job_id)
        # 解压rar
        rf = rarfile.RarFile(file_compressed_path)
        rf.extractall(Path(file_compressed_path).parent)
        # 删除压缩包
        os.remove(file_compressed_path) if os.path.exists(file_compressed_path) else None
        self.engineering.entity_filter('760')  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除筛选出的料号
        self.input_job = PageInput()
        file_path = str(Path(file_compressed_path).parent)
        self.input_job.set_path(file_path)  # 选择料号路径
        self.input_job.set_new_job_name('760')
        self.input_job.set_new_step_name('orig')
        self.input_job.identify()
        self.input_job.translate(time_sleep=0.2)
        self.input_job.dcode_edit_open()
        self.dcode_edit = PageDcodeEdit()
        assert self.dcode_edit.is_right()
        self.dcode_edit.close()
        self.input_job.close()

    @pytest.mark.coding
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_view_ascii_close(self, job_id, epcam_ui_start):
        """
        禅道用例ID：4045,4046
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        # # 下载料号
        # job_name, file_compressed_path = Base.get_file_compressed_job_name_by_job_id_from_dms(job_id)
        # # 解压rar
        # rf = rarfile.RarFile(file_compressed_path)
        # rf.extractall(Path(file_compressed_path).parent)
        # # 删除压缩包
        # os.remove(file_compressed_path) if os.path.exists(file_compressed_path) else None
        # self.engineering.entity_filter('760')  # 筛选料号，在界面上显示指定某一个料号
        # if self.engineering.job_first_is_opened():
        #     self.engineering.close_job_first()
        # self.engineering.delete_all_jobs()  # 删除筛选出的料号
        self.input_job = PageInput()
        # file_path = str(Path(file_compressed_path).parent)
        # self.input_job.set_path(file_path)  # 选择料号路径
        # self.input_job.set_new_job_name('760')
        # self.input_job.set_new_step_name('orig')
        # self.input_job.identify()
        # self.input_job.translate(time_sleep=0.2)
        self.input_job.view_ascii_open()
        self.view_ascii = PageInputViewAscii()
        assert self.view_ascii.is_right()
        self.view_ascii.minimize()
        self.view_ascii.maximize()
        self.view_ascii.scroll()
        # self.view_ascii.close()
        # self.input_job.close()
