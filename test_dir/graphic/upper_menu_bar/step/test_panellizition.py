import pytest
import os
from config_ep.page.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.left_layer_bar.page_copper_exposed_area import PageCopperExposedArea
from cc.cc_method import GetTestData
from config_ep.page.graphic.upper_menu_bar.step.page_step_and_repeat_puzzle_by_table import PageStepAndRepeatPuzzleByTable
from config_ep.base.base import MyODB


class TestStepAndReaptPuzleByAumatic:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

class TestStepAndReaptPuzleByTable:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.copper_exposed_area = PageCopperExposedArea()
        self.step_and_repeat = PageStepAndRepeatPuzzleByTable()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Set_mirror'))
    def test_graphic_panelization_case_4652(self, job_id, epcam_ui_start,
                                            download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：1546
        禅道用例：4652
        :param job_id:44117
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
        print(job_info['layer_info'])
        self.engineering.open_step_by_double_click(job_info, 'set')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, 'drill-map')
        self.graphic.open_step_and_repeat_puzzle_by_table_window()
        self.step_and_repeat = PageStepAndRepeatPuzzleByTable()
        self.step_and_repeat.new_step_mirror()
        self.step_and_repeat.close_step_and_repeat_window()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

class TestStepAndReaptEdit:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()