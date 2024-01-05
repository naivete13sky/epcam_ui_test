import pytest
import os
from pywinauto.keyboard import send_keys
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.graphic.upper_menu_bar.rout.page_chain import PageChain
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic.left_layer_bar.page_multi_layer_copy import PageMultiLayerCopy
from config_ep.page.matrix.page_matrix import PageMatrix
from config_ep.page.graphic.upper_menu_bar.edit.page_undo import PageUndo
import time


class TestUndo:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()
        self.chain = PageChain()
        self.undo = PageUndo()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Multi_layer_Undo'))
    def test_graphic_multi_layer_undo_case_4712(self, job_id, epcam_ui_start,
                                                download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证单层copy和多层copy以及中键覆盖功能使用后，修改step名称，点击undo闪退
        禅道BUG：4964
        禅道用例：4712
        :param job_id:
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
        self.graphic.click_layer(job_info, 'l2')
        self.graphic.click_layer(job_info, layer='l2', button_type='right')
        self.graphic.open_multi_layer_copy_window()

        self.multi = PageMultiLayerCopy()
        self.multi.click_source_step_button()
        self.multi.open_steps_pop_window(job_info, step='orig')
        self.multi.click_add_layers_button()
        self.multi.open_layers_pop_window(job_info, layers=['l2'])
        self.multi.click_ok_button()
        self.multi.information_pop_window()
        self.multi.information_pop_window()
        time.sleep(2)

        self.graphic = PageGraphic()
        self.graphic.click_job_matrix_button()
        self.matrix = PageMatrix()
        self.matrix.rename_step_open(job_info, 'net', 'edit')
        self.matrix.close()

        self.graphic = PageGraphic()
        self.graphic.click_undo_button()
        self.undo = PageUndo()
        # self.undo.click_yes_button(2)      #1.1.8.8版本可以撤销，但闪退
        self.undo.click_no_revocable_button()           # 1.1.12.3版本无法撤销
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id("Undo_Break_Line"))
    def test_graphic_undo_case_4740(self, job_id, epcam_ui_start,
                                    download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道bug:5943
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
        self.graphic.break_line()
        self.graphic.click_canvas(700, 300)
        self.graphic.double_click_canvas(700, 400)
        send_keys('^z')
        self.undo.click_yes_button()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
