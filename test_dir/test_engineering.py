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
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.matrix.page_matrix import PageMatrix
from config_ep.page.page_tool_size_edit import PageToolSizeEdit
from config_ep.page.page_dcode_edit import PageDcodeEdit
from config_ep.page.page_input_view_ascii import PageInputViewAscii
from config_ep.page.page_create import PageCreate
from config_ep.page.page_input_parameters import PageInputParameters
from config_ep.page.page_view_graphic import PageViewGraphic
from config_ep.page.page_input_jobs import PageInputJobs
from config_ep.page.page_input_steps import PageInputSteps


@pytest.mark.input
class TestUI:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.engineering = PageEngineering()
        self.create = PageCreate()
        self.engineering.engineering_window.set_focus()  # 激活窗口
        self.matrix = PageMatrix()

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
        self.engineering.open_create_window()
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
        self.create.close()
        assert self.create.create_window_is_closed()

    def test_create_entity_input(self, epcam_ui_start):
        self.engineering.open_create_window()
        self.create.clear_entity_name()
        self.create.entity_name_input('666abc-+{_}+{+}')
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
        self.create.close()

    def test_create_entity_illegal_input(self, epcam_ui_start):
        self.engineering.open_create_window()
        self.create.clear_entity_name()
        self.create.entity_name_input('ABC!@#$你瞅啥？')
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
        self.create.close()

    def test_create_database_reset(self, epcam_ui_start):
        self.engineering.open_create_window()
        self.create.clear_entity_name()
        self.create.clear_database_name()
        self.create.database_reset()
        self.create.database_input('666abc-+{_}+{+}ABC!@#$你说啥？')
        self.create.database_reset()
        self.engineering.job_list_click_empty()  # 鼠标点击空白处
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
        self.create.close()

    def test_create_new_job_ok(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.engineering.open_create_window()
        self.create.clear_entity_name()
        self.create.create_job('760', 'ok')
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

    def test_create_new_job_apply(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.engineering.open_create_window()
        self.create.clear_entity_name()
        self.create.create_job('760', 'apply')
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

    def test_create_exist_job(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.engineering.open_create_window()
        self.create.create_job('760', 'apply')
        self.engineering.open_create_window()
        self.create.create_job('760', 'apply', 'True')
        self.engineering.open_create_window()
        self.create.create_job('760', 'ok', 'True')
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

    def test_create_job_entity_none(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.engineering.open_create_window()
        self.create.clear_entity_name()
        self.create.create_window.click_input(coords=page.create_apply_button_coord)
        time.sleep(0.2)
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
        self.create.click_information_ok_button()
        self.create.close()

    def test_create_job_database_none(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.engineering.open_create_window()
        self.create.clear_entity_name()
        self.create.entity_name_input('666abc-+{_}+{+}')
        self.create.clear_database_name()
        self.create.create_window.click_input(coords=page.create_apply_button_coord)
        time.sleep(0.2)
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
        self.create.click_information_ok_button()
        self.create.close()

    def test_create_job_database_not_exist(self, epcam_ui_start):
        self.engineering.entity_filter('760')
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()
        self.engineering.open_create_window()
        self.create.clear_entity_name()
        self.create.entity_name_input('666abc-+{_}+{+}')
        self.create.database_input('123')
        self.create.create_window.click_input(coords=page.create_apply_button_coord)
        time.sleep(0.2)
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
        self.create.click_information_ok_button()
        self.create.close()

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

    def test_file_output_open_close_3726(self, epcam_ui_start):
        """
        禅道用例ID：3726、3727
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
        self.engineering.engineering_window.click_input(coords=page.engineering_file_output_close_coord)

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

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Symbols_open'))
    def test_engineering_symbols_open_case_4647(self, job_id, epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):

        """
        禅道用例ID：4647 正确打开附件资料的Symbol库
        禅道bugID：2724
        :param job_id:44119
        :param epcam_ui_start:
        :return:
        """
        download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)  # 调用 fixture 并传递参数值,下载料号
        time.sleep(30)  # 资料比较大，等待30s

        self.engineering.open_job_first_by_double_click()  # 双击打开测试料号
        self.engineering.double_click_symbols()#双击料号库按钮将其打开
        self.engineering.go_up()  # 双击go up按钮返回到上一级
        self.engineering.go_up()  # 再双击go up按钮到软件主界面

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Symbols_Click_on_the_slider'))
    def test_engineering_symbols_Click_on_the_slider_case_4731(self, job_id, epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):

        """
        打开资料的symbols库界面，可正确上下滑动页面软件不闪退
        禅道bugID：3493
        :param job_id:44119
        :param epcam_ui_start:
        :return:
        """
        download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)  # 调用 fixture 并传递参数值,下载料号

        self.engineering.open_job_first_by_double_click()  # 双击打开测试料号
        self.engineering.double_click_symbols() # 双击symbol图形

        self.engineering.engineering_window.click_input(coords=page.engineering_inJob_symbol_Left_clickon1_coord)
        self.engineering.engineering_window.click_input(coords=page.engineering_inJob_symbol_Left_clickon2_coord)

        self.engineering.go_up()  # 双击go up按钮返回到上一级
        self.engineering.go_up()  # 双击go up按钮到软件主界面
        self.engineering.entity_filter('2344473c1')  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除料,不影响后续用例的执行

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Close_Job'))
    def test_engineering_Close_Job_case_4654(self, job_id, epcam_ui_start,
                                             download_file_compressed_entity_filter_delete_all_jobs_import):

        """
        禅道用例ID：4654  打开matrix视窗后可正确关闭料号，软件不闪退
        禅道bugID：2307
        :param job_id:44122
        :param epcam_ui_start:
        :return:
        """
        download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)  # 调用 fixture 并传递参数值,下载料号

        self.engineering.open_job_first_by_double_click()  # 双击打开测试料号
        self.engineering.open_matrix_by_double_click()  # 双击Matrix,打开Matrix窗口
        self.matrix.close() #关闭matrix视窗
        self.engineering.go_up()  # 再双击go up按钮到软件主界面

        self.engineering.close_job_first()#关闭该料，预期不闪退

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Copy_step_Close_job'))
    def test_engineering_copy_step_close_job_case_4759(self, job_id, epcam_ui_start,
                                             download_file_compressed_entity_filter_delete_all_jobs_import):

        """
        matrix界面copy step后不保存直接close该料，软件不自动保存复制的step
        禅道bugID：2528
        :param job_id:44122
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_matrix_by_double_click()  # 双击Matrix,打开Matrix窗口

        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 得到odb的matrix文件路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)

        self.matrix.click_step(job_info, 'orig')  # 单击step
        send_keys('^c')
        self.matrix.click_step(job_info, 'orig')  # 再次单击将step复制到指定位置
        self.matrix.step_list_in_step_click_empty()  # 鼠标指示放到空白处，方便后面截图

        matrix_window_step_first_pic = self.matrix.matrix_window.capture_as_image()  # 截图
        img = np.array(matrix_window_step_first_pic)
        img_cut = img[140:185, 190:286]  # 后面的是水平方向
        text = pytesseract.image_to_string(img_cut)  # 使用Tesseract进行文字识别
        print('text:', text)  # 打印识别出的文本
        assert text in 'orig+1\n'

        self.matrix.close()  # 关闭matrix视窗
        self.engineering.go_up()  # 再双击go up按钮到软件主界面
        self.engineering.close_job_first()  # 不保存，关闭该料

        self.engineering.open_job_first_by_double_click()  # 再次双击打开料号
        self.engineering.open_matrix_by_double_click()  # 再次双击Matrix,打开Matrix窗口

        matrix_window_step_first_pic = self.matrix.matrix_window.capture_as_image()  # 截图
        img = np.array(matrix_window_step_first_pic)
        img_cut = img[140:185, 190:286]  # 后面的是水平方向
        text = pytesseract.image_to_string(img_cut)  # 使用Tesseract进行文字识别
        print('text:', text)  # 打印识别出的文本
        assert text in 'orig\n'
        # 预期在相同位置截图时，step名称为原始名称：orig，则证明copy step后不保存直接close该料，软件不自动保存复制的step

        self.matrix.close()  # 关闭matrix视窗
        self.engineering.go_up()  # 再双击go up按钮到软件主界面
        self.engineering.close_job_first()  # 关闭该料

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Steps_right_click_delete'))
    def test_engineering_steps_right_click_delete_case_4752(self, job_id, epcam_ui_start,
                                             download_file_compressed_entity_filter_delete_all_jobs_import):

        """
        steps界面下，使用右击/delete功能删除从左往右的最后一个step软件不闪退
        禅道bugID：5271
        :param job_id:29620
        :param epcam_ui_start:
        :return:
        """
        download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)  # 调用 fixture 并传递参数值,下载料号

        self.engineering.open_job_first_by_double_click()  # 双击打开测试料号
        self.engineering.open_steps_by_double_click()  # 双击打开steps
        self.engineering.in_job_steps_delete_step_first()  # 删除第一个step

        self.engineering.go_up()
        self.engineering.go_up()  # 双击两次go up按钮到软件主界面


class TestFile:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.engineering = PageEngineering()
        self.matrix = PageMatrix()
        self.engineering.engineering_window.set_focus()  # 激活窗口
        self.input_parameters = PageInputParameters()
        self.input_view_graphic = PageViewGraphic()
        self.input_jobs_window = PageInputJobs()
        self.input_steps_window = PageInputSteps()
        self.input_job = PageInput()

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
        input_view_ascii_window_scroll_y = self.view_ascii.engineering_input_view_ascii_window.capture_as_image()  # 截图
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
        :param job_id:268
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
        self.input_job.engineering_input_window.click_input(button='right', coords=(
            page.engineering_file_input_right_click_menu_coord))#打开右击菜单栏
        self.input_job.engineering_input_window.click_input(coords=(
            page.engineering_file_parameters_open_menu_coord))#打开parameters视窗
        send_keys("{TAB}")  # 按下TAB键，挪动光标位置

        img_name = 'engineering_input_parameters_window'
        img_path = self.input_parameters.capture_image(img_name)

        cut_coords = [5, 520, 8, 335] # 后面的是水平方向
        save_path_cut = self.input_parameters.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "engineering\\" + img_name + "_cut_standard.png"
        assert self.input_parameters.is_right(save_path_cut, img_standard_str)

        self.input_parameters.close()
        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_view_graphic(self, job_id, epcam_ui_start):

        """
        禅道用例ID：4029  验证View Graphic视窗展示正确
        :param job_id:268
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
        self.input_job.engineering_input_window.click_input(button='right', coords=(
            page.engineering_file_input_right_click_menu_coord))  # 右击层别栏
        self.input_job.engineering_input_window.click_input(coords=(
            page.engineering_file_input_view_graphic_menu_coord)) #打开view_graphic视窗

        img_name = 'engineering_input_view_graphic_window'
        img_path = self.input_view_graphic.capture_image(img_name)

        cut_coords = [5, 480, 8, 650]  # 后面的是水平方向
        save_path_cut = self.input_view_graphic.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "engineering\\" + img_name + "_cut_standard.png"
        assert self.input_view_graphic.is_right(save_path_cut, img_standard_str)

        self.input_view_graphic.close()
        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_right_click_window(self, job_id, epcam_ui_start):

        """
        禅道用例ID：4643 验证右击菜单栏展示正确展示正确
        :param job_id:268
        :param epcam_ui_start:
        :return:
        """
        #下载料号
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
        self.input_job.translate(time_sleep=1)
        self.input_job.engineering_input_window.click_input(button='right', coords=(
            page.engineering_file_input_right_click_menu_coord))  # 右击层别栏

        engineering_input_right_click_window_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_input_right_click_window_pic.save(r'C:\cc\share\temp\engineering_input_right_click_window_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_input_right_click_window_pic.png')
        img_cut = img[359:555, 369:475]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_input_right_click_window_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_input_right_click_window_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_input_right_click_window_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0

        self.engineering.job_list_click_empty()  # 鼠标点击空白处，不影响下一个用例
        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_jobs_window_open_close(self, job_id, epcam_ui_start):

        """
        禅道用例ID：3989 验证Job视窗展示正确、3990 已有Job会全部展示在Job视窗中、3991 Job视窗可正确关闭
        :param job_id:268
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
        self.input_job.translate(time_sleep=1)
        self.input_job.engineering_input_window.click_input(coords=(
            page.engineering_file_input_jobs_menu_coord))  # 左击Input视窗的Job按钮
        send_keys("{TAB}")  # 按下TAB键，挪动光标位置

        img_name = 'engineering_input_jobs_window'
        img_path = self.input_jobs_window.capture_image(img_name)

        cut_coords = [5, 300, 9, 278]  # 后面的是水平方向
        save_path_cut = self.input_jobs_window.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "engineering\\" + img_name + "_cut_standard.png"
        assert self.input_jobs_window.is_right(save_path_cut, img_standard_str)

        self.input_jobs_window.close()
        self.input_job.close()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
    def test_file_input_steps_window_open_close(self, job_id, epcam_ui_start):
        """
        禅道用例ID：4003 step视窗展示正确、34007 step视窗可正确关闭
        :param job_id:268
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
        self.input_job.set_new_step_name('pre')  # 多创建几个step，方便step视窗展示
        self.input_job.identify()
        self.input_job.translate(time_sleep=1)#等一下
        self.input_job.engineering_input_window.click_input(coords=(
            page.engineering_file_input_steps_window_menu_coord))  # 左击Input视窗的step按钮

        send_keys("{TAB}")  # 按下TAB键，挪动光标位置

        img_name = 'engineering_input_steps_window'
        img_path = self.input_steps_window.capture_image(img_name)

        cut_coords = [5, 300, 9, 278]  # 后面的是水平方向
        save_path_cut = self.input_steps_window.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "engineering\\" + img_name + "_cut_standard.png"
        assert self.input_steps_window.is_right(save_path_cut, img_standard_str)

        self.input_steps_window.close()
        self.input_job.close()

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

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input_excellent2'))
    def test_file_input_case_4751(self, job_id, epcam_ui_start):
        """
        禅道用例ID：4751 Input附件gerber资料，translate时excellent文件的数据越界错误 报failed
        BUG_ID：4982
        :param job_id:45727
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
        self.engineering.entity_filter('12')  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除筛选出的料号
        self.input_job = PageInput()
        file_path = str(Path(file_compressed_path).parent)
        self.input_job.set_path(file_path)  # 选择料号路径
        self.input_job.set_new_job_name('12')
        self.input_job.set_new_step_name('orig')
        self.input_job.identify()
        self.input_job.translate(time_sleep=1)

        engineering_input_excellent2_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_input_excellent2_pic.save(r'C:\cc\share\temp\engineering_input_excellent2_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_input_excellent2_pic.png')
        img_cut = img[340:580, 150:800]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_input_excellent2_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_input_excellent2_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_input_excellent2_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0

        self.input_job.close()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input_dwg'))
    def test_file_input_case_4756(self, job_id, epcam_ui_start):
        """
        可正确Input附件DWG文件，软件不卡死
        BUG_ID：5664
        :param job_id:45729
        :param epcam_ui_start:
        :return:
        """
        # # 下载料号
        job_name, file_compressed_path = Base.get_file_compressed_job_name_by_job_id_from_dms(job_id)
        # 解压rar
        rf = rarfile.RarFile(file_compressed_path)
        rf.extractall(Path(file_compressed_path).parent)
        # 删除压缩包
        os.remove(file_compressed_path) if os.path.exists(file_compressed_path) else None
        self.engineering.entity_filter('666layer')  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除筛选出的料号
        self.input_job = PageInput()
        file_path = str(Path(file_compressed_path).parent)
        self.input_job.set_path(file_path)  # 选择料号路径
        self.input_job.set_new_job_name('666layer')
        self.input_job.set_new_step_name('orig')
        self.input_job.identify()
        self.input_job.translate(time_sleep=1)

        engineering_input_dwg_pop_up_notification_pic = self.engineering.engineering_window.capture_as_image()  # 截图
        engineering_input_dwg_pop_up_notification_pic.save(r'C:\cc\share\temp\engineering_input_dwg_pop_up_notification_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\engineering_input_dwg_pop_up_notification_pic.png')
        img_cut = img[338:461, 430:615]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_input_dwg_pop_up_notification_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\engineering_input_dwg_pop_up_notification_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\engineering_input_dwg_pop_up_notification_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0

        send_keys("{ENTER}") #按下enter键关闭弹窗

        self.input_job.close()