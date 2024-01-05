import time
import pytest
import os
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page import graphic
from config_ep.page.graphic.left_layer_bar.page_feature_histogram import PageFeatureHistogram
from config_ep.page.graphic.upper_menu_bar.edit.page_resize import PageGlobal
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.page_graphic import PageGraphic


class TestGlobal:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.global_ = PageGlobal()
        self.feature_histogram = PageFeatureHistogram()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Global_close'))
    def test_graphic_global_case_4702(self, job_id, epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：3288
        :param job_id:44562
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(2)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'net')
        self.graphic.click_layer(job_info, 'smt')
        self.graphic.open_global_window()
        self.global_.size_input('10')
        self.global_.click_ok_button()
        self.global_.information_click_yes_button()
        self.graphic.file_close()
        self.engineering.open_step_by_double_click(job_info, 'net')
        self.graphic.file_close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Global_Feature_Histogram'))
    def test_graphic_global_case_4734(self, job_id, epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：4464
        :param job_id:45309
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(2)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'orig')
        self.graphic.click_layer(job_info, 'symbol_type')
        self.graphic.open_global_window()
        self.global_.size_input('100')
        self.global_.click_ok_button()
        self.global_.information_click_yes_button()
        self.graphic.click_layer(job_info, 'symbol_type', button_type='right')
        self.graphic.graphic_window.click_input(coords=graphic.left_layer_bar_feature_histogram_coord)
        self.feature_histogram.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
