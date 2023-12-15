import time
import pytest
import os
import cv2
import numpy as np
from PIL import Image
from config import RunConfig
from config_ep.page.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.page_copper_exposed_area import PageCopperExposedArea
from config_ep.page.page_measurement_mark import PageMeasurementMark
from config_ep.page.page_multi_layer_copy import PageMultiLayerCopy
from config_ep.base.base import MyODB
from cc.cc_method import GetTestData, PictureMethod, opencv_compare
from config_ep.page.page_step_and_repeat_puzzle_by_table import PageStepAndRepeatPuzzleByTable
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
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Exposed_Area_Mask_Crash'))
    def test_graphic_exposed_area_mask_case_4646(self, job_id, epcam_ui_start,
                                                 download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证mask为空时执行exposed_area弹出提示框（软件不闪退）
        禅道用例ID：4646
        禅道bug ID:5638
        :param job_id:7763
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
        self.graphic.right_click_layer(job_info, 'gtl')  # 右击层别
        self.graphic.open_copper_exposed_area_dindow()  # 打开Copper/Exposed Area窗口
        text = self.copper_exposed_area.apply_exposed_area_case_4646('gtl')  # 执行exposed_area功能,mask为空有提示框
        assert text == 'Mask 1 is empty!\n'  # 验证提示框

        self.graphic.close()  # 关闭graphic窗口
        self.engineering.go_up()  # 鼠标双击go_up
        self.engineering.go_up()  # 鼠标双击go_up

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Set_mirror'))
    def test_graphic_panelization_case_4652(self, job_id, epcam_ui_start,
                                            download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道BUG：1546
        禅道用例：4652
        :param job_id:44117
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
        print(job_info['layer_info'])
        self.engineering.open_step_by_double_click(job_info, 'set')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, 'drill-map')
        self.graphic.open_step_and_repeat_puzzle_by_table_window()
        self.step_and_repeat = PageStepAndRepeatPuzzleByTable()
        self.step_and_repeat.new_step_mirror()
        self.step_and_repeat.close_step_and_repeat_window()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

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
        self.graphic = PageGraphic()
        self.graphic.zoom_home()
        self.graphic.feature_selection()
        self.graphic.click_canvas(562, 520)
        self.graphic.open_close_angle_for_usersymbol()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

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
        self.graphic.click_layer(job_info, 'gtl', 10)
        self.graphic.right_click_canvas()  # 右击画布
        self.graphic.open_measurement_mark_window()  # 打开Measurement Mark窗口
        self.measure = PageMeasurementMark()
        self.measure.select_measure_mode(5)  # 选择measure_mode
        self.graphic.click_canvas(690, 300)
        self.graphic.click_canvas(690+50, 300)
        self.measure.close()  # 关闭Measurement Mark窗口
        self.graphic.close()  # 关闭graphic窗口
        self.engineering.go_up()  # 鼠标双击go_up
        self.engineering.go_up()  # 鼠标双击go_up

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Multi_Layer_Copy_Crash'))
    def test_multi_layer_copy_case_4651(self, job_id, epcam_ui_start,
                                        download_file_compressed_entity_filter_delete_all_jobs_import):
        """
         测试附件资料使用multi layer copy功能软件不能闪退
         禅道用例ID：4651
        禅道bug ID:1809
        :param job_id:44120
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
        self.engineering.open_step_by_double_click(job_info, 'pcs')

        self.graphic = PageGraphic()
        self.graphic.right_click_layer(job_info, 'gtl')
        self.graphic.open_multi_layer_copy_dindow()

        self.mutli = PageMultiLayerCopy()
        self.mutli.multi_layer_copy_case_4651(job_info, soure_step='net', add_layers=['gtl'], suffix='_net')

        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

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
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Analysis_MRC'))
    def test_graphic_mrc_case_4655(self, job_id, epcam_ui_start,
                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证不导入json，mrc运行结束后，点击单位切换，软件闪退
        禅道用例ID：4655
        关联bug:5486
        :param job_id:44121
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_steps_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 解压后得odb路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info, 'prepare')  # 双击打开prepare
        self.graphic.graphic_window.click_input(coords=page.graphic_step_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_step_robotcam_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_step_robotcam_save_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_step_robotcam_ok_information_window_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_step_robotcam_close_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_analysis_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_analysis_mrc_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_analysis_mrc_run_globally_coord)
        time.sleep(20)
        self.graphic.graphic_window.click_input(coords=page.graphic_analysis_mrc_view_results_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_analysis_mrc_select_first_results_coord)  #此步可省略，也能闪退
        self.graphic.graphic_window.click_input(coords=page.graphic_analysis_mrc_close_results_viewer_coord)
        self.graphic.graphic_window.click_input(coords=page.graphic_unit_british_system_coord)
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
