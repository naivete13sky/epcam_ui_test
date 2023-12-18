import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.central_canvas.page_measurement_mark import PageMeasurementMark
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestMeasurementtMask:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

class TestBetweenMidpoints:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Measure_Crash'))
    def test_measure_between_midpoints_case_4649(self, job_id, epcam_ui_start,
                                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证附件资料使用Measure的Between Midpoints功能不闪退
        禅道用例ID：4649
        禅道bug ID:1313
        :param job_id:44120
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
        self.engineering.open_step_by_double_click(job_info, 'net')  # 双击打开panel
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, layer='gtl', time_sleep=10)
        self.graphic.click_canvas(button_type='right')  # 右击画布
        self.graphic.open_measurement_mark_window()  # 打开Measurement Mark窗口
        self.measure = PageMeasurementMark()
        self.measure.select_measure_mode(5)  # 选择measure_mode
        self.graphic.click_canvas(690, 300)
        self.graphic.click_canvas(690 + 50, 300)
        self.measure.close()  # 关闭Measurement Mark窗口
        self.graphic.close()  # 关闭graphic窗口
        self.engineering.go_up()  # 鼠标双击go_up
        self.engineering.go_up()  # 鼠标双击go_up
