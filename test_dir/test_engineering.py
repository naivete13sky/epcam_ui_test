import pytest
from config import RunConfig
from cc.cc_method import GetTestData
from config_ep.epcam_ui import EPCAM


@pytest.mark.input
class TestUI:
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Engineering'))
    def test_ui_all(self,job_id,epcam_ui_start):
        pass
        print('\njob_id:',job_id)

        engineering_window = RunConfig.driver_epcam_ui.window(title="Engineering 1.1.7.2")

        # engineering_window.print_control_identifiers()

        cc = EPCAM.get_engineering_left_top_Coor(engineering_window)
        print("cc:",cc)



        assert 1==1