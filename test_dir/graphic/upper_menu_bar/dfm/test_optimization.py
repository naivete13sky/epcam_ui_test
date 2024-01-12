import os
import pyautogui
import pytest
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.dfm.page_powerground_optimization import PagePowerGroundOptimization
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestPowerGroundOptimization:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('PowerGround_Optimization'))
    def test_powerground_optimization_case_4711(self, job_id, epcam_ui_start,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证PowerGround Optimization执行优化过程中按下F1键，软件不闪退
        禅道bug ID:1384
        :param job_id:44563
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
        self.engineering.open_step_by_double_click(job_info, 'pcs')

        self.graphic = PageGraphic()
        self.graphic.open_powerground_optimization_window()

        self.powerground = PagePowerGroundOptimization()
        self.powerground.click_run_globally_button(2)
        pyautogui.press('f1')
        self.powerground.close_information_window()
        self.powerground.close()

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()