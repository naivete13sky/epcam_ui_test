import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic.right_tool_bar.page_feature_selection_filter import PageFeatureSelectionFilter


class TestFeatureSelectionFilter:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()
        self.filter = PageFeatureSelectionFilter()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Feature_Selection_Filter_Crash'))
    def test_graphic_feature_selection_filter_case_4727(self, job_id, epcam_ui_start,
                                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证打开影响层，使用过滤器选中物件，软件闪退
        禅道BUG：2763
        :param job_id:44814
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'net')
        self.graphic.click_affected_layer(job_info, 'l1')

        self.graphic.feature_selection_filter()
        # self.graphic.click_affected_layer(job_info, 'l2')
        # self.filter.click_reset_button()
        self.filter.click_select_button()
        self.filter.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()


    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Feature_Selection_Filter_Advanced_Crash'))
    def test_graphic_feature_selection_filter_advanced_case_4730(self, job_id, epcam_ui_start,
                                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        【Filter】advanced高级过滤使用闪退
        禅道BUG：4313
        :param job_id:44814
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'pre')
        self.graphic.click_layer(job_info, 'l1')

        self.graphic.feature_selection_filter()
        self.filter.click_advanced_button()
        self.filter.advanced_click_surface_button()
        self.filter.advanced_surface_elements_button()
        self.filter.advanced_close()
        self.filter.click_select_button(time_sleep=3)
        self.filter.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()