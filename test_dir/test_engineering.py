import os
import time

import numpy as np
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

        # 截图
        engineering_window_jpg = my_epcam.engineering_window.capture_as_image()
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img_cut = img[30:60, 10:250]#后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu.jpg", img_cut)
        cv2.waitKey(0)

        # 比图
        img_standard = cv2.imread(os.path.join(os.getcwd(), r'data\pic\engineering\engineering_menu.jpg'))
        img_current = cv2.imread(r'C:\cc\share\temp\engineering_menu.jpg')

        if img_standard.shape == img_current.shape:
            print("shape一样")
        else:
            print("shape not equal")

        difference = cv2.subtract(img_standard, img_current)
        print(difference)
        result = not np.any(difference)

        if result is True:
            print("两张图一样")
        else:
            cv2.imwrite(r"temp\result.jpg", difference)
            print("两张图不一样")

        assert result == True