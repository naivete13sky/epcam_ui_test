import time
import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.base.base import MyMouse
from pywinauto.keyboard import send_keys

class TestChain:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id",GetTestData.get_job_id("Delete_To_Intersection"))
    def test_delete_to_intersection_not_crash_with_file_case_4698(self, job_id, epcam_ui_start,
                                                            download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证附件资料使用delete_to_intersection功能不闪退
        禅道bug ID：4807
        :param job_id:44554
        :param epcam_ui_start:
        :return:
        """
        job_name,file_compressed_path =download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 解压后得odb路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'set')  # 双击打开panel
        self.graphic.click_layer(job_info, '2626')
        self.graphic.click_canvas(coord_x=1049,coord_y=504,button_type='center')
        scroll_clicks = 5
        for click in range(scroll_clicks):
            MyMouse.mouse_scroll(1)
        send_clicks = 2
        for click in range(send_clicks):
            send_keys("^w")
            time.sleep(0.5)
        self.graphic.click_delete_feature(1) # 点击delete_to_intresetion功能
        self.graphic.execute_delete_to_intresetion(1058, 580)
        self.graphic.execute_delete_to_intresetion(1058, 580, 1)
        self.graphic.execute_delete_to_intresetion(1058, 580, 2)
        self.graphic.execute_delete_to_intresetion(1058, 580, 1)
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()



