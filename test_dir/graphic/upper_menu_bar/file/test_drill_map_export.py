import pytest
import os
import pyautogui
import time
import datetime
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.file.page_drillmap_export import PageDrillMapExport
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB
from pywinauto.keyboard import send_keys
from config_ep.page.graphic import upper_menu_bar


class TestDrillMapExport:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.engineering.engineering_window.set_focus()
        self.graphic = PageGraphic()
        self.drill_map_export = PageDrillMapExport()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Drill_map_export'))
    def test_graphic_file_drill_map_export_case_4746(
            self, job_id, epcam_ui_start, download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道用例ID：4746 导入附件物料，可正确输出drill map软件不闪退
        禅道bugID：1575
        :param job_id:45723
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
        self.engineering.open_step_by_double_click(job_info, 'orig')  # 双击打开orig
        self.graphic.click_layer(job_info, 'drillmap')  # 打开drill_map层

        self.graphic.open_file_drill_map_export_window()  # 打开drill_map_export窗口
        self.drill_map_export.click_export_path_button()
        self.drill_map_export.click_export_window_file_nama_input()# 定位到新窗口export_window的文件名输入栏
        # 获取当前时间戳
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # 要输入的字符串加上时间戳
        input_string = f"drill_map_{timestamp}"
        # 打印生成的输入字符串
        print(input_string)
        # 模拟键盘输入
        pyautogui.typewrite(input_string)
        time.sleep(2)
        send_keys("{ENTER}")  # 按下enter键
        time.sleep(0.2)  # 等待0.2s
        send_keys("{ENTER}")  # 按下enter键
        self.drill_map_export.click_export_button()  # 点击Export按钮运行
        self.drill_map_export.click_export_button()  # 再点击Export按钮，预期正确运行不闪退

        self.drill_map_export.close()
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()
