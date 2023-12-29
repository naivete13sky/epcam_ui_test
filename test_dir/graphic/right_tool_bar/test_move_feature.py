import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic.upper_menu_bar.edit.page_delete import PageDelete
import time


class TestMoveFeature:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Move_Feature_Crash'))
    def test_graphic_move_feature_case_4716(self, job_id, epcam_ui_start,
                                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证右侧工具栏的move功能，全选后删除，双击闪退
        禅道BUG：3836
        禅道用例：4716
        :param job_id:44814
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
        self.engineering.open_step_by_double_click(job_info, 'net')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, 'gtl')

        self.graphic.click_move_feature()
        self.graphic.click_canvas(coord_x=712, coord_y=610, button_type='left')
        self.graphic.click_edit_delete_button()

        self.delete = PageDelete()
        self.delete.click_yes_button(1)

        self.graphic = PageGraphic()
        self.graphic.double_click_canvas(coord_x=712, coord_y=610, button_type='left', time_sleep=1)

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

