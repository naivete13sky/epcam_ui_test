import os
import pytest
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.graphic.upper_menu_bar.edit.page_transform import PageTransform
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestTransform:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Transform_Scale_Not_Case'))
    def test_file_transform_scale_not_case_4722(self, job_id, epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：5498
        :param job_id:45730
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        print(odb_folder_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, '0')
        self.graphic.click_layer(job_info, '53.dxf')
        self.graphic.open_transform_window()
        self.transform = PageTransform()
        self.transform.tansform_features(True,10,10)
        self.transform.click_apply_button()
        self.transform.click_information_yes_button()
        self.transform.click_information_yes_button()
        self.transform.click_information_ok_button()

        self.transform.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()