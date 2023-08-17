import json
import os,sys
import re
import urllib  # 导入urllib库
import urllib.request
import time
from pathlib import Path

import cv2
import psycopg2
import rarfile
from sqlalchemy import create_engine
import pandas as pd
from config import RunConfig
print(os.path.dirname("__file__"))
sys.path.append(RunConfig.epcam_python_interface_path)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_path)
sys.path.insert(0, os.path.join(base_path,r'config_ep/epcam'))

import tarfile as tf

class GetTestData():
    pass
    def get_job_id(self,fun):
        pd_1=pd.read_excel(io=os.path.join(os.path.abspath('.'),r"config.xlsx"), sheet_name="test_data")
        return [ each2 for each1 in pd_1[(pd_1["测试功能"]==fun) & (pd_1["是否执行"] == 1)][['测试料号']].values.tolist() for each2 in each1]

class CompressTool():
    @staticmethod
    def untgz(ifn, untgz_path):
        """解压tgz文件到指定目录
        :param     ifn(str):解压导入路径
        :param     untgz_path(str):解压后存放路径
        :returns   :None
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
        print('uncompress success!')
        return os.path.dirname(tarinfo.name)
        # os.system('pause')
        return

class DMS():

    # 下载文件
    def file_downloand(self,need_file_path, save_path):  #######文件下载
        if os.path.exists(need_file_path) == False:  # 判断是否存在文件

            # 文件url
            file_url = 'http://10.97.80.119/media/files/{}'.format(os.path.basename(need_file_path))

            # 文件基准路径
            # basedir = os.path.abspath(os.path.dirname(__file__))
            # 下载到服务器的地址
            file_path = save_path

            try:
                # 如果没有这个path则直接创建
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                # file_suffix = os.path.splitext(file_url)[1]
                # filename = '{}{}'.format(file_path, file_suffix)  # 拼接文件名。
                filename = os.path.join(file_path, os.path.basename(need_file_path))
                urllib.request.urlretrieve(file_url, filename=filename)
                print("成功下载文件")
            except IOError as exception_first:  # 设置抛出异常
                print(1, exception_first)

            except Exception as exception_second:  # 设置抛出异常
                print(2, exception_second)
        else:
            print("文件已经存在！")

    def get_job_fields_from_dms_db_sql(self,sql):
        pass
        conn = psycopg2.connect(database="epdms", user="readonly", password="123456", host="10.97.80.119", port="5432")
        cursor = conn.cursor()
        sql = sql
        print('sql:', sql)
        cursor.execute(sql)
        conn.commit()
        ans = cursor.fetchall()
        conn.close()
        return ans

    def get_job_fields_from_dms_db_pandas(self, job_id,*args, **kwargs):
        sql = '''SELECT a.* from eptest_job_for_test a
                where a.id = {}
                '''.format(job_id)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/epdms')
        pd_job_current = pd.read_sql(sql=sql, con=engine).loc[0]
        if 'field' in kwargs:
            return pd_job_current[kwargs['field']]
        else:
            return pd_job_current

    def get_job_layer_fields_from_dms_db_pandas(self, job_id,*args, **kwargs):
        sql = '''SELECT a.* from eptest_layer a
            where a.job_id = {}
                '''.format(job_id)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/epdms')
        pd_job_current_layers = pd.read_sql(sql=sql, con=engine)
        if 'field' in kwargs:
            return pd_job_current_layers[kwargs['field']]
        else:
            return pd_job_current_layers

    def get_job_layer_fields_from_dms_db_pandas_one_layer(self, job_id,*args, **kwargs):
        layer=kwargs['filter']
        sql = '''SELECT a.* from eptest_layer a
            where a.job_id = {} and lower(a.layer)='{}'
                '''.format(job_id,layer)
        # print("sql:",sql)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/epdms')
        pd_job_current_layer = pd.read_sql(sql=sql, con=engine)
        return pd_job_current_layer

    def get_job_layer_drill_from_dms_db_pandas_one_job(self, job_id,*args, **kwargs):

        sql = '''SELECT a.* from eptest_layer a
            where a.job_id = {} and a.status = 'published' and a.layer_file_type = 'excellon2'
                '''.format(job_id)
        # print("sql:",sql)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/epdms')
        pd_job_current_layer_drill = pd.read_sql(sql=sql, con=engine)
        return pd_job_current_layer_drill

    def get_file_from_dms_db(self,temp_path,job_id,*args, **kwargs):
        job_current_all_fields = self.get_job_fields_from_dms_db_pandas(job_id)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        #判断是要下载哪个类型的文件
        if 'field' in kwargs:
            print('field:',kwargs['field'])
            #如果下载的是整理过的gerber压缩包
            if kwargs['field'] == 'file_compressed':
                temp_compressed_path = os.path.join(temp_path, 'compressed')
                if not os.path.exists(temp_compressed_path):
                    os.mkdir(temp_compressed_path)
                temp_ep_path = os.path.join(temp_path, 'ep')
                if not os.path.exists(temp_ep_path):
                    os.mkdir(temp_ep_path)
                file_compressed_name = job_current_all_fields['file'].split("/")[1]

                # 下载并解压原始gerber文件
                if not os.path.exists(os.path.join(temp_compressed_path, file_compressed_name)):
                    print("not have")
                    self.file_downloand(os.path.join(temp_compressed_path, file_compressed_name), temp_compressed_path)

                if 'decompress' in kwargs:
                    print('decompress', kwargs['decompress'])
                    time.sleep(0.1)
                    file_compressed_file_path = os.listdir(temp_compressed_path)[0]
                    print("file_compressed_file_path:", file_compressed_file_path)
                    temp_compressed = os.path.join(temp_compressed_path, file_compressed_name)
                    if kwargs['decompress'] == 'rar':
                        rf = rarfile.RarFile(temp_compressed)
                        rf.extractall(temp_compressed_path)
                        # 删除压缩包
                        if os.path.exists(temp_compressed):
                            os.remove(temp_compressed)
                        # return os.listdir(temp_compressed_path)[0].lower()  + '_ep'
                        # 料号名称设置为小写，不能有'.'
                        return os.listdir(temp_compressed_path)[0].lower().replace('.', '') + '_ep'

                    if kwargs['decompress'] == 'tgz':
                        pass
                        CompressTool.untgz(os.path.join(temp_compressed_path, os.listdir(temp_compressed_path)[0]), temp_compressed_path)
                        if os.path.exists(os.path.join(temp_compressed_path, file_compressed_file_path)):
                            os.remove(os.path.join(temp_compressed_path, file_compressed_file_path))
                        return os.listdir(temp_compressed_path)[0].lower()
                else:
                    pass
                    return (os.listdir(temp_compressed_path)[0])



            # 如果下载的是G转图的tgz
            if kwargs['field'] == 'file_odb_g':
                temp_g_path = os.path.join(temp_path, 'g')
                if not os.path.exists(temp_g_path):
                    os.mkdir(temp_g_path)
                file_odb_g_name = job_current_all_fields['standard_odb'].split("/")[1]

                # 下载并解压原始gerber文件
                if not os.path.exists(os.path.join(temp_g_path, file_odb_g_name)):
                    print("not have")
                    self.file_downloand(os.path.join(temp_g_path, file_odb_g_name), temp_g_path)

                if 'decompress' in kwargs:
                    print('decompress', kwargs['decompress'])
                    time.sleep(0.1)
                    g_tgz_file = os.listdir(temp_g_path)[0]
                    print("g_tgz_file:", g_tgz_file)
                    CompressTool.untgz(os.path.join(temp_g_path, os.listdir(temp_g_path)[0]), temp_g_path)
                    if os.path.exists(os.path.join(temp_g_path, g_tgz_file)):
                        os.remove(os.path.join(temp_g_path, g_tgz_file))
                return os.listdir(temp_g_path)[0].lower()

    def get_job_layer_rout_from_dms_db_pandas_one_job(self, job_id,*args, **kwargs):

        sql = '''SELECT a.* from eptest_layer a
            where a.job_id = {} and a.status = 'published' and a.layer_file_type = 'excellon2' and a.layer_type = 'rout'
                '''.format(job_id)
        # print("sql:",sql)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/epdms')
        pd_job_current_layer_rout = pd.read_sql(sql=sql, con=engine)
        return pd_job_current_layer_rout



class Print():
    @staticmethod
    def print_with_delimiter(text, sign='*', numbers=198):
        pass
        print(str(sign) * int((numbers - len(text.encode('utf-8'))) / 2), text, str(sign) * int((numbers - len(text.encode('utf-8'))) / 2))

    @staticmethod
    def print_with_delimiter1(text,sign='*',numbers=200):
        pass
        # print(text.center( int(numbers) - len(text.encode('utf-8')), '*'))
        print(text.center(int(numbers) - len(text), '*'))




def get_data(file_path):
    """
    读取参数化文件
    :param file_path:
    :return:
    """
    data = []
    with(open(file_path, "r")) as f:
        dict_data = json.loads(f.read())
        for i in dict_data:
            data.append(tuple(i.values()))
    return data


def getFlist(path):
    for root, dirs, files in os.walk(path):
        print('root_dir:', root)  #当前路径
        print('sub_dirs:', dirs)   #子文件夹
        print('files:', files)     #文件名称，返回list类型
    return files

class StringMehtod(object):
    @staticmethod
    def is_chinese(string):
        """判断是否有中文
        :param     string(str):所有字符串
        :returns   :False
        :raises    error:
        """
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

#存储为json文件的方法
def else1():
    pass
    all_result_g = {"layer1":"正常","layer2":"错误"}
    #结果存入josn文件，如果有需要的话
    if os.path.exists(r'result.json'):
        os.remove(r'result.json')
    with open(r'result.json', 'w') as f:
        json.dump(all_result_g, f, indent=4, ensure_ascii=False)




class TextArea(object):
    def __init__(self):
        self.buffer = []
    def write(self,*args,**kwargs):
        self.buffer.append(args)

def get_print_control_identifiers_text(object_print_control_identifiers):
    stdout = sys.stdout
    sys.stdout = TextArea()
    object_print_control_identifiers.print_control_identifiers()
    text_area, sys.stdout = sys.stdout, stdout
    # print('text_area.buffer:',text_area.buffer)
    return text_area.buffer

def get_coor_of_object(text_wanted,text_from):
    pass
    for tup in text_from:
        i = tup[0].find(text_wanted)
        if i > 0:
            pattern = re.compile(r"(\(L\d+, T\d+, R\d+, B\d+\))")
            result = pattern.findall(tup[0])
            tup_coor = result[0]
    coor_file_w = int(tup_coor.split(",")[0][2:]) + 1
    coor_file_h = int(tup_coor.split(",")[1][2:]) + 1
    return (coor_file_w, coor_file_h)

def opencv_compare(img_standard_path,img_current_path,custom_width = 10, custom_height = 10):

    # 加载两张图片
    img_standard = cv2.imread(img_standard_path)
    img_current = cv2.imread(img_current_path)

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
    custom_width = custom_width
    custom_height = custom_height

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
    return rectangle_count


class PictureMethod(object):
    @staticmethod
    def png_to_tiff_one_file(input_path, output_path):
        try:
            # 打开PNG图像
            from PIL import Image
            image = Image.open(input_path)

            # 将PNG图像转换为TIFF图像
            image.save(output_path, format='TIFF')

            print("转换成功！")
        except Exception as e:
            print("转换出错:", str(e))

    @staticmethod
    def png_to_tiff_batch(input_folder,out_folder):
        pass
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                input_path = os.path.join(root, file)
                print("文件名1:", input_path)
                print("文件名2",os.path.splitext(file)[0])
                output_path = os.path.join(out_folder,os.path.splitext(file)[0]) + '.tif'
                PictureMethod.png_to_tiff_one_file(input_path,output_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                # print("文件夹:", dir_path)

    @staticmethod
    def get_word_pos_of_picture(image_path,target_word):
        import pytesseract
        from PIL import Image
        # 读取图片并进行 OCR
        image = Image.open(image_path)  # 打开图像

        # 使用 Tesseract 进行文本块检测和识别
        text_boxes = pytesseract.image_to_boxes(image, config='--psm 6')

        image_width, image_height = image.size

        for box in text_boxes.splitlines():
            box_data = box.split()
            character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

            # 获取字符的文本内容
            character_text = character

            # 计算相对于图像左上角的坐标
            relative_x = x / image_width
            relative_y = 1.0 - (y / image_height)

            # print(f"Text: {character_text}, Relative X: {relative_x}, Relative Y: {relative_y}")


        # 将文本块存储为列表
        text_boxes_list = text_boxes.splitlines()
        # print('text_boxes_list:',text_boxes_list)

        # 遍历文本块，找到目标单词的位置
        target_word_start = -1
        target_word_end = -1
        for i in range(len(text_boxes_list)):
            box_data = text_boxes_list[i].split()
            # print('box_data:',box_data)
            character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

            if character == target_word[0]:
                # print("i:",i)
                potential_word = character
                for j in range(1, len(target_word)):
                    next_box_data = text_boxes_list[i + j].split()
                    next_character = next_box_data[0]
                    potential_word += next_character
                if potential_word == target_word:
                    target_word_start = i
                    target_word_end = i + j
                    break  # 只找到第一个符合的就行

        print(f"Target Word: {target_word}")
        print('target_word_start,target_word_end:', target_word_start, target_word_end)

        # 计算左上角的相对坐标
        box_data_start = text_boxes_list[target_word_start].split()
        character_start, x_start, y_start, w_start, h_start = box_data_start[0], int(box_data_start[1]), int(
            box_data_start[2]), int(box_data_start[3]), int(box_data_start[4])
        left_top_relative_x_start = x_start / image_width
        left_top_relative_y_start = 1.0 - (y_start / image_height)
        print(f"Left Top Relative Coordinates: ({left_top_relative_x_start}, {left_top_relative_y_start})")
        # 计算右下角的相对坐标
        box_data_end = text_boxes_list[target_word_end].split()
        character_end, x_end, y_end, w_end, h_end = box_data_end[0], int(box_data_end[1]), int(box_data_end[2]), int(
            box_data_end[3]), int(box_data_end[4])
        left_top_relative_x_end = x_end / image_width
        left_top_relative_y_end = 1.0 - (y_end / image_height)
        print(f"Right Bottom Relative Coordinates: ({left_top_relative_x_end}, {left_top_relative_y_end})")


def f_png_to_tiff_one_file():
    pass
    input_png_path = r"C:\cc\software\ocr\train5\png\1.png"  # 替换为您的PNG文件路径
    output_tiff_path = r"C:\cc\software\ocr\train5\tif\1.tif"  # 替换为您想要保存的TIFF文件路径
    # 调用函数进行转换
    PictureMethod.png_to_tiff_one_file(input_png_path, output_tiff_path)

def f_png_to_tiff_batch():

    pass
    input_folder = r'C:\cc\software\ocr\train5\png'
    out_folder = r'C:\cc\software\ocr\train5\tif'
    PictureMethod.png_to_tiff_batch(input_folder,out_folder)

def f_get_word_pos_of_picture():
    pass
    image_path = r"C:\cc\share\temp\cc2.png"
    target_word = 'steps'
    PictureMethod.get_word_pos_of_picture(image_path,target_word)

    image_path = r"C:\cc\share\temp\cc3.png"
    target_word = 'testcase3'
    PictureMethod.get_word_pos_of_picture(image_path, target_word)


if __name__ == '__main__':    # 输入和输出文件路径
    print("我是main()")
    f_get_word_pos_of_picture()





