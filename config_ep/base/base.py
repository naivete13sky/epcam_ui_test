import os
import shutil
from pathlib import Path
from cc.cc_method import DMS
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
