import pytest
import os
from config_ep import page
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic.upper_menu_bar.edit.page_resize import PageGlobal
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.page_graphic import PageGraphic


class TestGlobal:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.global_ = PageGlobal()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Global'))
    def test_graphic_global_case_4702(self, job_id, epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：3288
        禅道用例：4702
        :param job_id:44562
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
