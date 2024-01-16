import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.left_layer_bar.page_multi_layer_copy import PageMultiLayerCopy
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestMultiLayerCopy:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Multi_Layer_Copy_Crash'))
    def test_multi_layer_copy_case_4651(self, job_id, epcam_ui_start,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        测试附件资料使用multi layer copy功能软件不能闪退
        禅道用例ID：4651
        禅道bug ID:1809
        :param job_id:44120
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
        self.engineering.open_step_by_double_click(job_info, 'pcs')

        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, layer='gtl', button_type='right')
        self.graphic.open_multi_layer_copy_window()

        self.mutli = PageMultiLayerCopy()
        self.mutli.multi_layer_copy_case_4651(job_info, soure_step='net', add_layers=['gtl'], suffix='_net')

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
