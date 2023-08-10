import os
import shutil
import time
from pathlib import Path
import pytest
from config import RunConfig
from cc.cc_method import GetTestData,DMS
from config_ep.epcam_ui import EPCAM
import cv2


@pytest.mark.input
class TestUI:

    def test_ui_all(self,epcam_ui_start):

        my_epcam = EPCAM()
        my_epcam.engineering_window.set_focus()  # 激活窗口

        # my_epcam.delete_all_jobs()#清空所有料号，ctrl + A 全选料号，然后 ctrl + B删除

        # 截图
        engineering_window_jpg = my_epcam.engineering_window.capture_as_image()
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img_cut = img[30:60, 10:250]#后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu.jpg", img_cut)
        cv2.waitKey(0)

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
        # 自定义矩形框的宽度和高度
        custom_width = 10
        custom_height = 10

        # 在b图上标记差异点
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(img_current, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(img_current, (x, y), (x + custom_width, y + custom_height), (0, 0, 255), 2)
            rectangle_count += 1

        # 输出矩形框的个数
        print(f"矩形框的个数：{rectangle_count}")

        # 保存结果图像
        cv2.imwrite(r'C:\cc\share\temp\diff_with_rectangles.jpg', img_current)

        # 显示结果图像
        # cv2.imshow('Difference Image with Rectangles', img_current)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        assert rectangle_count == 0

        print("分割线")

    @pytest.mark.coding
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Engineering'))
    def test_go_up(self,job_id,epcam_ui_start):

        # 下载料号
        temp_path = os.path.join(r'C:\cc\share\temp',str(job_id))
        if os.path.exists(temp_path):
            # 删除目录及其内容
            # os.remove(temp_path)
            shutil.rmtree(temp_path)
        os.mkdir(temp_path)
        temp_compressed_path = os.path.join(temp_path, 'compressed')
        job_current_all_fields = DMS().get_job_fields_from_dms_db_pandas(job_id)
        file_compressed_name = job_current_all_fields['file'].split("/")[1]
        DMS().file_downloand(os.path.join(temp_compressed_path, file_compressed_name), temp_compressed_path)

        file_compressed_path = Path(os.path.join(temp_compressed_path,file_compressed_name))  # 替换为你的文件路径
        job_name = file_compressed_path.stem

        my_epcam = EPCAM()
        my_epcam.entity_filter(job_name)#筛选料号，在界面上显示指定某一个料号
        if my_epcam.job_first_is_opened():
            my_epcam.close_job_first()
        my_epcam.delete_all_jobs()#删除筛选出的料号
        my_epcam.import_ipc2581(str(file_compressed_path))#导入一个料号
        my_epcam.open_job_first_by_double_click()# 双击打开料号
        my_epcam.go_up()


        assert my_epcam.job_first_is_opened() == True



        # my_epcam.engineering_window.print_control_identifiers()









