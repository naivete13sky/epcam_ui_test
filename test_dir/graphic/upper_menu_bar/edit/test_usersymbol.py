import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from config_ep.page.graphic.upper_menu_bar.edit.page_create_usersymbol import PageCreateUserSymbol


class TestCreateUserSymbol:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Create_UserSymbol_name'))
    def test_graphic_create_usersymbol_case_4691(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证创建usersymbol时，命名与标准symbol库冲突，软件闪退
        禅道BUG：4692
        禅道用例：4691
        :param job_id:44121
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
        self.engineering.open_step_by_double_click(job_info, 'prepare')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, 'l1')
        self.graphic.feature_selection()
        self.graphic.click_canvas(562, 520)   #选中物件的坐标（画布）
        self.graphic.open_create_usersymbol()    #打开Creat UserSymbol窗口
        self.creat = PageCreateUserSymbol()
        self.creat.symbol_name(symbol='r10')   #给选中symbol输入一个名称
        self.creat.click_ok_button()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Create_UserSymbol_length'))
    def test_graphic_create_usersymbol_case_4693(self, job_id, epcam_ui_start,
                                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证 Creat Usersymbo若命名为r10+字母，软件闪退
        禅道BUG：4693
        禅道用例：4693
        :param job_id:44121
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
        self.engineering.open_step_by_double_click(job_info, 'prepare')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, 'l1')
        self.graphic.feature_selection()
        self.graphic.click_canvas(425, 471)  # 选中物件的坐标（画布）
        self.graphic.open_create_usersymbol()  # 打开Creat UserSymbol窗口
        self.creat = PageCreateUserSymbol()
        self.creat.symbol_name(symbol='r10gnsjghsjh')  # 给选中symbol输入一个名称
        self.creat.click_ok_button()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

class TestAngleForUserSymbol:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Angle_for_usersymbol'))
    def test_graphic_usersymbol_case_4653(self, job_id, epcam_ui_start,
                                          download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：1811
        禅道用例：4653
        :param job_id:44123
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
        self.graphic.click_layer(job_info, 'top')
        self.graphic.zoom_home()
        self.graphic.feature_selection()
        self.graphic.click_canvas(562, 520)
        self.graphic.open_angle_for_usersymbol_ok()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
