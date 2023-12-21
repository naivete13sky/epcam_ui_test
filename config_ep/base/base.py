import os
import re
import shutil
from pathlib import Path
import pyautogui
from cc.cc_method import DMS
from config import RunConfig
import tarfile as tf


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



class MyODB:
    pass

    @staticmethod
    def get_odb_folder_path(file_compressed_path) -> str:
        """
        获取odb中所有layer信息
        :param file_compressed_path:
        :return:
        """
        ifn = file_compressed_path  # 解压文件路径
        untgz_path = Path(ifn).parent  # 解压后存放路径
        job_name = File.untgz(ifn, untgz_path)  # 解压
        odb_folder_path = os.path.join(untgz_path, job_name)
        return odb_folder_path

    @staticmethod
    def get_layer_info_from_odb_file(odb_matrix_file) -> dict:
        """
        获取每个layer中的部分信息
        :param odb_matrix_file:
        :return：
        """
        with open(odb_matrix_file, 'r') as f:
            content = f.read()
        # print('content:', content)
        re_com = re.compile(r"LAYER \{([\s\S]*?)\}")
        matches = re_com.findall(content)
        dict_layer = {}
        for match in matches:
            lines = match.splitlines()
            dict_layer[lines[4].split('=')[1]] = {'row': lines[1].split('=')[1],'type': lines[3].split('=')[1]}
        return dict_layer

    @staticmethod
    def get_step_info_from_odb_file(odb_matrix_file) -> dict:
        """
        获取每个step中的部分信息
        :param odb_matrix_file:
        :return：
        """
        with open(odb_matrix_file, 'r') as f:
            content = f.read()
        # print('content:', content)
        re_com = re.compile(r"STEP \{([\s\S]*?)\}")
        matches = re_com.findall(content)
        dict_step = {}
        for match in matches:
            lines = match.splitlines()
            dict_step[lines[2].split('=')[1]] = {'col': lines[1].split('=')[1]}
        return dict_step

    @staticmethod
    def get_layer_featur_from_odb_file(odb_steps_folder_path) -> dict:
        """
        获取每个layer的feature信息
        :param odb_steps_folder_path:
        :return:
        """
        dict_layer_feature = {}
        for step in os.listdir(odb_steps_folder_path):
            step_path = os.path.join(odb_steps_folder_path, step)
            if os.path.isdir(step_path):
                dict_layer_feature[step] = {}
                for subdirectory in os.listdir(step_path):
                    if subdirectory == "layers":
                        layers_path = os.path.join(step_path, subdirectory)
                        for layer in os.listdir(layers_path):
                            layer_path = os.path.join(layers_path, layer)
                            if os.path.isdir(layer_path):
                                dict_layer_feature[step][layer] = {}
                                feature_path = os.path.join(layer_path, 'features')
                                if os.path.exists(feature_path):
                                    file_size = os.path.getsize(feature_path)
                                    dict_layer_feature[step][layer][
                                        'features'] = file_size > 0
                                else:
                                    dict_layer_feature[step][layer][
                                        'features'] = False
        return dict_layer_feature

class File:
    @staticmethod
    def untgz(ifn, untgz_path):
        """解压tgz文件到指定目录
        :param     ifn(str):解压导入路径
        :param     untgz_path(str):解压后存放路径
        :returns   :返回解压后的文件名
        :raises    error:
        """
        try:
            ifn = ifn.split(sep='"')[1]
        except:
            pass
        ofn = untgz_path
        # with tf.open(ifn, 'r:gz') as tar:
        tar = tf.open(ifn)
        for tarinfo in tar:
            if os.path.exists(os.path.join(ofn, tarinfo.name)):
                for root, dirs, files in os.walk(os.path.join(ofn, tarinfo.name), topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
            tar.extract(tarinfo.name, ofn)
        return os.path.dirname(tarinfo.name)


class MyMouse:
    @staticmethod
    def mouse_simulator(coord_x, coord_y, duration=2):
        """
        模拟鼠标左键按下、拖动、释放的操作
        ：param coord_x: x坐标
        ：param coord_y: y坐标
        ：param duration: 拖动速度
        """
        pyautogui.mouseDown(button='left')  # 模拟按下鼠标左键
        pyautogui.moveTo(coord_x, coord_y, duration=duration)  # 移动鼠标到指定位置（x，y），duration控制拖动速度
        pyautogui.mouseUp(button='left')  # 模拟释放鼠标左键

    @staticmethod
    def mouse_scroll(clicks:int):
        """
        模拟鼠标滚动
        ：param pixel:滚动像素。100,模拟向上滚动100像素；-100，模拟向下滚动100像素。
        """
        pyautogui.scroll(clicks=clicks)

