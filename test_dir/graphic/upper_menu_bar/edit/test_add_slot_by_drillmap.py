import os
import pytest
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.page.graphic.upper_menu_bar.edit.page_add_slot_by_drillmap import PageAddSlotByDrillmap
from config_ep.page.matrix.page_matrix import PageMatrix
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData
from config_ep.base.base import MyODB


class TestAddSlotByDrillmap:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus()
        self.matrix = PageMatrix()
        self.graphic = PageGraphic()
        self.add_slot_by_drlmap = PageAddSlotByDrillmap()

    @pytest.mark.from_bug
    @pytest.mark.crash
    @pytest.mark.parametrize("job_id", GetTestData.get_job_id('Add_slot_by_drlmap'))
    def test_graphic_add_slot_by_drillmap_case_4692(self, job_id, epcam_ui_start,
                                                    download_file_compressed_entity_filter_delete_all_jobs_import):

        """
        禅道BUG：2573
        禅道用例：4692
        :param job_id:44555
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)
        self.engineering.open_job_first_by_double_click()
        self.engineering.open_matrix_by_double_click()
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info = {}
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.matrix.rename_step_open(job_info, 'orig+1', 'net')
        self.graphic = PageGraphic()
        self.graphic.click_layer(job_info, 'drl1-4')
        self.graphic.click_layer(job_info, 'drillmap')
        self.graphic.open_add_solt_by_drillmap_window()
        self.add_slot_by_drlmap = PageAddSlotByDrillmap()
        self.add_slot_by_drlmap.layer_input('drl1-4')
        self.add_slot_by_drlmap.maplayer_input('drillmap')
        self.add_slot_by_drlmap.add_slot_by_dilmap_ok()
        self.graphic.close()
        self.matrix.close()
        self.engineering.go_up()
