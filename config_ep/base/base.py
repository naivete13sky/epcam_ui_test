import os
import shutil
from pathlib import Path
from cc.cc_method import get_print_control_identifiers_text, get_coord_of_object, DMS
from config import RunConfig



class Base:
    def __init__(self):
        pass

    @staticmethod
    def get_file_compressed_job_name_by_job_id_from_dms(job_id):
        temp_path = os.path.join(RunConfig.temp_path_base, str(job_id))
        shutil.rmtree(temp_path) if os.path.exists(temp_path) else None  # 如果已存在旧目录，则删除目录及其内容
        # 从DMS下载附件，并返回文件名称
        file_compressed_name = DMS().get_file_from_dms_db(temp_path, job_id, field='file_compressed')
        temp_compressed_path = os.path.join(temp_path, 'compressed')
        file_compressed_path = Path(os.path.join(temp_compressed_path, file_compressed_name))
        job_name = file_compressed_path.stem
        return job_name, file_compressed_path



class Engineering(object):
    # 获得坐标
    def getCoor(self,window,wanted_title):
        win_text = get_print_control_identifiers_text(window)
        coor_ok = get_coord_of_object(wanted_title, win_text)
        return coor_ok

    def get_engineering_left_top_Coor(self):
        win_text2 = get_print_control_identifiers_text(self.engineering_window)
        coor_ok = get_coord_of_object(RunConfig.driver_epcam_ui_engineering_title, win_text2)
        return coor_ok

