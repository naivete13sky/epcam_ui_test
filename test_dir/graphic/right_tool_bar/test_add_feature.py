import os
import pytest
from config_ep.page.graphic.right_tool_bar.page_add_feature import AddPad
from config_ep.page.graphic.right_tool_bar.page_add_feature import PageSymbol
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestAddLine():
    def test_add_line(self):
        print("123")

class TestAddPad():

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Add_Oval_Pad_From_Symbol'))
    def test_add_oval_pad_from_symbol_not_case_4724(self, job_id, epcam_ui_start, setup_method,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证symbol窗口添加oval物件，软件不闪退
        禅道bug ID:2854
        :param job_id:44563
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        engineering = setup_method['engineering']
        engineering.open_job_first_by_double_click()
        engineering.open_steps_by_double_click()
        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r"matrix\matrix")
        job_info["step_info"] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        engineering.open_step_by_double_click(job_info, 'pcs')

        graphic = setup_method.get('graphic')
        graphic.click_add_feature()

        add_pad = AddPad()
        add_pad.add_pad(symbol_type='oval',param=[200, 300])

        graphic.close()
        engineering.go_up()
        engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Add_cb5_Pad'))
    def test_add_cb5_pad_not_case_4725(self, job_id, epcam_ui_start, setup_method,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证附件资料可以正常添加symbol库中的"cb5"物件，软件不闪退
        禅道bug ID:3268
        :param job_id:44818
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        engineering = setup_method['engineering']
        engineering.open_job_first_by_double_click()
        engineering.open_steps_by_double_click()
        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r"matrix\matrix")
        job_info["step_info"] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info["layer_info"] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        engineering.open_step_by_double_click(job_info, 'edit')
        #
        graphic = setup_method.get('graphic')
        graphic.click_layer(job_info,'gtl')
        graphic.click_add_feature()

        add_pad = AddPad()
        add_pad.add_pad(symbol_name='cb5',coord_x=690, coord_y=200)

        graphic.close()
        engineering.go_up()
        engineering.go_up()

class TestAddSurface():
    def test_add_surface(self):
        print("123")

class TestAddArc():
    def test_add_arc(self):
        print("123")
class TestAddText():
    def test_add_text(self):
        print("123")

