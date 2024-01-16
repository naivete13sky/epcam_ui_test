import time
import pytest
import os
from pywinauto.keyboard import send_keys
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.graphic.upper_menu_bar.edit.page_connection import PageConnection
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.rout.page_chain import PageChain
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestChain:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.connection = PageConnection()
        self.chain = PageChain()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id",GetTestData.get_job_id("Chain_No_Crash"))
    def test_chain_not_crash_with_file_case_4689(self,job_id,epcam_ui_start,
                                                  download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证附件资料使用chain功能不闪退
        禅道bug ID：4849
        :param job_id:44552
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
        self.engineering.open_step_by_double_click(job_info, 'set')  # 双击打开panel
        self.graphic.open_chain() # 打开chain窗口
        self.chain = PageChain()
        self.chain.create_chain('22',1)
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id("Chain_Warning"))
    def test_graphic_chain_case_4721(self, job_id, epcam_ui_start,
                                     download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证Chain走刀设置起刀位置warning弹窗崩溃问题
        禅道bug:5303
        :param job_id:44817
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(8)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit')
        self.graphic.click_layer(job_info, 'gko')
        self.graphic.zoom_home()
        send_keys('^t')
        self.graphic.area_zoom()
        self.graphic.click_canvas(400, 580)
        self.graphic.click_canvas(450, 620)
        self.graphic.select_by_net()
        self.graphic.click_canvas(700, 300)
        self.graphic.open_chain()
        self.chain.set_tool_size(0.059)
        self.chain.set_compensation('Right')
        self.chain.click_ok_button()
        send_keys('^w')
        self.graphic.feature_selection()
        send_keys("{VK_SHIFT down}")
        self.graphic.click_canvas(700, 300)
        self.graphic.click_canvas(850, 115)
        send_keys("{VK_SHIFT up}")
        self.graphic.open_connection_window()
        self.connection.connection_mode('corner')
        self.connection.close()
        self.graphic.click_canvas(720, 125)
        send_keys('^b')
        self.graphic.click_canvas(500, 650)
        self.graphic.open_chain()
        self.chain.click_set_plunge_button()
        self.chain.click_set_plunge_type_open()
        self.chain.click_ok_button()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
