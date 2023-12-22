import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.left_layer_bar.page_split_layer import PageSplitLayer
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestSpliplayer:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Split_Layer'))
    def test_split_not_layer_case_4699(self, job_id, epcam_ui_start,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证Attribute不存在的layer弹出提示框
        禅道bug ID:2129
        :param job_id:44559
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering = PageEngineering()
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r"matrix\matrix")
        job_info["step_info"] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info["layer_info"] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit-35')

        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, layer='gtl', button_type='right')
        self.graphic.open_split_layer_window()

        self.split_layer = PageSplitLayer()
        self.split_layer.set_layer()
        self.split_layer.click_attribute_button(job_info)
        self.split_layer.close()

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

