import pytest
import os
from config_ep.page.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.left_layer_bar.page_copper_exposed_area import PageCopperExposedArea
from cc.cc_method import GetTestData
from config_ep.page.graphic.upper_menu_bar.step.page_step_and_repeat_puzzle_by_table import PageStepAndRepeatPuzzleByTable
from config_ep.base.base import MyODB

class TestCopperExposedArea:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.copper_exposed_area = PageCopperExposedArea()
        self.step_and_repeat = PageStepAndRepeatPuzzleByTable()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Exposed_Area_Mask_Crash'))
    def test_graphic_exposed_area_mask_case_4646(self, job_id, epcam_ui_start,
                                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证mask为空时执行exposed_area弹出提示框（软件不闪退）
        禅道用例ID：4646
        禅道bug ID:5638
        :param job_id:7763
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()  # 双击steps
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'panel')  # 双击打开panel
        self.graphic.click_layer(job_info, layer='gtl', button_type='right')  # 右击层别
        self.graphic.open_copper_exposed_area_dindow()  # 打开Copper/Exposed Area窗口
        text = self.copper_exposed_area.apply_exposed_area_case_4646('gtl')  # 执行exposed_area功能,mask为空有提示框
        assert text == 'Mask 1 is empty!\n'  # 验证提示框

        self.graphic.close()  # 关闭graphic窗口
        self.engineering.go_up()  # 鼠标双击go_up
        self.engineering.go_up()  # 鼠标双击go_up