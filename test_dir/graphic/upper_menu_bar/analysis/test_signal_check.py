import pytest
import os
import time
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.analysis.page_signal_check import PageSignalCheck
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic import upper_menu_bar

class TestGraphicUI:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()
        self.signal_check = PageSignalCheck()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Signal_check'))
    def test_graphic_analysis_signal_check_case_4672(
            self, job_id, epcam_ui_start, download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道用例ID：4672 打开附件资料的panel的画布，使用signal layer check 功能可以正确执行分析操作不发生闪退
        禅道bugID：2963
        :param job_id:44170
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()  # 双击steps
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'panel')  # 双击打开panel
        self.graphic.click_layer(job_info, 'gtl')#打开gtl层

        self.graphic = PageGraphic()
        self.graphic.open_analysis_signal_check_window()#打开signal_check窗口

        self.signal_check.click_run_type(3)
        self.signal_check.close()

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()