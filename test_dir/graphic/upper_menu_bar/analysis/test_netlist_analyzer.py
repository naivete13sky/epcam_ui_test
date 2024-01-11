import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic.upper_menu_bar.analysis.page_netlist_analyzer import PageNetListAnalyzer
import time


class TestNetlistAnalyzer:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.netlist = PageNetListAnalyzer()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Netlist_Analyzer_close_job_Crash'))
    def test_netlist_analyzer_case_4745(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证【Netlist Analyzer】后，点击关闭料号，软件闪退
        禅道BUG：2406
        :param job_id:45567
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

        self.graphic.click_delete_feature(delete_type=0)
        self.graphic.double_click_canvas(coord_x=695, coord_y=320)
        self.graphic.open_netlist_analyzer_window()

        self.netlist = PageNetListAnalyzer()
        self.netlist.click_first_step_button()

        self.netlist.select_step(job_info, step_name='orig')
        # self.netlist.click_step_ok_button()   #此步用不到，上一步step直接双击
        self.netlist.click_compare_button(time_sleep=5)
        self.netlist.click_broken_button()
        self.netlist.select_broken_project()
        self.netlist.broken_close()
        self.netlist.close()

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
        self.engineering.close_job_first()
        self.engineering.open_job_first_by_double_click()
