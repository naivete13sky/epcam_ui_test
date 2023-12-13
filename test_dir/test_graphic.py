import pytest
import os
from cc.cc_method import GetTestData
from config_ep.page.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.page_copper_exposed_area import PageCopperExposedArea
from config_ep.base.base import MyODB

class Test_Graphic_UI:

    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()
        self.copper_exposed_area = PageCopperExposedArea()

    @pytest.mark.coding
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Graphic'))
    def test_graphic_apply_exposed_area_mask_is_null(self, job_id,epcam_ui_start,
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
        self.engineering.open_steps_by_double_click() # 双击steps
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path,r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.engineering.open_step_by_double_click(job_info,'panel') # 双击打开panel
        self.graphic.copper_exposed_area_open(job_info,'gtl') # 打开copper_exposed_area功能
        text = self.copper_exposed_area.apply_exposed_area('gtl') # 执行exposed_area功能,mask为空有提示框
        assert text == 'Mask 1 is empty!\n' # 验证提示框

        self.graphic.close() # 关闭graphic窗口
        self.engineering.go_up()  # 鼠标双击go_up
        self.engineering.go_up()  # 鼠标双击go_up





