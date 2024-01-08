import time
import pytest
import os
from config_ep import page
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from pywinauto.keyboard import send_keys
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.graphic.upper_menu_bar.edit.page_undo import PageUndo
from config_ep.page.graphic.upper_menu_bar.edit.page_substitute import PageSubstitute
from config_ep.page.graphic.upper_menu_bar.edit.page_contour2pad import PageContour2pad
from config_ep.page.graphic.upper_menu_bar.edit.page_create_usersymbol import PageCreateUserSymbol


class TestContourToPad:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.undo = PageUndo()
        self.contour2pad = PageContour2pad()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Contour2pad_Undo1'))
    def test_graphic_contour2pad_case_4713(self, job_id, epcam_ui_start,
                                           download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：4060
        :param job_id:44560
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(2)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit')
        self.graphic.click_layer(job_info, 'gtl')
        self.graphic.zoom_home()
        self.graphic.feature_selection()
        self.graphic.click_canvas(680, 490)
        self.graphic.open_contour2pad_window()
        self.contour2pad.click_ok_button()
        send_keys('^z')
        self.undo.click_yes_button()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Contour2pad_Undo2'))
    def test_graphic_contour2pad_case_4741(self, job_id, epcam_ui_start,
                                           download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：1552
        :param job_id:45562
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(10)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'net')
        self.graphic.click_layer(job_info, 'l1')
        self.graphic.zoom_home()
        self.graphic.area_zoom()
        self.graphic.click_canvas(780, 155)
        self.graphic.click_canvas(820, 180)
        self.graphic.feature_selection()
        self.graphic.click_canvas(777, 440)
        self.graphic.open_contour2pad_window()
        self.contour2pad.click_ok_button()
        img_name = 'graphic_contour2pad2_window'
        img_path = self.graphic.capture_image(img_name)
        cut_coords = [300, 600, 600, 1000]  # 后面的是水平方向
        save_path_cut = self.graphic.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "graphic\\" + img_name + "_cut_standard.png"
        assert self.graphic.is_right(save_path_cut, img_standard_str)
        send_keys('^z')
        self.undo.click_yes_button()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()


class TestSubstitute:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.creat_usersymbol = PageCreateUserSymbol()
        self.substitute = PageSubstitute()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Substitute'))
    def test_graphic_substitute_case_4700(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：3269
        禅道用例：4700
        :param job_id:44560
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(2)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit')
        self.graphic.click_layer(job_info, 'gts')
        self.graphic.zoom_home()
        self.graphic.area_zoom()
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_reshape_substitute_area_zoom_1_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_reshape_substitute_area_zoom_2_coord)
        self.graphic.feature_selection()
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_reshape_substitute_canvas_select_1_coord)
        self.graphic.open_create_usersymbol()
        self.creat_usersymbol.symbol_name('100')
        self.creat_usersymbol.click_ok_button()
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_reshape_substitute_canvas_select_2_coord)
        self.graphic.open_substitute_window()
        self.substitute.symbol_input('100')
        self.substitute.click_ok_button()
        self.substitute.click_information_ok_button()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
