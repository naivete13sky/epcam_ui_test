import time
import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestSelectByNet:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Select_By_Net'))
    def test_graphic_select_by_net_case_4726(self, job_id, epcam_ui_start,
                                             download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：5929
        :param job_id:44814
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
        self.engineering.open_step_by_double_click(job_info, 'edit')
        self.graphic.click_layer(job_info, 'gto')
        self.graphic.zoom_home()
        self.graphic.area_zoom()
        self.graphic.click_canvas(640, 310)
        self.graphic.click_canvas(810, 430)
        self.graphic.select_by_net()
        self.graphic.click_canvas(290, 415)
        self.graphic.click_canvas(588, 428)
        self.graphic.click_canvas(988, 500)
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
