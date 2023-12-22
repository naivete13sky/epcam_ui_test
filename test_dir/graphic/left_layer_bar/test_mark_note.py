import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.left_layer_bar.page_mark_note import PageMrakNote
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
import time

class TestMultiLayerCopy:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()


    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Mark_Note_move_Crash'))
    def test_mark_note_case_4695(self, job_id, epcam_ui_start,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证note标记层别为空，Mark note功能使用直接闪退
        禅道用例ID：4695
        禅道bug ID:3459
        :param job_id:44556
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
        self.engineering.open_step_by_double_click(job_info, 'net')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, layer='l1', button_type='right')
        self.graphic.open_mark_note_window()
        self.mark = PageMrakNote()
        self.mark.click_delete_all_notes_button()
        self.mark.click_no_note_information()
        self.mark.click_move_note_button()
        self.graphic.click_canvas(1065, 555)
        time.sleep(0.10)
        self.mark.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()


    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Mark_Note_copy_Crash'))
    def test_mark_note_case_4697(self, job_id, epcam_ui_start,
                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证note标记层别为空，Mark note功能使用直接闪退
        禅道用例ID：4697
        禅道bug ID:3459
        :param job_id:44558
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(10)
        self.engineering = PageEngineering()
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r"matrix\matrix")
        job_info["step_info"] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info["layer_info"] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'net')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, 'comp')
        self.graphic.click_layer(job_info, layer='comp', button_type='right')
        self.graphic.open_mark_note_window()
        self.mark = PageMrakNote()
        self.mark.click_delete_all_notes_button()           #删除所有已存在的note标记
        self.mark.click_delete_note_information_ok()
        self.graphic.zoom_home()
        self.mark.click_add_note_button()                   # 点击添加note标记
        self.graphic.add_double_click(1065, 555)            # 双击画布坐标添加note标记成功
        self.mark.click_delete_note_by_mouse_button()       # 点击通过鼠标点击删除note标记
        self.graphic.add_double_click(1065, 555)            # 双击画布坐标删除
        self.mark.click_copy_note_button()                  # 点击copy note标记按钮
        self.graphic.click_canvas(1065, 555)                # 点击画布
        time.sleep(0.10)
        self.mark.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
