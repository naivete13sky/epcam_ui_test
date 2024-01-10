import pytest
import os
from config_ep.page.graphic.upper_menu_bar.analysis.page_layer_netlist_check import PageLayerNetlistCheck
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestLayerNetlistCheck:

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Compare_Two_Panel_Netlist'))
    def test_compare_two_panel_netlist_not_case_4737(self, job_id, epcam_ui_start, setup_method,
                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证附件资料Compare两个panel的网络，软件不闪退
        禅道bug:4760
        :param job_id:45311
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)
        self.engineering = setup_method['engineering']
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 解压后得odb路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit46')  # 双击打开panel

        self.graphic = setup_method['graphic']
        self.graphic.open_layer_netlist_check_window()

        self.layer_netlist_check = PageLayerNetlistCheck()
        self.layer_netlist_check.click_compare('l2','panel','panel')

        self.layer_netlist_check.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Compare_Panel_And_Non_Panel_Netlist'))
    def test_compare_panel_and_non_panel_netlist_not_case_4738(self, job_id, epcam_ui_start, setup_method,
                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证附件资料Compare panel和非panel的网络，软件不闪退
        禅道bug:4760
        :param job_id:45311
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)
        self.engineering = setup_method['engineering']
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 解压后得odb路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit46')  # 双击打开panel

        self.graphic = setup_method['graphic']
        self.graphic.open_layer_netlist_check_window()

        self.layer_netlist_check = PageLayerNetlistCheck()
        self.layer_netlist_check.click_compare('l2','panel','edit46')

        self.layer_netlist_check.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()