import time
import pytest
import os
from pywinauto.keyboard import send_keys
from config_ep.page.graphic import upper_menu_bar
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.right_tool_bar.page_feature_selection_filter import PageFeatureSelectionFilter
from config_ep.page.graphic.upper_menu_bar.dfm.page_dynamc_etch_compensation import PageDynamicEtchCompensation
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestDynamicEtchCompensation:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.feature_selection_filter = PageFeatureSelectionFilter()
        self.dynamic_etch_compensation = PageDynamicEtchCompensation()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Dynamc_Etch_Compensation'))
    def test_dynamic_etch_compensation_case_4703(self, job_id, epcam_ui_start,
                                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证Attribute不存在的layer弹出提示框
        禅道bug ID:5904
        :param job_id:44559
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
        job_info["layer_info"] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit-35')

        self.graphic = PageGraphic()
        self.graphic.open_dynamic_etch_compensation_window()

        self.dynamic_etch_compensation = PageDynamicEtchCompensation()
        self.dynamic_etch_compensation.save_as_json(json_name="123")
        self.dynamic_etch_compensation.delete_json(json_name="123")
        self.dynamic_etch_compensation.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Compensation_undo'))
    def test_graphic_dynamic_etch_compensation_case_4715(self, job_id, epcam_ui_start,
                                                         download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道bug ID:5025
        :param job_id:44560
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
        job_info["layer_info"] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit')
        self.graphic.click_layer(job_info, 'gtl')
        self.graphic.click_affected_layer(job_info, 'gbl')
        self.graphic.feature_selection_filter()
        self.feature_selection_filter.click_pad_button()
        self.feature_selection_filter.click_surface_button()
        self.feature_selection_filter.click_negative_button()
        self.feature_selection_filter.click_select_button()
        self.feature_selection_filter.close()
        self.graphic.open_dynamic_etch_compensation_window()
        self.dynamic_etch_compensation.click_compensation_functions_button(1, 1)
        self.dynamic_etch_compensation.add_new_json('0.1')
        self.dynamic_etch_compensation.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_add_row_button_coord)
        self.dynamic_etch_compensation.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_spacing_step_first_row_value1_input_coord)
        send_keys('0')
        self.dynamic_etch_compensation.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_spacing_step_first_row_value2_input_coord)
        send_keys('4')
        self.dynamic_etch_compensation.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_to_infinity_check_box_coord)
        self.dynamic_etch_compensation.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_to_infinity_value1_input_coord)
        send_keys('4')
        self.dynamic_etch_compensation.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_to_infinity_value2_input_coord)
        send_keys('0.5')
        self.dynamic_etch_compensation.dynamc_compensate_range_window.click_input(
            coords=upper_menu_bar.dynamic_compensate_range_ok_button_coords)
        self.warning_window = self.graphic.graphic_window.child_window(
            **upper_menu_bar.warning_window_para)
        self.warning_window.click_input(coords=upper_menu_bar.dynamic_compensate_range_ok_waring_yes_button_coord)
        coords = self.dynamic_etch_compensation.get_all_json_input_coords()
        for coord in coords:
            self.dynamic_etch_compensation.dynamic_etch_compensation_window.click_input(coords=coord)
            send_keys('^a')
            send_keys('0.1.json')
        self.dynamic_etch_compensation.run_on_selected_features_yes()
        self.dynamic_etch_compensation.run_operation(1)
        time.sleep(10)
        self.dynamic_etch_compensation.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
