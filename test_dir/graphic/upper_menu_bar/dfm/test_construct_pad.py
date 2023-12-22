import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic.upper_menu_bar.dfm.page_construct_pad import PageConstructPad
from config_ep.page.graphic.upper_menu_bar.edit.page_undo import PageUndo
import time


class TestConstructPad:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Construct_Pad_Crash'))
    def test_graphic_dfm_cleanup_construct_pad_case_4701(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证
        禅道BUG：3478
        禅道用例：4701
        :param job_id:44561
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
        self.graphic.click_layer(job_info, 'l1')
        self.graphic.open_dfm_cleanup_construct_pad_window()

        self.construct = PageConstructPad()
        self.construct.click_run_all_button(8)
        self.construct.click_layer_button()
        self.construct.layer_popup_select(job_info, layers=['l1'])    #选择具体的layer层别信息
        self.construct.layer_popup_ok()
        self.construct.click_run_all_button(2)
        self.construct.close()

        self.undo = PageUndo()
        for _ in range(2):                                # undo操作执行2次，"_"下划线在此处为占位符，不需要变量
            self.graphic.click_undo_button()
            self.undo.click_yes_button()

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
        self.engineering.close_job_first()
        time.sleep(0.5)


