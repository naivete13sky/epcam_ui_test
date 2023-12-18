import pytest
import os
from config_ep.page.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.step.page_robotcam import PageRobotCAM
from config_ep.page.graphic.upper_menu_bar.analysis.page_mrc import PageMRC
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestGraphicUI:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Analysis_MRC'))
    def test_graphic_mrc_case_4655(self, job_id, epcam_ui_start,
                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证不导入json，mrc运行结束后，点击单位切换，软件闪退
        禅道用例ID：4655
        关联bug:5486
        :param job_id:44121
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
        self.engineering.open_step_by_double_click(job_info, 'prepare')  # 双击打开prepare
        self.graphic.open_robotcam()
        self.robotcam = PageRobotCAM()
        self.robotcam.save()
        self.robotcam.close()
        self.graphic.open_mrc()
        self.mrc = PageMRC()
        self.mrc.click_run_globally_button(20)
        self.mrc.open_viewer_result_window()
        self.mrc.close_viewer_result_window()
        self.mrc.close()
        self.graphic.click_unit_british_system()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()