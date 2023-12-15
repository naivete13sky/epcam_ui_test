import os
import time
from pathlib import Path
import numpy as np
import pytest
import pytesseract
import rarfile
from pywinauto.keyboard import send_keys
from PIL import Image
from config import RunConfig
from cc.cc_method import GetTestData, PictureMethod, opencv_compare
from config_ep import page
import cv2
from config_ep.base.base import Base, MyODB
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.page_input import PageInput
from config_ep.page.page_graphic import PageGraphic
from config_ep.page.page_tool_size_edit import PageToolSizeEdit
from config_ep.page.page_dcode_edit import PageDcodeEdit
from config_ep.page.page_input_view_ascii import PageInputViewAscii
from config_ep.page.page_engineering_file import PageFile


@pytest.mark.input
class TestUI:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.engineering = PageEngineering()
        self.file = PageFile()
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

    def test_open_file_menu(self, epcam_ui_start):
        self.engineering.engineering_window.click_input(coords=page.engineering_file_coord)  # 单击打开File菜单
        engineering_file_menu_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_file_menu_pic.save(r'C:\cc\share\temp\engineering_file_menu_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_menu_pic.png')
        img_cut = img[25:315, 8:190]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_menu_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_menu_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_file_menu_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.engineering.job_list_click_empty()  # 鼠标点击空白处，不影响下一个用例

    def test_open_close_create_window(self, epcam_ui_start):
        self.file.open_create_window()
        time.sleep(0.2)
        engineering_file_create_window_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_file_create_window_pic.save(r'C:\cc\share\temp\engineering_file_create_window_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_window_pic.png')
        img_cut = img[50:780, 380:455]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_window_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_window_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_file_create_window_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('x')
        assert self.file.create_window_is_closed()

    def test_create_entity_input(self, epcam_ui_start):
        self.file.open_create_window()
        self.file.clear_entity_name()
        self.file.entity_name_input()
        engineering_file_create_entity_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_file_create_entity_pic.save(r'C:\cc\share\temp\engineering_file_create_entity_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_entity_pic.png')
        img_cut = img[50:780, 460:666]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_entity_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_entity_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_file_create_entity_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('x')

    def test_create_entity_illegal_input(self, epcam_ui_start):
        self.file.open_create_window()
        self.file.clear_entity_name()
        self.file.entity_name_illegal_input()
        engineering_file_create_entity_illegal_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_file_create_entity_illegal_pic.save(
            r'C:\cc\share\temp\engineering_file_create_entity_illegal_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_entity_illegal_pic.png')
        img_cut = img[50:780, 460:666]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_entity_illegal_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_entity_illegal_pic_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_create_entity_illegal_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('x')

    def test_create_database_reset(self, epcam_ui_start):
        self.file.open_create_window()
        self.file.clear_entity_name()
        self.file.database_input_reset()
        engineering_file_create_database_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_file_create_database_pic.save(
            r'C:\cc\share\temp\engineering_file_create_database_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_database_pic.png')
        img_cut = img[50:780, 460:666]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_database_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_database_pic_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_create_database_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('x')

    def test_create_new_job_ok(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.file.open_create_window()
        self.file.clear_entity_name()
        self.file.create_job('760', 'ok')
        engineering_file_create_new_job_ok_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_file_create_new_job_ok_pic.save(
            r'C:\cc\share\temp\engineering_file_create_new_job_ok_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_new_job_ok_pic.png')
        img_cut = img[88:780, 25:800]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_new_job_ok_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_new_job_ok_pic_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_create_new_job_ok_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('close')

    def test_create_new_job_apply(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.file.open_create_window()
        self.file.clear_entity_name()
        self.file.create_job('760', 'apply')
        engineering_file_create_new_job_apply_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_file_create_new_job_apply_pic.save(
            r'C:\cc\share\temp\engineering_file_create_new_job_apply_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_new_job_apply_pic.png')
        img_cut = img[88:780, 25:455]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_new_job_apply_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_new_job_apply_pic_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_create_new_job_apply_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('close')

    def test_create_exist_job(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.file.open_create_window()
        self.file.create_job('760', 'apply')
        self.file.create_job('760', 'apply')
        self.file.create_job('760', 'ok')
        engineering_file_create_exist_job_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_file_create_exist_job_pic.save(
            r'C:\cc\share\temp\engineering_file_create_exist_job_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_exist_job_pic.png')
        img_cut = img[88:780, 25:855]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_exist_job_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_exist_job_pic_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_create_exist_job_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('close')

    def test_create_job_entity_none(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.file.open_create_window()
        self.file.clear_entity_name()
        self.file.engineering_window.click_input(coords=page.engineering_file_create_apply_button_coord)
        engineering_file_create_job_database_none_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_file_create_job_database_none_pic.save(
            r'C:\cc\share\temp\engineering_file_create_job_entity_none_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_job_entity_none_pic.png')
        img_cut = img[88:780, 25:855]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_job_entity_none_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_job_entity_none_pic_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_create_job_entity_none_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('close')
        self.file.close_create_window('close')

    def test_create_job_database_none(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.file.open_create_window()
        self.file.clear_entity_name()
        self.file.entity_name_input()
        self.file.clear_database_name()
        self.file.engineering_window.click_input(coords=page.engineering_file_create_apply_button_coord)
        engineering_file_create_job_database_none_pic = self.engineering.engineering_window.capture_as_image()
        engineering_file_create_job_database_none_pic.save(
            r'C:\cc\share\temp\engineering_file_create_job_database_none_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_job_database_none_pic.png')
        img_cut = img[88:780, 25:855]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_job_database_none_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_job_database_none_pic_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_create_job_database_none_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('close')
        self.file.close_create_window('close')

    def test_create_job_database_not_exist(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.file.open_create_window()
        self.file.clear_entity_name()
        self.file.entity_name_input()
        self.file.database_input()
        self.file.engineering_window.click_input(coords=page.engineering_file_create_apply_button_coord)
        engineering_file_create_job_database_not_exist_pic = self.engineering.engineering_window.capture_as_image()
        engineering_file_create_job_database_not_exist_pic.save(
            r'C:\cc\share\temp\engineering_file_create_job_database_not_exist_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_create_job_database_not_exist_pic.png')
        img_cut = img[88:780, 25:855]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_create_job_database_not_exist_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_file_create_job_database_not_exist_pic_cut_standard'
                                         r'.png')
        img_current_path = r'C:\cc\share\temp\engineering_file_create_job_database_not_exist_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.file.close_create_window('close')
        self.file.close_create_window('close')

    def test_open_option_menu(self, epcam_ui_start):  # 验证打开Option菜单栏
        """
        禅道用例ID：3970、3971
        :param epcam_ui_start:
        :return:
        """
        self.engineering.engineering_window.click_input(coords=page.engineering_option_coord)  # 单击打开Option菜单
        self.engineering.engineering_window.click_input(coords=page.engineering_option_language_coord)
        time.sleep(0.3)  # 单击打开language子菜单
        engineering_option_menu_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_option_menu_pic.save(r'C:\cc\share\temp\engineering_option_menu_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_option_menu_pic.png')
        img_cut = img[25:173, 150:570]  # 前纵后横（A:B,C:D，A裁剪的越多，数值越大，B裁剪的越多，数值越小；CD一样的说法）
        cv2.imwrite(r"C:\cc\share\temp\engineering_option_menu_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_option_menu_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_option_menu_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.engineering.job_list_click_empty()  # 鼠标点击空白处，不影响下一个用例

    def test_open_close_about_us_window(self, epcam_ui_start):      # 验证打开、关闭About_Us弹窗
        """
        禅道用例ID：3975、3976
        :param epcam_ui_start:
        :return:
        """
        self.engineering.engineering_window.click_input(coords=page.engineering_option_coord)  # 单击打开Option菜单
        # time.sleep(0.4)
        self.engineering.engineering_window.click_input(coords=page.engineering_option_About_Us_coord)
        time.sleep(0.3)      # 单机打开About_Us窗口
        engineering_option_about_us_window_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_option_about_us_window_pic.save(r'C:\cc\share\temp\engineering_option_about_us_window_pic.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_option_about_us_window_pic.png')
        img_cut = img[360:580, 460:620]  # 前纵后横（A:B,C:D，A裁剪的越多，数值越大，B裁剪的越多，数值越小；CD一样的说法）
        cv2.imwrite(r"C:\cc\share\temp\engineering_option_about_us_window_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_option_about_us_window_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_option_about_us_window_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.engineering.engineering_window.click_input(coords=page.engineering_option_close_About_Us_coord)  # 关闭窗口

    def test_open_action_menu(self, epcam_ui_start):      # 验证打开action菜单栏
        """
        禅道用例ID：3944、3945
        :param epcam_ui_start:
        :return:
        """
        self.engineering.engineering_window.click_input(coords=page.engineering_action_coord)  # 单击打开Option菜单
        self.engineering.engineering_window.click_input(coords=page.engineering_action_select_coord)  # 单击打开language子菜单
        time.sleep(0.3)
        engineering_option_menu_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_option_menu_pic.save(r'C:\cc\share\temp\engineering_action_menu_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_action_menu_pic.png')
        img_cut = img[25:173, 8:470]  # 前纵后横（A:B,C:D，A裁剪的越多，数值越大，B裁剪的越多，数值越小；CD一样的说法）
        cv2.imwrite(r"C:\cc\share\temp\engineering_action_menu_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_action_menu_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_action_menu_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.engineering.job_list_click_empty()  # 鼠标点击空白处，不影响下一个用例

    def test_file_output_open(self, epcam_ui_start):
        """
        禅道用例ID：3726。
        DMS_ID：
        :param epcam_ui_start:
        :return:
        """
        # download_file_compressed_entity_filter_delete_all_jobs_import(job_id)# 调用 fixture 并传递参数值,下载料号
        self.engineering.engineering_window.click_input(coords=page.engineering_file_coord)
        self.engineering.engineering_window.click_input(coords=page.engineering_file_output_coord)
        time.sleep(0.3)
        engineering_output_open_window_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_output_open_window_pic.save(
            r'C:\cc\share\temp\engineering_output_open_window_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_output_open_window_pic.png')
        img_cut = img[35:760, 145:890]  # 前纵后横（A:B,C:D，A裁剪的越多，数值越大，B裁剪的越多，数值越小；CD一样的说法）
        cv2.imwrite(r"C:\cc\share\temp\engineering_output_open_window_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_output_open_window_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_output_open_window_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))      # 验证input导入多个料号全部选中、取消
    def test_action_select_all(self, job_id, epcam_ui_start):
        """
        禅道用例ID：3946、3952
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        for i in range(3):
            # 下载料号
            job_name, file_compressed_path = Base.get_file_compressed_job_name_by_job_id_from_dms(job_id)
            # 解压rar
            rf = rarfile.RarFile(file_compressed_path)
            rf.extractall(Path(file_compressed_path).parent)
            # 删除压缩包
            os.remove(file_compressed_path) if os.path.exists(file_compressed_path) else None
            self.engineering.entity_filter('760*')  # 筛选料号，在界面上显示指定某一个料号
            self.input_job = PageInput()
            file_path = str(Path(file_compressed_path).parent)
            self.input_job.set_path(file_path)  # 选择料号路径
            self.input_job.set_new_job_name(f'760_{i}')  # 使用索引来生成不同的料号名称
            self.input_job.set_new_step_name('orig')
            self.input_job.identify()
            self.input_job.translate(time_sleep=0.2)
            self.input_job.close()
        self.engineering.engineering_window.click_input(coords=page.engineering_action_coord)
        self.engineering.engineering_window.click_input(coords=page.engineering_action_select_coord)
        self.engineering.engineering_window.click_input(coords=page.engineering_action_select_select_all_coord)
        time.sleep(0.3)
        engineering_action_select_all_window_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_action_select_all_window_pic.save(r'C:\cc\share\temp\engineering_action_select_all_window_pic.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_action_select_all_window_pic.png')
        img_cut = img[5:822, 9:780]  # 前纵后横（A:B,C:D，A裁剪的越多，数值越大，B裁剪的越多，数值越小；CD一样的说法）
        cv2.imwrite(r"C:\cc\share\temp\engineering_action_select_all_window_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_action_select_all_window_pic_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\engineering_action_select_all_window_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.engineering.engineering_window.click_input(coords=page.engineering_action_coord)
        self.engineering.engineering_window.click_input(coords=page.engineering_action_select_coord)
        self.engineering.engineering_window.click_input(coords=page.engineering_action_select_unselect_all_coord)

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

    @pytest.mark.zjr
    @pytest.mark.engineering
    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Open_Job'))
    def test_open_step_case_4648(self, job_id, epcam_ui_start,
                           download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道bug ID: 1305 验证打开pcs软件不闪退（影响版本号：beta_2.28.054_s16）
        测试用例ID：4648
        :param job_id:44120
        :param epcam_ui_start:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()  # 双击打开steps
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'pcs')  # 双击打开panel
        self.graphic = PageGraphic()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()


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
        禅道用例ID：4045,4046,4047
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
        self.input_job.view_ascii_open()
        self.view_ascii = PageInputViewAscii()
        assert self.view_ascii.is_right()
        self.view_ascii.minimize()
        self.view_ascii.maximize()

        self.view_ascii.scroll_y(y_pixel=10)
        input_view_ascii_window_scroll_y = self.view_ascii.engineering_input_view_ascii_window.capture_as_image()# 截图
        input_view_ascii_window_scroll_y.save(r'C:\cc\share\temp\input_view_ascii_window_scroll_y.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\input_view_ascii_window_scroll_y.png')
        img_cut = img[5:822, 8:1005]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\input_view_ascii_window_scroll_y_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\input_view_ascii_window_scroll_y_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\input_view_ascii_window_scroll_y_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0

        self.view_ascii.close()
        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_parameters(self, job_id, epcam_ui_start):
        """
        禅道用例ID：4036  Parameters视窗展示正确
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
        self.input_job.engineering_input_window.click_input(
            button='right', coords=(page.engineering_file_parameters_coord))
        self.input_job.engineering_input_window.click_input(
            coords=(page.engineering_file_parameters_menu_coord))
        send_keys("{TAB}")  # 按下TAB键，挪动光标位置

        engineering_input_parameters_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_input_parameters_pic.save(r'C:\cc\share\temp\engineering_input_parameters_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_input_parameters_pic.png')
        img_cut = img[370:800, 480:800]  # 前纵后横
        cv2.imwrite(r"C:\cc\share\temp\engineering_input_parameters_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_input_parameters_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_input_parameters_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0

        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_view_graphic(self, job_id, epcam_ui_start):

        """
        禅道用例ID：4029  验证View Graphic视窗展示正确
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
        self.input_job.engineering_input_window.click_input(
            button='right', coords=(page.engineering_file_input_view_graphic_coord))  # 右击层别栏
        self.input_job.engineering_input_window.click_input(
            coords=(page.engineering_file_input_view_graphic_menu_coord))

        engineering_input_view_graphic_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_input_view_graphic_pic.save(r'C:\cc\share\temp\engineering_input_view_graphic_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_input_view_graphic_pic.png')
        img_cut = img[150:650, 208:825]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_input_view_graphic_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_input_view_graphic_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_input_view_graphic_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0

        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_right_click_menu(self, job_id, epcam_ui_start):

        """
        禅道用例ID：4643 验证右击菜单栏展示正确展示正确
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
        self.input_job.engineering_input_window.click_input(
            button='right', coords=(page.engineering_file_input_right_click_menu_coord))  # 右击层别栏

        engineering_input_view_graphic_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_input_view_graphic_pic.save(r'C:\cc\share\temp\engineering_input_right_click_menu_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_input_right_click_menu_pic.png')
        img_cut = img[368:562, 425:510]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_input_right_click_menu_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_input_right_click_menu_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_input_right_click_menu_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.engineering.job_list_click_empty()  # 鼠标点击空白处，不影响下一个用例

        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_job_window_close(self, job_id, epcam_ui_start):

        """
        禅道用例ID：3989 验证Job视窗展示正确、3990 已有Job会全部展示在Job视窗中、3991 Job视窗可正确关闭
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
        self.input_job.engineering_input_window.click_input(
            coords=(page.engineering_file_input_job_window_menu_coord))  # 左击Input视窗的Job按钮
        send_keys("{TAB}")  # 按下TAB键，挪动光标位置

        engineering_input_view_graphic_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_input_view_graphic_pic.save(r'C:\cc\share\temp\engineering_input_job_window_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_input_job_window_pic.png')
        img_cut = img[375:678, 470:750]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_input_job_window_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_input_job_window_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_input_job_window_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0

        self.input_job.close_job_window()
        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_step_window_close(self, job_id, epcam_ui_start):

        """
        禅道用例ID：4003 step视窗展示正确、34007 step视窗可正确关闭
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
        self.input_job.set_new_step_name('net')
        self.input_job.set_new_step_name('pre')#多创建几个step，方便step市场展示
        self.input_job.identify()
        self.input_job.translate(time_sleep=0.2)
        self.input_job.engineering_input_window.click_input(
            coords=(page.engineering_file_input_step_window_menu_coord))  # 左击Input视窗的step按钮
        send_keys("{TAB}")  # 按下TAB键，挪动光标位置

        engineering_input_view_graphic_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_input_view_graphic_pic.save(r'C:\cc\share\temp\engineering_input_step_window_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_input_step_window_pic.png')
        img_cut = img[375:678, 470:750]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_input_step_window_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_input_step_window_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_input_step_window_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0

        self.input_job.close_step_window()#关闭step视窗
        self.input_job.close()



    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Symbols'))
    def test_symbols_open(self, job_id, epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):

        """
        禅道用例ID：4647 正确打开附件资料的Symbol库
        :param job_id:44119
        :param epcam_ui_start:
        :return:
        """
        download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)  # 调用 fixture 并传递参数值,下载料号
        time.sleep(30)#资料比较大，等待30s

        self.engineering.open_job_first_by_double_click()  # 双击打开测试料号
        self.engineering.engineering_window.double_click_input(coords=page.engineering_inJob_symbols_coord)  #双击打开symbol库
        self.engineering.go_up() #双击go up按钮返回到上一级
        self.engineering.go_up() #再双击go up按钮到软件主界面
        self.engineering.entity_filter('2344473c_58Te6ao')  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除料,不影响后续用例的执行


    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id("Input_Crash"))
    def test_file_input_case_4671(self, job_id, epcam_ui_start):
        """
        验证input附件资料，软件不闪退
        用例ID：4671
        BUG_ID：4451
        :param job_id:44169
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

        self.engineering.entity_filter(job_name)  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除筛选出的料号
        self.input_job = PageInput()
        # file_path = os.path.join(Path(file_compressed_path).parent,os.listdir(Path(file_compressed_path).parent)[0])
        file_path = str(Path(file_compressed_path).parent)
        self.input_job.set_path(file_path)  # 选择料号路径
        self.input_job.set_new_job_name(job_name)
        self.input_job.set_new_step_name('orig')
        self.input_job.identify()
        self.input_job.translate(time_sleep=0.2)
        self.input_job.close()

    def test_cc(self,epcam_ui_start):
        pass

