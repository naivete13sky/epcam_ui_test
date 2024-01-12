import os
import time
import pytest
from config_ep import page
from pywinauto.keyboard import send_keys
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.graphic.upper_menu_bar.edit.page_connection import PageConnection
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestConnection:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()
        self.connection = PageConnection()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Connection_rout'))
    def test_graphic_connection_case_4694(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证connection对rout层线和弧导角闪退问题
        禅道BUG：2796
        :param job_id:44557
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(2)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        print(odb_folder_path)
        odb_matrix_file = os.path.join(odb_folder_path.split("/")[0], r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'array')
        self.graphic.click_layer(job_info, 'rout')
        self.graphic.zoom_home()
        self.graphic.area_zoom()
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_connection_rout_area_zoom_1_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_connection_rout_area_zoom_2_coord)
        self.graphic.feature_selection()
        send_keys('^w')
        send_keys("{VK_SHIFT down}")
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_connection_rout_select_line_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_connection_rout_select_arc_coord)
        send_keys("{VK_SHIFT up}")
        self.graphic.open_connection_window()
        self.connection.connection_mode('corner')
        self.connection.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Connection_Line_Arc'))
    def test_graphic_connection_case_4750(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证connection连接线和弧导致其他地方断线的问题
        禅道BUG：1585
        :param job_id:45726
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(2)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        print(odb_folder_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'orig')
        self.graphic.click_layer(job_info, 'r')
        self.graphic.zoom_home()
        send_keys("^t")
        self.graphic.feature_selection()
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_connection_line_arc_select_line_coord)
        send_keys("{VK_SHIFT down}")
        self.graphic.graphic_window.click_input(coords=page.graphic.edit_connection_line_arc_select_arc_coord)
        send_keys("{VK_SHIFT up}")
        self.graphic.open_connection_window()
        self.connection.connection_mode('corner')
        self.connection.close()
        img_name = 'graphic_connection_line_arc'
        img_path = self.graphic.capture_image(img_name)
        cut_coords = [100, 650, 360, 1100]  # 后面的是水平方向
        save_path_cut = self.graphic.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "graphic\\" + img_name + "_cut_standard.png"
        assert self.graphic.is_right(save_path_cut, img_standard_str)
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
