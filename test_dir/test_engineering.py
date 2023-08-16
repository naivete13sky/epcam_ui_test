import os
import shutil
import time
from pathlib import Path
import pytest
import pytesseract
from pywinauto.keyboard import send_keys

from config import RunConfig
from cc.cc_method import GetTestData, DMS, opencv_compare
from config_ep.epcam_ui import Engineering
import cv2


@pytest.mark.input
class TestUI:

    def test_ui_all(self,epcam_ui_start):
        my_engineering = Engineering()
        my_engineering.engineering_window.set_focus()  # 激活窗口
        engineering_window_pic = my_engineering.engineering_window.capture_as_image()# 截图
        engineering_window_pic.save(r'C:\cc\share\temp\engineering_window.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window.png')

        img_cut = img[30:60, 10:40]#后面的是水平方向,file
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu_file.png", img_cut)
        text = pytesseract.image_to_string(img_cut)# 使用Tesseract进行文字识别
        assert text == 'File\n'

        img_cut = img[30:60, 70:120]  # 后面的是水平方向,action
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu_action.png", img_cut)
        text = pytesseract.image_to_string(img_cut)# 使用Tesseract进行文字识别
        assert text == 'Action\n'

        img_cut = img[30:60, 155:205]  # 后面的是水平方向,option
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu_option.png", img_cut)
        text = pytesseract.image_to_string(img_cut)  # 使用Tesseract进行文字识别
        assert text == 'Option\n'



    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Engineering'))
    def test_go_up(self,job_id,epcam_ui_start):
        '''
        禅道用例ID：1505
        :param job_id:
        :param epcam_ui_start:
        :return:
        '''
        # 下载料号
        temp_path = os.path.join(r'C:\cc\share\temp',str(job_id))
        if os.path.exists(temp_path):
            # 删除目录及其内容
            # os.remove(temp_path)
            shutil.rmtree(temp_path)
        os.mkdir(temp_path)
        temp_compressed_path = os.path.join(temp_path, 'compressed')
        job_current_all_fields = DMS().get_job_fields_from_dms_db_pandas(job_id)
        file_compressed_name = job_current_all_fields['file'].split("/")[1]
        DMS().file_downloand(os.path.join(temp_compressed_path, file_compressed_name), temp_compressed_path)

        file_compressed_path = Path(os.path.join(temp_compressed_path,file_compressed_name))  # 替换为你的文件路径
        job_name = file_compressed_path.stem

        my_engineering = Engineering()
        my_engineering.entity_filter(job_name)#筛选料号，在界面上显示指定某一个料号
        if my_engineering.job_first_is_opened():
            my_engineering.close_job_first()
        my_engineering.delete_all_jobs()#删除筛选出的料号
        my_engineering.import_job(str(file_compressed_path),job_org_type = 'ipc2581')#导入一个料号

        my_engineering.open_job_first_by_double_click()# 双击打开料号
        my_engineering.go_up()#鼠标点击
        assert my_engineering.job_first_is_opened() == True

        my_engineering.open_job_first_by_double_click()  # 双击打开料号
        my_engineering.go_up(method='menu')  # 通过菜单action-open
        assert my_engineering.job_first_is_opened() == True

        # my_engineering.engineering_window.print_control_identifiers()

    def test_option_language(self,epcam_ui_start):
        '''
        禅道用例ID：1506
        :param epcam_ui_start:
        :return:
        '''
        my_engineering = Engineering()

        my_engineering.language_switch(language='Simplified Chinese')
        # my_engineering.engineering_window.print_control_identifiers()
        assert my_engineering.language_is_Simplified_Chinese() == True

        my_engineering.language_switch(language='EP Default')

    def test_file_save_no_job_select(self,epcam_ui_start):
        '''
        禅道用例ID：3552
        :param epcam_ui_start:
        :return:
        '''
        my_engineering = Engineering()
        my_engineering.engineering_window.click_input(coords=(800,600))#鼠标点击空白处，不选择料号
        # time.sleep(10)
        my_engineering.file_save()
        # my_engineering.engineering_window.print_control_identifiers()


        engineering_file_save_job_no_select_dialog = RunConfig.driver_epcam_ui.window(**{'title': "Save", 'control_type': "Window"})
        # dialog.print_control_identifiers()
        engineering_file_save_job_no_select_jpg = engineering_file_save_job_no_select_dialog.capture_as_image()# 截图
        engineering_file_save_job_no_select_jpg.save(r'C:\cc\share\temp\engineering_file_save_no_job_select.png')
        img = cv2.imread(r'C:\cc\share\temp\engineering_file_save_no_job_select.png')
        img_cut = img[35:60, 35:205]  # 后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_file_save_job_no_select_text.png", img_cut)
        cv2.waitKey(0)
        # 使用Tesseract进行文字识别
        text = pytesseract.image_to_string(img_cut)
        # 打印识别出的文本
        # print('text:',text)

        assert text == 'No elements were selected!\n'

        send_keys("{ENTER}")#确认关闭弹窗




class TestFile:

    @pytest.mark.coding
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Save'))
    def test_file_save_no_changed(self, job_id, epcam_ui_start):
        '''
        禅道用例ID：3553。
        :param epcam_ui_start:
        :return:
        '''

        # 下载料号
        temp_path = os.path.join(r'C:\cc\share\temp', str(job_id))
        if os.path.exists(temp_path):
            # 删除目录及其内容
            # os.remove(temp_path)
            shutil.rmtree(temp_path)
        os.mkdir(temp_path)
        temp_compressed_path = os.path.join(temp_path, 'compressed')
        job_current_all_fields = DMS().get_job_fields_from_dms_db_pandas(job_id)
        file_compressed_name = job_current_all_fields['file'].split("/")[1]
        DMS().file_downloand(os.path.join(temp_compressed_path, file_compressed_name), temp_compressed_path)

        file_compressed_path = Path(os.path.join(temp_compressed_path, file_compressed_name))  # 替换为你的文件路径
        job_name = file_compressed_path.stem

        my_engineering = Engineering()
        my_engineering.entity_filter(job_name)  # 筛选料号，在界面上显示指定某一个料号
        if my_engineering.job_first_is_opened():
            my_engineering.close_job_first()
        my_engineering.delete_all_jobs()  # 删除筛选出的料号
        my_engineering.import_job(str(file_compressed_path))  # 导入一个料号

        my_engineering.open_job_first_by_double_click()  # 双击打开料号
        # my_engineering.go_up()  # 鼠标点击


