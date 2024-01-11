import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic import left_layer_bar
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic.upper_menu_bar.dfm.page_copper_peeling import PageCopperPeeling
import time


class TestCopperPeeling:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.copper = PageCopperPeeling()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Copper_Peeling_close_job_Crash'))
    def test_graphic_dfm_copper_peeling_case_4743(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证【Copper Peeling】软件闪退
        禅道BUG：1144
        :param job_id:45564
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
        self.engineering.open_step_by_double_click(job_info, 'edit')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, 'l3')
        self.graphic.open_copper_peeling_window()

        self.copper.click_layer_button()
        self.copper.select_layer_name(job_info, ['l3'])
        self.copper.click_layer_popup_ok_button()
        self.copper.set_copper_peeling_text(5, 6, 6, 6, 6, 6, 6)
        self.copper.check_fix_bridge_by_line()
        self.copper.cilck_run_globally_button(time_sleep=8)
        self.copper.close()

        self.graphic.click_layer(job_info, layer='l3', button_type='right')
        self.graphic.click_left_delete_layer()
        self.graphic.graphic_window.click_input(coords=left_layer_bar.delete_layer_information_ok_button_coords)

        self.graphic.open_copper_peeling_window()
        self.copper.cilck_run_globally_button(time_sleep=1)
        self.copper.close()

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
        self.engineering.close_job_first()
        time.sleep(0.5)
        self.engineering.open_job_first_by_double_click()


