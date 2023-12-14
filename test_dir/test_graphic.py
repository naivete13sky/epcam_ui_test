import pytest
import os
import cv2
import numpy as np
from PIL import Image
from config import RunConfig
from config_ep.page.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.page_copper_exposed_area import PageCopperExposedArea
from config_ep.page.page_measurement_mark import PageMeasurementMark
from config_ep.base.base import MyODB
from cc.cc_method import GetTestData, PictureMethod, opencv_compare


class TestGraphicUI:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.copper_exposed_area = PageCopperExposedArea()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.coding
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Graphic'))
    def test_graphic_apply_exposed_area_mask_is_null(self, job_id, epcam_ui_start,
                                                     download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证mask为空时执行exposed_area弹出提示框（软件不闪退）
        禅道用例ID：4646
        禅道bug ID:5638
        :param job_id:7763
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()  # 双击steps
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info,'panel') # 双击打开panel
        self.graphic.right_click_layer(job_info,'gtl')  # 右击层别
        self.graphic.open_copper_exposed_area_dindow() # 打开Copper/Exposed Area窗口
        text = self.copper_exposed_area.apply_exposed_area('gtl') # 执行exposed_area功能,mask为空有提示框
        assert text == 'Mask 1 is empty!\n' # 验证提示框

        self.graphic.close()  # 关闭graphic窗口
        self.engineering.go_up()  # 鼠标双击go_up
        self.engineering.go_up()  # 鼠标双击go_up

    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Graphic'))
    def test_graphic_step_by_table(self, job_id, epcam_ui_start,
                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：1546
        料号ID：44117
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()  # 双击打开steps
        self.engineering.open_fourth_step_by_double_click()  # 双击打开第四个step
        graphic_window_set_pic = self.graphic.graphic_window.capture_as_image()  # 截图
        img = np.array(graphic_window_set_pic)
        x_s, x_e = 58, 230  # x_s,x_e分别是层别列表的x方向开始与结束像素。
        y_s, y_e = 160, 750  # y_s,y_e分别是层别列表的y方向开始与结束像素。
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
        target_word = 'map'
        target_word_coord_percentage = PictureMethod.get_word_pos_of_picture(output_image_path, target_word)
        assert target_word_coord_percentage[0] > -1
        graphic_layer_size = (x_e - x_s, y_e - y_s)  # x,y
        my_coord = (int(graphic_layer_size[0] * target_word_coord_percentage[0]) + x_s + 10,
                    int(graphic_layer_size[1] * target_word_coord_percentage[1]) + y_s)
        self.graphic.graphic_window.click_input(coords=my_coord)
        self.graphic.open_step_panelization_by_table()
        self.graphic.add_new_step_by_table_mirror()
        graphic_step_panelization_by_table_mirror_pic = self.engineering.engineering_window.capture_as_image()
        graphic_step_panelization_by_table_mirror_pic.save(
            r'C:\cc\share\temp\graphic_step_panelization_by_table_mirror_pic.png')
        img = cv2.imread(r'C:\cc\share\temp\graphic_step_panelization_by_table_mirror_pic.png')
        img_cut = img[5:690, 0:925]
        cv2.imwrite(r"C:\cc\share\temp\graphic_step_panelization_by_table_mirror_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'graphic\graphic_step_panelization_by_table_mirror_pic_cut_standard.png')
        img_current_path = r'C:\cc\share\temp\graphic_step_panelization_by_table_mirror_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        assert rectangle_count == 0
        self.graphic.close_by_table_window()
        self.graphic = PageGraphic()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Measure'))
    def test_measure_between_midpoints(self,job_id,epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()  # 双击steps
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'net')  # 双击打开panel
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info,'gtl',10)
        self.graphic.right_click_canvas() # 右击画布
        self.graphic.open_measurement_mark_window() # 打开Measurement Mark窗口
        self.measure = PageMeasurementMark()
        self.measure.select_measure_mode(5) # 选择measure_mode
        self.graphic.click_canvas(690, 300)
        self.graphic.click_canvas(690+50, 300)
        self.measure.close() # 关闭Measurement Mark窗口
        self.graphic.close() # 关闭graphic窗口
        self.engineering.go_up() # 鼠标双击go_up
        self.engineering.go_up() # 鼠标双击go_up

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Graphic'))
    def test_multi_layer_copy(self, job_id, epcam_ui_start,
                              download_file_compressed_entity_filter_delete_all_jobs_import):
        print("123sdasdas")
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Import'))
    def test_open_left_two_layer(self, job_id, epcam_ui_start,
                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道用例ID：4650
        关联bug:5592
        DMS_ID：44118
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        job_name,file_compressed_path=download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()

        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path) #解压后得odb路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit')  # 双击打开panel
        self.graphic.click_layer(job_info,"gw-0001-5050-co")
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()




