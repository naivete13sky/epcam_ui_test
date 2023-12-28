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
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Add_Pad'))
    def test_add_pad_case_4724(self, job_id, epcam_ui_start, setup_method,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证PowerGround Optimization执行优化过程中按下F1键，软件不闪退
        禅道bug ID:1384
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
        add_pad.add_pad('oval20x60',True)

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

