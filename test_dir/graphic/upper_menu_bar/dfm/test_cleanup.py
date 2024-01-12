import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.dfm.page_redundant_line_removal import PageRedundantLineRemoval
from cc.cc_method import GetTestData
import pyautogui
from config_ep.base.base import MyODB
from config_ep.page.graphic import upper_menu_bar
from config_ep.page.graphic import left_layer_bar
from config_ep.page.graphic.upper_menu_bar.dfm.page_impedance_line_recognition import PageImpedanceLineRecognition
import time


class TestRedundantLineRemoval:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Redundant_Line_Removal_F1'))
    def test_redundant_line_removal_f1_not_case_4748(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """

        禅道BUG：4995
        :param job_id:45724
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
        self.engineering.open_step_by_double_click(job_info, 'net')
        self.graphic = PageGraphic()
        self.graphic.open_redundant_line_removal_window()
        self.redundant_line_removal = PageRedundantLineRemoval()
        self.redundant_line_removal.click_run_globally_button(time_sleep=2)
        pyautogui.press('f1')
        self.redundant_line_removal.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()


class TestImpedanceLineRecognition:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()
        self.impedance = PageImpedanceLineRecognition()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Impedance_Line_Recognition_F1_Crash'))
    def test_dfm_cleanup_impedance_line_recognition_F1_case_4749(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证【Impedance Line Recognition】按F1闪退
        禅道BUG：2415
        :param job_id:45725
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
        self.graphic.click_layer(job_info, 'gtl')

        self.graphic.open_impedance_line_recognition_window()
        self.impedance.click_layer_button()
        self.impedance.select_layer(job_info, layer_name=['gtl'])
        self.impedance.click_layer_popup_ok_button()
        self.impedance.click_differential()
        self.impedance.click_plus_butoon()
        self.impedance.input_parameter(line_width=5.034, line_spacing=3.037)
        self.impedance.click_dropdown()
        self.impedance.Ipimpedance_line_recognition_window.click_input(
            coords=upper_menu_bar.impedance_line_recognition_reference_select_layer_coords)
        self.impedance.click_ok_button(press='f1')
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Impedance_Line_Recognition_undo_Crash'))
    def test_dfm_cleanup_impedance_line_recognition_undo_case_4755(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证【Impedance Line Recognition】将产生的新层删除，点击undo，软件闪退
        禅道BUG：2417
        :param job_id:45725
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
        self.graphic.click_layer(job_info, 'gtl')

        self.graphic.open_impedance_line_recognition_window()
        self.impedance.click_layer_button()
        self.impedance.select_layer(job_info, layer_name=['gtl'])
        self.impedance.click_layer_popup_ok_button()
        self.impedance.click_differential()
        self.impedance.click_plus_butoon()
        self.impedance.input_parameter(line_width=5.034, line_spacing=3.037)
        self.impedance.click_dropdown()
        self.impedance.Ipimpedance_line_recognition_window.click_input(
            coords=upper_menu_bar.impedance_line_recognition_reference_select_layer_coords)
        self.impedance.click_ok_button(time_sleep=5)
        self.graphic.graphic_window.click_input(coords=(125, 600), button='right')   #产生的层别坐标，右击

        self.graphic.click_left_delete_layer()
        self.graphic.graphic_window.click_input(coords=left_layer_bar.delete_layer_information_ok_button_coords)
        self.graphic.click_undo_button()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
