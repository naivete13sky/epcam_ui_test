import os
import shutil
import time
from pathlib import Path

import numpy as np
import pytest
import pytesseract
from pywinauto.keyboard import send_keys

from config import RunConfig
from cc.cc_method import GetTestData, DMS, opencv_compare, PictureMethod
from config_ep.epcam_ui import Engineering,Graphic
import cv2


@pytest.mark.input
class TestUI:

    def test_ui_all(self,epcam_ui_start):
        my_engineering = Engineering()
        my_engineering.engineering_window.set_focus()  # 激活窗口
        engineering_window_pic = my_engineering.engineering_window.capture_as_image()# 截图
        img = np.array(engineering_window_pic)  # Convert the PIL image to a numpy array,此方法不需要把截图保存到硬盘的。

        img_cut = img[30:60, 10:40]#后面的是水平方向,file
        text = pytesseract.image_to_string(img_cut)# 使用Tesseract进行文字识别
        assert text == 'File\n'

        img_cut = img[30:60, 70:120]  # 后面的是水平方向,action
        text = pytesseract.image_to_string(img_cut)# 使用Tesseract进行文字识别
        assert text == 'Action\n'

        img_cut = img[30:60, 155:205]  # 后面的是水平方向,option
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
        temp_path = os.path.join(RunConfig.temp_path_base,str(job_id))
        shutil.rmtree(temp_path) if os.path.exists(temp_path) else None # 如果已存在旧目录，则删除目录及其内容
        file_compressed_name = DMS().get_file_from_dms_db(temp_path,job_id,field='file_compressed')#从DMS下载附件，并返回文件名称
        temp_compressed_path = os.path.join(temp_path, 'compressed')
        file_compressed_path = Path(os.path.join(temp_compressed_path,file_compressed_name))
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
        my_engineering.file_save()
        engineering_file_save_job_no_select_dialog = RunConfig.driver_epcam_ui.window(**{'title': "Save", 'control_type': "Window"})
        engineering_file_save_job_no_select_jpg = engineering_file_save_job_no_select_dialog.capture_as_image()# 截图
        img = np.array(engineering_file_save_job_no_select_jpg)# Convert the PIL image to a numpy array,此方法不需要把截图保存到硬盘的。
        img_cut = img[35:60, 35:205]  # 后面的是水平方向
        # 使用Tesseract进行文字识别
        text = pytesseract.image_to_string(img_cut)
        # 打印识别出的文本
        print('text:',text)
        assert text == 'No elements were selected!\n'
        send_keys("{ENTER}")#确认关闭弹窗




class TestFile:

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Save'))
    def test_file_save_no_changed(self, job_id, epcam_ui_start):
        '''
        禅道用例ID：3553。
        :param epcam_ui_start:
        :return:
        '''
        # 下载料号
        temp_path = os.path.join(RunConfig.temp_path_base, str(job_id))
        shutil.rmtree(temp_path) if os.path.exists(temp_path) else None  # 如果已存在旧目录，则删除目录及其内容
        file_compressed_name = DMS().get_file_from_dms_db(temp_path, job_id,field='file_compressed')  # 从DMS下载附件，并返回文件名称
        temp_compressed_path = os.path.join(temp_path, 'compressed')
        file_compressed_path = Path(os.path.join(temp_compressed_path, file_compressed_name))
        job_name = file_compressed_path.stem

        my_engineering = Engineering()
        my_engineering.entity_filter(job_name)  # 筛选料号，在界面上显示指定某一个料号
        my_engineering.close_job_first() if my_engineering.job_first_is_opened() else None#如果料号是打开状态，要先关闭料号

        my_engineering.delete_all_jobs()  # 删除筛选出的料号
        my_engineering.import_job(str(file_compressed_path))  # 导入一个料号

        my_engineering.open_job_first_by_double_click()  # 双击打开料号
        my_engineering.engineering_window.double_click_input(coords=my_engineering.get_engineering_job_steps_coor(coor_type = 'relative'))# 双击打开steps
        my_engineering.engineering_window.double_click_input(coords=my_engineering.get_engineering_job_steps_step_first_coor(coor_type = 'relative'))# 打开第1个step
        time.sleep(0.5)#打开graphic要等一会儿

        my_graphic = Graphic()
        my_graphic.close()#关闭Graphic窗口

        my_engineering.go_up()  # 鼠标点击
        my_engineering.go_up()  # 鼠标点击，返回到了job list界面
        my_engineering.selct_first_job()#选中第一个料号
        my_engineering.file_save()#保存

        engineering_file_save_job_no_changed_dialog = my_engineering.engineering_window.child_window(title="Information", control_type="Window")
        engineering_file_save_job_no_changed_dialog = engineering_file_save_job_no_changed_dialog.capture_as_image()  # 截图
        img = np.array(engineering_file_save_job_no_changed_dialog)
        img_cut = img[35:60, 55:210]  # 后面的是水平方向
        # 使用Tesseract进行文字识别
        text = pytesseract.image_to_string(img_cut)
        # 打印识别出的文本
        print('text:',text)
        assert text in 'Job does not changed !\n'
        send_keys("{ENTER}")  # 确认关闭弹窗

    @pytest.mark.coding
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Save'))
    def test_file_save_job_changed(self, job_id, epcam_ui_start):
        '''
        禅道用例ID：3594。
        :param epcam_ui_start:
        :return:
        '''
        # 下载料号
        temp_path = os.path.join(RunConfig.temp_path_base, str(job_id))
        shutil.rmtree(temp_path) if os.path.exists(temp_path) else None  # 如果已存在旧目录，则删除目录及其内容
        file_compressed_name = DMS().get_file_from_dms_db(temp_path, job_id,field='file_compressed')  # 从DMS下载附件，并返回文件名称
        temp_compressed_path = os.path.join(temp_path, 'compressed')
        file_compressed_path = Path(os.path.join(temp_compressed_path, file_compressed_name))
        job_name = file_compressed_path.stem

        my_engineering = Engineering()
        my_engineering.entity_filter(job_name)  # 筛选料号，在界面上显示指定某一个料号
        my_engineering.close_job_first() if my_engineering.job_first_is_opened() else None  # 如果料号是打开状态，要先关闭料号

        # my_engineering.delete_all_jobs()  # 删除筛选出的料号
        # my_engineering.import_job(str(file_compressed_path))  # 导入一个料号

        my_engineering.open_job_first_by_double_click()  # 双击打开料号
        my_engineering.engineering_window.double_click_input(
            coords=my_engineering.get_engineering_job_steps_coor(coor_type='relative'))  # 双击打开steps
        my_engineering.engineering_window.double_click_input(
            coords=my_engineering.get_engineering_job_steps_step_first_coor(coor_type='relative'))  # 打开第1个step
        time.sleep(0.5)  # 打开graphic要等一会儿

        my_graphic = Graphic()

        my_graphic.graphic_window.print_control_identifiers()

        graphic_window_pic = my_graphic.graphic_window.capture_as_image()  # 截图
        # graphic_window_pic.save(r'C:\cc\share\temp\graphic_window.png')
        img = np.array(graphic_window_pic)
        img_cut = img[160:750, 58:230]  # 后面的是水平方向,file
        cv2.imwrite(r"C:\cc\share\temp\graphic_window_layers_pic.png", img_cut)
        # 读取图片并进行 OCR
        image_path = r"C:\cc\share\temp\graphic_window_layers_pic.png"
        output_image_path = r'C:\cc\share\temp\graphic_window_layers_pic4.png'
        from PIL import Image
        image = Image.open(image_path)  # 打开图像

        # 图像灰度化： 将彩色图像转换为灰度图像可以减少颜色干扰。
        image = image.convert('L')  # Convert image to grayscale
        # 阈值化会将图像的像素值映射到两个值之间（例如，黑色和白色）.二值化： 将灰度图像转换为二值图像可以使文字与背景更明显。
        threshold_value = 130  # Adjust this threshold value as needed
        image = image.point(lambda p: 255 if p > threshold_value else p)# Apply thresholding to convert gray areas to white
        image.save(output_image_path)# 保存
        image_path = r"C:\cc\share\temp\graphic_window_layers_pic4.png"
        target_word = 'smt'
        # target_word = 'top'
        target_word_coord_percentage =PictureMethod.get_word_pos_of_picture2(image_path, target_word)
        print('target_word_coord_percentage:',target_word_coord_percentage)
        assert target_word_coord_percentage[0] > -1

        graphic_size=(0,0,1382,807)#(L0, T0, R1382, B807)

        graphic_layer_size = (172,590)#x,y

        my_coor = (int(graphic_layer_size[0] * target_word_coord_percentage[0]) + 58 + 10,int(graphic_layer_size[1] * target_word_coord_percentage[1]) + 160)
        print('my_coor:',my_coor)

        my_graphic.graphic_window.click_input(coords=my_coor)#点击 smt层







        # my_graphic.close()  # 关闭Graphic窗口
        #
        # my_engineering.go_up()  # 鼠标点击
        # my_engineering.go_up()  # 鼠标点击，返回到了job list界面
        # my_engineering.selct_first_job()  # 选中第一个料号
        # my_engineering.file_save()  # 保存
        #
        # engineering_file_save_job_no_changed_dialog = my_engineering.engineering_window.child_window(
        #     title="Information", control_type="Window")
        # engineering_file_save_job_no_changed_dialog = engineering_file_save_job_no_changed_dialog.capture_as_image()  # 截图
        # img = np.array(engineering_file_save_job_no_changed_dialog)
        # img_cut = img[35:60, 55:210]  # 后面的是水平方向
        # # 使用Tesseract进行文字识别
        # text = pytesseract.image_to_string(img_cut)
        # # 打印识别出的文本
        # print('text:', text)
        # assert text in 'Job does not changed !\n'
        # send_keys("{ENTER}")  # 确认关闭弹窗