import pytest
import os
from pywinauto.keyboard import send_keys
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.left_layer_bar.page_copper_exposed_area import PageCopperExposedArea
from cc.cc_method import GetTestData
from config_ep.page.graphic.upper_menu_bar.step.page_step_and_repeat_puzzle_by_table \
    import PageStepAndRepeatPuzzleByTable
from config_ep import page
import time
from config_ep.base.base import Base, MyODB
import rarfile
from pathlib import Path
from config_ep.page.page_input import PageInput


class TestGraphicUI:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.copper_exposed_area = PageCopperExposedArea()
        self.step_and_repeat = PageStepAndRepeatPuzzleByTable()
        self.engineering.engineering_window.set_focus()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Open_layer'))
    def test_graphic_open_left_two_layer(self, job_id, epcam_ui_start,
                                         download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证打开第二层layer正确显示
        禅道用例ID：4650
        关联bug:5592
        :param job_id:44118
        :param epcam_ui_start:
        :return:
        """
        job_name,file_compressed_path=download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()

        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 解压后得odb路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'edit')  # 双击打开panel
        self.graphic.click_layer(job_info, "gw-0001-5050-co")
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Signal_layer_check'))
    def test_graphic_analysis_signal_layer_check_case_4672(
            self, job_id, epcam_ui_start, download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道用例ID：4672 打开附件资料的panel的画布，使用signal layer check 功能可以正确执行分析操作不发生闪退
        禅道bugID：2963
        :param job_id:44170
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
        self.graphic.open_analysis_signal_layer_check_windows()
        self.graphic.graphic_window.click_input(coords=page.graphic_analysis_signal_layer_check_windows_run_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_analysis_signal_layer_check_windows_close_coord)
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Open_layer'))
    def test_graphic_open_layer_4658(self, job_id, epcam_ui_start):
        """
        验证导入附件资料，打开第一层，点击home，软件闪退
        禅道用例ID：4658
        关联bug:5105
        :param job_id:44168
        :param epcam_ui_start:
        :return:
        """
        # 下载料号
        job_name, file_compressed_path = Base.get_file_compressed_job_name_by_job_id_from_dms(job_id)
        # 解压rar
        rf = rarfile.RarFile(file_compressed_path)
        rf.extractall(Path(file_compressed_path).parent)
        # 删除压缩包
        os.remove(file_compressed_path) if os.path.exists(file_compressed_path) else None
        self.engineering.entity_filter('y6t280e15919b0')  # 筛选料号，在界面上显示指定某一个料号
        if self.engineering.job_first_is_opened():
            self.engineering.close_job_first()
        self.engineering.delete_all_jobs()  # 删除筛选出的料号
        self.input_job = PageInput()
        file_path = str(Path(file_compressed_path).parent)
        self.input_job.set_path(file_path)  # 选择料号路径
        self.input_job.set_new_job_name('y6t280e15919b0')
        self.input_job.set_new_step_name('orig')
        self.input_job.identify()
        self.input_job.translate(time_sleep=15)
        self.input_job.close()
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()
        self.engineering.open_first_step_by_double_click()
        self.graphic.graphic_window.click_input(coords=page.graphic_first_layer_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_right_home)
        time.sleep(0.10)
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Acs_copy_click'))
    def test_graphic_case_4672(self, job_id, epcam_ui_start,
                               download_file_compressed_entity_filter_delete_all_jobs_import):

        """
        禅道BUG：2409
        禅道用例：4690
        :param job_id:44553
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(2)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        print(job_info['layer_info'])
        self.engineering.open_step_by_double_click(job_info, 'edit')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, 'txt-1-8')
        self.graphic.zoom_home()
        self.graphic.feature_selection()
        send_keys('^w')
        self.graphic.click_canvas(610, 490)
        send_keys('^c')
        self.graphic.graphic_window.click_input(coords=page.graphic.acs_coord)
        self.graphic.click_canvas(610, 490)
        self.graphic.graphic_window.click_input(coords=page.graphic.acs_coord)
        self.graphic.click_canvas(610, 490)
        send_keys('^c')
        self.graphic.graphic_window.click_input(coords=page.graphic.acs_coord)
        self.graphic.click_canvas(610, 490)
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Mouse_Middle'))
    def test_graphic_case_4729(self, job_id, epcam_ui_start,
                               download_file_compressed_entity_filter_delete_all_jobs_import):

        """
        禅道BUG：2601
        :param job_id:44562
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        time.sleep(2)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        print(job_info['layer_info'])
        self.engineering.open_step_by_double_click(job_info, 'orig')
        self.graphic.graphic_window.click_input(button='middle', coords=page.graphic.left_layer_bar_blank_area_coord)
        time.sleep(0.3)
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
