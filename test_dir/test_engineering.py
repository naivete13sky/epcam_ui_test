import time

import pytest
from config import RunConfig
from cc.cc_method import GetTestData
from config_ep.epcam_ui import EPCAM

import cv2

@pytest.mark.input
class TestUI:
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Engineering'))
    def test_ui_all(self,job_id,epcam_ui_start):
        pass
        print('\njob_id:',job_id)

        my_epcam = EPCAM()
        #清空所有料号，ctrl + A 全选料号，然后 ctrl + B删除
        my_epcam.delete_all_jobs()

        # 截图与比图
        engineering_window_jpg = my_epcam.engineering_window.capture_as_image()
        engineering_window_jpg.save(r'temp\engineering_window_jpg.jpg')
        img = cv2.imread(r'temp\engineering_window_jpg.jpg')
        img_cut = img[1:100, 1:300]
        cv2.imwrite(r"temp\person.jpg", img_cut)
        cv2.waitKey(0)


