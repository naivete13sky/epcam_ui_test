import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.analysis.page_drill_check import PageDrillCheck

from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestGraphicUI:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Analysis_Drill_Check_Crash'))
    def test_graphic_drill_check_case_4719(self, job_id, epcam_ui_start,
                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证钻孔分析在panel中使用会发生闪退情况
        禅道bug:2967
        禅道用例ID：4719
        :param job_id:44815
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 解压后得odb路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'panel')  # 双击打开panel

        self.graphic = PageGraphic()
        self.graphic.click_drill_check_window()

        self.drillcheck = PageDrillCheck()
        self.drillcheck.click_run_globally_button(7)
        self.drillcheck.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
        self.engineering.close_job_first()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Drill_Check_Result_Crash'))
    def test_graphic_drill_check_case_4720(self, job_id, epcam_ui_start,
                                           download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证钻孔分析不勾选网络分析，点击close pths，软件闪退
        禅道bug:2670
        禅道用例ID：4720
        :param job_id:44816
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 解压后得odb路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'pre')  # 双击打开pre

        self.graphic = PageGraphic()
        self.graphic.click_drill_check_window()

        self.drillcheck = PageDrillCheck()
        self.drillcheck.click_unselect_computing_board_network()
        self.drillcheck.click_run_globally_button(5)
        self.drillcheck.open_viewer_result_window()
        self.drillcheck.click_result_categories(item_x=340, item_y=110)
        self.drillcheck.close_viewer_result_window()


        self.drillcheck.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
        self.engineering.close_job_first()
