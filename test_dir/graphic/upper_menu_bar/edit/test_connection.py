import os
import pytest
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.matrix.page_matrix import PageMatrix
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.graphic.upper_menu_bar.edit.page_connection import PageConnection
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestConnection:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.matrix = PageMatrix()
        self.graphic = PageGraphic()
        self.connection = PageConnection()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Connection_rout'))
    def test_graphic_connection_case_4694(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：2796
        禅道用例：4694
        :param job_id:44557
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        print(odb_folder_path)
        odb_matrix_file = os.path.join(odb_folder_path.split("/")[0], r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'array')
        self.graphic.click_layer(job_info, 'rout')
        self.graphic.zoom_home()
        self.graphic.area_zoom()
        self.graphic.connection_area_zoom()
        self.graphic.feature_selection()
        self.graphic.click_canvas_select_line_arc()
        self.graphic.open_connection_window()
        self.connection.click_apply_button()
        self.connection.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
