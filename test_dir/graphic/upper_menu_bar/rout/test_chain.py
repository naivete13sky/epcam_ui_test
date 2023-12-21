import pytest
import os
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.page_engineering import PageEngineering
from config_ep.page.graphic.upper_menu_bar.rout.page_chain import PageChain
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB

class TestChain:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.graphic = PageGraphic()

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
        self.chain.chain_no_crash_with_file('22',1)
        self.graphic.close()
        self.engineering.go_up()
        self.engineering.go_up()

