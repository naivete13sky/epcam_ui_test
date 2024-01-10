import time
import pyautogui
import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestSelectPolyline:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Select_Polyline_Canvas'))
    def test_graphic_select_polyline_case_4736(self, job_id, epcam_ui_start,
                                               download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：5465
        :param job_id:44122
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(3)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'orig')
        self.graphic.click_layer(job_info, 'l6')
        self.graphic.zoom_home()
        self.graphic.area_zoom()
        self.graphic.click_canvas(900, 225)
        self.graphic.click_canvas(985, 290)
        self.graphic.select_polyline()
        self.graphic.click_canvas(800, 310)
        self.graphic.zoom_home()
        coords = [(690, 600), (690, 200), (890, 400), (490, 400)]
        for coord in coords:
            pyautogui.moveTo(690, 400)
            pyautogui.mouseDown(button='middle')
            pyautogui.moveTo(coord)
            pyautogui.mouseUp(button='middle')
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()