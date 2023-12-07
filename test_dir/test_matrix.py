import os
import time
import cv2
import pytest
from config import RunConfig
from config_ep import page
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.page.page_matrix import PageMatrix
from config_ep.page.page_view_graphic import PageViewGraphic
from config_ep.page.page_graphic import PageGraphic
import pyautogui
from config_ep.base.base import MyODB


class Test_Matrix_UI:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()  # 激活窗口

    @pytest.mark.coding
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Change_Matrix'))
    def test_matrix_change_drill_correlation_layer(self,job_id,epcam_ui_start,
                                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        调整drill层的关联层
        禅道用例ID：4608
        DMS_ID：42983
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_matrix_by_double_click() # 双击Matrix,打开Matrix窗口
        self.matrix = PageMatrix()
        job_info = {}
        matrix_file_path = MyODB.get_odb_matrix_file_path(file_compressed_path)  # 得到odb的matrix文件路径
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(matrix_file_path) # 得到料号layer信息

        self.matrix.change_drill_cross(job_info,'drl1-10','top','bot') # 修改孔带

        img_name = 'drill_correlation_layer'
        cut_coords = [100, 799, 8, 1032] # 后面的是水平方向
        save_path_cut = self.matrix.cut_img(img_name, cut_coords)
        img_standard_str = "matrix\\" + img_name + "_cut_standard.png"
        assert self.matrix.is_right(save_path_cut, img_standard_str)
        self.matrix.close()  # 关闭matrix窗口
        self.engineering.go_up()  # 鼠标双击go_up