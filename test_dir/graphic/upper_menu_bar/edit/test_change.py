import os
import time
import pytest
from config_ep.page.graphic.upper_menu_bar.edit.page_feature_to_drill_pattern import PageFeatureToDrillPattern
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.page_graphic import PageGraphic
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestFeature2drlPattern:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()
        self.feature2drl_pattern = PageFeatureToDrillPattern()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Feature2drl_Pattern'))
    def test_graphic_change_case_4722(self, job_id, epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证Feature to drill pattern钻孔值过大时闪退问题
        禅道BUG：5498
        :param job_id:44560
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
        self.engineering.open_step_by_double_click(job_info, 'edit')
        self.graphic.click_layer(job_info, 'gts')
        self.graphic.zoom_home()
        self.graphic.area_zoom()
        self.graphic.click_canvas(625, 450)
        self.graphic.click_canvas(720, 520)
        self.graphic.feature_selection()
        self.graphic.click_canvas(555, 425)
        self.graphic.open_feature2drl_pattern_window()
        self.feature2drl_pattern.target_layer_input('00000')
        self.feature2drl_pattern.drill_size_input('100')
        self.feature2drl_pattern.pitch_input('2')
        self.feature2drl_pattern.click_apply_button()
        self.feature2drl_pattern.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
