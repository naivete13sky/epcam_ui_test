import os
import time
from pathlib import Path
import numpy as np
import pytest
from config import RunConfig
from cc.cc_method import GetTestData
from config_ep.epcam_ui import EPCAM

import cv2
from skimage.metrics import structural_similarity as ssim

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

        img_standard = cv2.imread(os.path.join(Path(os.path.dirname(__file__)).parent, r'data\pic\engineering\engineering_menu_standard.jpg'))
        img_current = cv2.imread(r'C:\cc\share\temp\engineering_menu.jpg')




        print("分割线")

        # 加载两张图片
        img_standard = cv2.imread(os.path.join(Path(os.path.dirname(__file__)).parent, r'data\pic\engineering\engineering_menu_standard.jpg'))
        img_current = cv2.imread(r'C:\cc\share\temp\engineering_menu.jpg')

        # 转换为灰度图像
        gray_a = cv2.cvtColor(img_standard, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(img_current, cv2.COLOR_BGR2GRAY)

        # 计算两张灰度图像的差异
        diff = cv2.absdiff(gray_a, gray_b)

        # 设定差异的阈值，这里使用了一个简单的固定阈值，你可以根据需要进行调整
        threshold = 30
        _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        # 找到差异点的轮廓
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 初始化矩形框计数器
        rectangle_count = 0

        # 在b图上标记差异点
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img_current, (x, y), (x + w, y + h), (0, 0, 255), 2)
            rectangle_count += 1

        # 输出矩形框的个数
        print(f"矩形框的个数：{rectangle_count}")

        # 保存结果图像
        cv2.imwrite(r'C:\cc\share\temp\diff_with_rectangles.jpg', img_current)

        # 显示结果图像
        cv2.imshow('Difference Image with Rectangles', img_current)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        assert rectangle_count == 0