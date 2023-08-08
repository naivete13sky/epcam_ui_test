import time

import pytest
from config import RunConfig
from cc.cc_method import GetTestData
from config_ep.epcam_ui import EPCAM

from pywinauto.keyboard import send_keys

@pytest.mark.input
class TestUI:
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Engineering'))
    def test_ui_all(self,job_id,epcam_ui_start):
        pass
        print('\njob_id:',job_id)

        engineering_window = RunConfig.driver_epcam_ui.window(title="Engineering 1.1.7.2")

        # engineering_window.print_control_identifiers()

        # cc = EPCAM.get_engineering_left_top_Coor(engineering_window)
        # print("cc:",cc)

        #清空料号，ctrl + A 全选料号，然后 ctrl + B删除
        engineering_window.set_focus()# 激活窗口
        send_keys("^a")# 发送 Ctrl + A 快捷键，全选
        send_keys("^b")# 发送 Ctrl + B 快捷键，删除
        send_keys("{ENTER}")# 发送回车键，删除
        send_keys("{ENTER}")# 发送回车键，确认删除所有
        time.sleep(3)






        assert 1==1