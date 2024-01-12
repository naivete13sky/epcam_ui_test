import os
import pytest
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.dfm.page_powerground_optimization import PagePowerGroundOptimization
from config_ep.page.graphic.right_tool_bar.page_feature_selection_filter import PageFeatureSelectionFilter
from config_ep.page.graphic.upper_menu_bar.edit.page_delete import PageDelete
from config_ep.page.graphic.upper_menu_bar.dfm.page_solder_mask_optimization import PageSolderMaskOptimization
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestPowerGroundOptimization:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('PowerGround_Optimization'))
    def test_powerground_optimization_case_4711(self, job_id, epcam_ui_start,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证PowerGround Optimization执行优化过程中按下F1键，软件不闪退
        禅道bug ID:1384
        :param job_id:44563
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
        self.engineering.open_step_by_double_click(job_info, 'pcs')

        self.graphic = PageGraphic()
        self.graphic.open_powerground_optimization_window()

        self.powerground = PagePowerGroundOptimization()
        self.powerground.click_run_globally_button('f1')
        self.powerground.close()

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()



class TestSolderMaskOptimization:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()
        self.feature_selection_filter = PageFeatureSelectionFilter()
        self.delete = PageDelete()
        self.solder_opt = PageSolderMaskOptimization()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Solder_Mask_Optimization_Close_Job_Crash'))
    def test_dfm_solder_mask_optimization_close_job_case_4753(self, job_id, epcam_ui_start,
                                                              download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证【SM Opt】后，点击关闭料号闪退
        禅道BUG：3324
        :param job_id:45728
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
        self.engineering.open_step_by_double_click(job_info, '11')
        self.graphic.click_layer(job_info, 'cm')

        self.graphic.feature_selection_filter()
        self.feature_selection_filter.click_positive_button()
        self.feature_selection_filter.click_select_button()
        self.feature_selection_filter.click_close_reset_button()
        self.graphic.click_edit_delete_button()
        self.graphic.area_zoom()
        self.graphic.click_canvas(550, 285)
        self.graphic.click_canvas(670, 415)
        self.graphic.open_solder_mask_optimization_window()
        self.solder_opt.move_window()   # 拖动功能视窗
        self.solder_opt.click_layer_button()
        self.solder_opt.select_layer(job_info, layer=['cm'])
        self.solder_opt.click_layer_popup_ok_button()
        self.solder_opt.set_clearance_parameter(0.8, 2)
        self.solder_opt.set_coverage_parameter(2, 2)
        self.solder_opt.set_bridge_parameter(3, 3)
        self.solder_opt.click_run_on_features_on_screen_only(32)
        self.solder_opt.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
        self.engineering.close_job_first()
        self.engineering.open_job_first_by_double_click()
