import pyautogui

from config import RunConfig
from config_ep import page
import time
import cv2
import os
from cc.cc_method import opencv_compare
from cc.cc_method import PictureMethod
from config_ep.base.base import Base
from config_ep.base.base import MyMouse


class PageMatrix(Base,MyMouse):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数
        self.matrix_window = RunConfig.driver_epcam_ui.window(**page.matrix_window_pare)
        self.matrix_window_scroll_coord = None
        self.temp_path = RunConfig.temp_path_base

    def capture_image(self,img_name):
        """
        捉取图片
        :param img_name:
        :return:
        """
        self.matrix_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.matrix_window.capture_as_image()  # 截图
        save_path = os.path.join(self.temp_path, img_name + '.png')
        drill_correlation_layer_pic.save(save_path)  # 保存到硬盘
        return save_path

    def cut_img(self, img_path, img_name, cut_coords):
        """
        减切图像
        :param img_path:
        :param img_name:
        :param cut_coords:
        :return:
        """
        img = cv2.imread(img_path)
        img_cut = img[cut_coords[0]:cut_coords[1], cut_coords[2]:cut_coords[3]]  # 后面的是水平方向
        save_path_cut = os.path.join(self.temp_path, img_name + '_cut.png')
        cv2.imwrite(save_path_cut, img_cut)
        # img = cv2.imread(save_path_cut)
        # cv2.imshow("Cropped Image", img)
        cv2.waitKey(0)
        return save_path_cut
        # return save_path

    def is_right(self, save_path_cut, img_standard_str):
        """
        验证两张图片是否一致
        :param save_path_cut:
        :param img_standard_str:
        :return:
        """
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         img_standard_str)
        img_current_path = save_path_cut
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def close(self):
        """
        关闭Matrix窗口
        """
        self.matrix_window.child_window(title="关闭", control_type="Button").click_input()

    def get_drill_rout_count(self,layer_info):
        """
        得到layer中dirll和rout类型的数量
        :param layer_info:
        :return:
        """
        drill_rout_count = 0
        # 遍历字典中的值，检查'type'键对应的值是否为'drill'或'rout'
        for value in layer_info.values():
            value.get('type').lower()
            if value.get('type').lower() in ['drill', 'rout']:
                drill_rout_count += 1
        return drill_rout_count

    def check_layer_img(self, job_info, img_path):
        """
        验证layer图片（有物件和没有物件两种情况）
        :param job_info:
        """
        step_info = job_info.get('step_info')
        layer_info = job_info.get('layer_info')
        layer_feature_info = job_info.get('layer_feature_info')
        drill_rout_count = self.get_drill_rout_count(layer_info)
        sum = 0

        for step in layer_feature_info:
            steps = layer_feature_info.get(step)
            for layer in layer_feature_info.get(step):
                layers = steps.get(layer)
                if layers.get('features') == True:
                    img_standard_str = r'matrix\has_feature.png'
                else:
                    img_standard_str = r'matrix\not_has_feature.png'
                step_col = int(step_info.get(step.upper())['col'])
                layer_row = int(layer_info.get(layer.upper())['row'])

                img_name = 'layer_feature'
                coords = [192 + (layer_row - 1) * 30, 201  + (layer_row - 1) * 30,
                          172 + (step_col - 1) * 100 + drill_rout_count * 15, #水平方向
                          176 + (step_col - 1) * 100 + drill_rout_count * 15] #水平方向
                save_path_cut = self.cut_img(img_path, img_name, coords)
                print(step + "[" + step_info.get(step.upper()).get('col') + "]",
                      layer + "[" + layer_info.get(layer.upper()).get('row') + "]", layers)
                print("img_standard_str",img_standard_str)
                sum = sum + 1
                assert self.is_right(save_path_cut, img_standard_str)
                time.sleep(0.01)
        print("共验证了",sum,"个层别")

    def select_drill_cross(self, large_pic_path, small_pic_str, time_sleep = 0.5):
        small_pic_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                     small_pic_str)
        top_left, bottom_right = PictureMethod.get_small_pic_position_from_large_pic(small_pic_path, large_pic_path)
        x = int((top_left[0] + bottom_right[0]) / 2)
        y = int((top_left[1] + bottom_right[1]) / 2)
        print('x,y:', x, y)
        self.matrix_window.click_input(coords=(x,y)) # 选中drill关联线的顶部
        time.sleep(time_sleep)
        return x, y

    def change_drill_cross(self, job_info, layer, start_name, end_name):
        layer_info = job_info.get('layer_info')
        layer_name_row = int(layer_info.get(layer.upper())['row'])

        coords = (110, 200 + (layer_name_row - 1) * 30)
        self.matrix_click(coords)

        img_name = 'matrix_window'
        save_path = self.capture_image(img_name)  # 截图

        small_pic_str = r"matrix\drill_top.png"
        x, y = self.select_drill_cross(save_path, small_pic_str)  # 选中drill关联线的顶部
        start_name_row = int(layer_info.get(start_name.upper())['row'])
        start_coord_y = 200 + (start_name_row - 1) * 30
        MyMouse.mouse_simulator(440 + x, 106 + start_coord_y) # 移动孔带顶部

        small_pic_str = r"matrix\drill_bot.png"
        x, y = self.select_drill_cross(save_path, small_pic_str)  # 选中drill关联线的底部
        end_name_row = int(layer_info.get(end_name.upper())['row'])
        end_coord_y = 200 + (end_name_row - 1) * 30
        MyMouse.mouse_simulator(440 + x, 106 + end_coord_y) # 移动孔带底部

    def double_click_layer_has_step(self, job_info, step, layer):
        """
        双击有step的层别单元格
        :param job_info:
        :param step:
        :param layer:
        """
        step_info = job_info.get('step_info')
        layer_info = job_info.get('layer_info')
        drill_rout_count = self.get_drill_rout_count(layer_info)

        step_col = int(step_info.get(step.upper())['col'])
        layer_row = int(layer_info.get(layer.upper())['row'])
        coord_x = 220 + (step_col - 1) * 100 + drill_rout_count * 15
        coord_y = 200 + (layer_row - 1) * 30
        coords = (coord_x, coord_y)
        self.matrix_double_click(coords=coords) # 双击有step的layer单元格

    def double_click_step(self, job_info, step):
        """
        双击step
        :param job_info:
        :param step:
        """
        step_info = job_info.get('step_info')
        layer_info = job_info.get('layer_info')
        drill_rout_count = self.get_drill_rout_count(layer_info)

        step_col =  int(step_info.get(step.upper())['col'])
        coord_x  =220 + (step_col - 1) * 100 + drill_rout_count * 15
        coord_y = 160
        coords = (coord_x, coord_y)
        self.matrix_double_click(coords) # 双击

    def click_layer(self, job_info, layer):
        """
        单击层别
        :param job_info:
        :param layer:
        """
        layer_info = job_info.get('layer_info')
        drill_rout_count = self.get_drill_rout_count(layer_info)

        layer_row = int(layer_info.get(layer.upper())['row'])
        coord_x = 105 + drill_rout_count * 15
        coord_y = 200 + (layer_row - 1) * 30
        coords = (coord_x, coord_y)
        self.matrix_click(coords)

    def selections_layer(self,job_info,layer):
        """
        框选多个layer
        :param job_info:
        :param layer:
        """
        layer_info = job_info.get('layer_info')
        layer_row = int(layer_info.get(layer.upper())['row'])
        drill_rout_count = self.get_drill_rout_count(layer_info)

        coord_x = 535 + drill_rout_count * 15
        coord_y = 105 + 200 + (layer_row - 1) *  30
        MyMouse.mouse_simulator(coord_x, coord_y)

    def matrix_double_click(self, coords, time_sleep = 0.5):
        """
        matrix窗口双击
        :param coords:
        """
        self.matrix_window.double_click_input(coords=coords)
        time.sleep(time_sleep)

    def matrix_click(self,coords, time_sleep = 0.5):
        """
        matrix窗口单击
        :param coords:
        """
        self.matrix_window.click_input(coords=coords)
        time.sleep(time_sleep)

    def click_layer_test(self,job_info, layer, max_layer_row = 18, min_layer_row = 0):
        layer_info = job_info.get('layer_info')
        layer_row = int(layer_info.get(layer.upper())['row'])
        print("{}的row是{}".format(layer,layer_row))
        drill_rout_count = self.get_drill_rout_count(layer_info)
        if layer_row <= 18 and max_layer_row == 18 and min_layer_row == 0:
            print("进入第1个条件")
            coord_x = 105 + drill_rout_count * 15
            coord_y = 140 + 50 + layer_row * 30 - 15
            self.matrix_window.click_input(coords=(coord_x,coord_y))
        else:
            if 18 < layer_row and max_layer_row == 18 and min_layer_row == 0:
                print("进入第2个条件")
                self.matrix_window.click_input(coords=(1015,750))
                max_layer_row = 20
                min_layer_row = 1
            if layer_row > max_layer_row:
                print("进入第3个条件")
                diff = layer_row - max_layer_row
                coord_x = 105 + drill_rout_count * 15
                coord_y = 140 + 20 * 30 - 15
                print("{}的row比{}大{}".format(layer,max_layer_row,diff))
                for num in range(diff):
                    self.matrix_window.click_input(coords=(1015, 750))

                max_layer_row = layer_row
                min_layer_row = min_layer_row + diff

            elif layer_row < min_layer_row:
                print("进入第4个条件")
                diff = min_layer_row - layer_row
                print("{}比{}的row大{}".format(min_layer_row, layer, diff))
                coord_x = 105 + drill_rout_count * 15
                coord_y = 140 + 30 - 15
                print("diff:",diff)
                for num in range(diff):
                    self.matrix_window.click_input(coords=(1015, 145))

                max_layer_row = max_layer_row - diff
                min_layer_row = min_layer_row - diff

            else:
                print("进入第5个条件")
                coord_x = 105 + drill_rout_count * 15
                coord_y = 140 + (layer_row - 1) * 30 - 15
                if layer_row <= 20:
                    print("进入第6个条件")
                    coord_y = 140 + layer_row * 30 - 15
                if min_layer_row != 1:
                    print("进入第7个条件")
                    coord_y = 140 + (layer_row - (min_layer_row- 1)) * 30 - 15

            self.matrix_window.click_input(coords=(coord_x,coord_y))

        print("最大row:{}".format(max_layer_row))
        print("最小row:{}".format(min_layer_row))
        return max_layer_row,min_layer_row

    # def click_layer_top_from_layer(self):
    #     img_name = "matrix_window"
    #     large_pic_path = self.capture_image(img_name)
    #     # self.cut_img(r'C:\cc\share\temp\cc.png',"fisrt_row_second_col.png",[138,190, 35,189])
    #     small_pic_str = r"matrix\fisrt_row_second_col_2.png"
    #     small_pic_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
    #                                   small_pic_str)
    #     print("small_pic_path",small_pic_path)
    #     print("large_pic_path",large_pic_path)
    #     top_left, bottom_right=PictureMethod.get_small_pic_position_from_large_pic(small_pic_path, large_pic_path)
    #     print("top_left",top_left)
    #     print("bottom_right",bottom_right)
    #     self.cut_img(large_pic_path,'fisrt_row_second_col',[top_left[1],bottom_right[1],top_left[0],bottom_right[0]])
    #     return top_left, bottom_right