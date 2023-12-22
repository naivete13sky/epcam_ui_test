import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.dfm.page_dynamc_etch_compensation import PageDynamicEtchCompensation
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestDynamicEtchCompensation:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Dynamc_Etch_Compensation'))
    def test_dynamic_etch_compensation_case_4703(self, job_id, epcam_ui_start,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证Attribute不存在的layer弹出提示框
        禅道bug ID:
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
        # odb_folder_path = r'C:\cc\share\temp\44559\compressed\4z99008a'
        odb_matrix_file = os.path.join(odb_folder_path, r"matrix\matrix")
        job_info["step_info"] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info["layer_info"] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit-35')

        self.graphic = PageGraphic()
        self.graphic.open_dynamc_etch_compensation_window()

        self.dynamic_etch_compensation = PageDynamicEtchCompensation()
        # self.dynamic_etch_compensation.click_compensation_functions_button(1,5)
        self.dynamic_etch_compensation.save_as_json(1,5,"123")
        self.dynamic_etch_compensation.delete_json(1,5)
        self.dynamic_etch_compensation.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
