import os
import pytest
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic import upper_menu_bar
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.step.page_step_and_repeat_puzzle_by_table \
    import PageStepAndRepeatPuzzleByTable
from config_ep.page.graphic.upper_menu_bar.step.page_step_and_repeat_puzzle_by_automatic import \
    PageStepAndRepeatPuzzleByAutomatic


class TestStepAndRepeatPuzzleByAutomatic:
    def setup_method(self):
        self.graphic = PageGraphic()
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.step_and_repeat_by_automatic = PageStepAndRepeatPuzzleByAutomatic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Automatic_panel'))
    def test_graphic_step_and_repeat_puzzle_by_automatic_case_4714(
            self, job_id, epcam_ui_start, download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：4840
        禅道用例：4714
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
        self.graphic.open_step_and_repeat_puzzle_by_automatic_window()
        self.step_and_repeat_by_automatic.step_name_input('pcs')
        self.step_and_repeat_by_automatic.panel_x_min_input('100')
        self.step_and_repeat_by_automatic.panel_y_min_input('100')
        self.step_and_repeat_by_automatic.click_ok_button()
        self.step_and_repeat_by_automatic.click_information_ok_button()
        self.step_and_repeat_by_automatic.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()


class TestStepAndRepeatPuzzleByTable:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.step_and_repeat_by_table = PageStepAndRepeatPuzzleByTable()
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
        self.graphic.click_layer(job_info, 'drill-map')
        self.graphic.open_step_and_repeat_puzzle_by_table_window()
        self.step_and_repeat_by_table.new_step_button()
        self.step_and_repeat_by_table.steps_popup_window.click_input(
            coords=upper_menu_bar.step_and_repeat_puzzle_by_table_steps_popup_pcs_step_coord)
        self.step_and_repeat_by_table.steps_popup_ok_button()
        self.step_and_repeat_by_table.step_mirror()
        self.step_and_repeat_by_table.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()


class TestStepAndRepeatEdit:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()
