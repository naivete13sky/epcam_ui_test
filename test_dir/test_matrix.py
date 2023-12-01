import pytest
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.page.page_matrix import PageMatrix
import pyautogui

class Test_Matrix_UI:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()  # 激活窗口

    @pytest.mark.coding
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Drill_Correlation_Layer'))
    def test_matrix_change_drill_correlation_layer(self,job_id,epcam_ui_start,
                                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        禅道用例ID：4608
        :param job_id:
        :param epcam_ui_start:
        :return:
        """
        download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_matrix_by_double_click() # 双击Matrix,打开Matrix窗口

        self.matrix = PageMatrix()
        self.matrix.select_drill_correlation_top()
        pyautogui.mouseDown(button='left')  # 模拟按下鼠标左键
        pyautogui.moveTo(466, 400, duration=2)  # 移动鼠标到指定位置（x，y），duration控制拖动速度
        pyautogui.mouseUp(button='left')  # 模拟释放鼠标左键

        self.matrix.select_drill_correlation_bot()
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(466, 670, duration=2)
        pyautogui.mouseUp(button='left')
        assert self.matrix.drill_correlation_layer_is_right()

        self.matrix.close()  # 关闭matrix窗口
        self.engineering.go_up()  # 鼠标双击go_up