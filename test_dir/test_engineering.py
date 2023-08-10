import os
import shutil
import time
from pathlib import Path
import pytest
from config import RunConfig
from cc.cc_method import GetTestData, DMS, opencv_compare
from config_ep.epcam_ui import Engineering
import cv2


@pytest.mark.input
class TestUI:

    def test_ui_all(self,epcam_ui_start):
        my_engineering = Engineering()
        my_engineering.engineering_window.set_focus()  # 激活窗口
        engineering_window_jpg = my_engineering.engineering_window.capture_as_image()# 截图
        engineering_window_jpg.save(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img = cv2.imread(r'C:\cc\share\temp\engineering_window_jpg.jpg')
        img_cut = img[30:60, 10:250]#后面的是水平方向
        cv2.imwrite(r"C:\cc\share\temp\engineering_menu.jpg", img_cut)
        cv2.waitKey(0)

        # 加载两张图片
        img_standard_path = os.path.join(Path(os.path.dirname(__file__)).parent, r'data\pic\engineering\engineering_menu_standard.jpg')
        img_current_path = r'C:\cc\share\temp\engineering_menu.jpg'
        rectangle_count = opencv_compare(img_standard_path,img_current_path)

        assert rectangle_count == 0

    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Engineering'))
    def test_go_up(self,job_id,epcam_ui_start):
        '''
        禅道用例ID：1505
        :param job_id:
        :param epcam_ui_start:
        :return:
        '''
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

        my_engineering = Engineering()
        my_engineering.entity_filter(job_name)#筛选料号，在界面上显示指定某一个料号
        if my_engineering.job_first_is_opened():
            my_engineering.close_job_first()
        my_engineering.delete_all_jobs()#删除筛选出的料号
        my_engineering.import_ipc2581(str(file_compressed_path))#导入一个料号

        my_engineering.open_job_first_by_double_click()# 双击打开料号
        my_engineering.go_up()#鼠标点击
        assert my_engineering.job_first_is_opened() == True

        my_engineering.open_job_first_by_double_click()  # 双击打开料号
        my_engineering.go_up(method='menu')  # 通过菜单action-open
        assert my_engineering.job_first_is_opened() == True

        # my_engineering.engineering_window.print_control_identifiers()

    @pytest.mark.coding
    def test_option_language(self,epcam_ui_start):
        pass
        my_engineering = Engineering()

        my_engineering.language_switch(language='Simplified Chinese')
        # my_engineering.engineering_window.print_control_identifiers()
        assert my_engineering.language_is_Simplified_Chinese() == True

        my_engineering.language_switch(language='EP Default')





