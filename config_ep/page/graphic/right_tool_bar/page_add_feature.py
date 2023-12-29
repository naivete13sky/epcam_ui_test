import os
import re
import time
import cv2
from pywinauto.keyboard import send_keys
from cc.cc_method import opencv_compare
from config import RunConfig
from config_ep import page
from config_ep.page.graphic import right_tool_bar

class PageAddFeature(object):
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)

        # 切换到Add Feature子窗口
        self.add_feature_window = self.graphic_window.child_window(
            **right_tool_bar.add_feature_window_para)

        self.temp_path = RunConfig.temp_path_base

    def close(self):
        self.add_feature_window.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.add_feature_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.add_feature_window.capture_as_image()  # 截图
        save_path = os.path.join(self.temp_path, img_name + '.png')
        drill_correlation_layer_pic.save(save_path)  # 保存到硬盘
        return save_path

    def cut_img(self, img_path, img_name, cut_coords):
        img = cv2.imread(img_path)
        img_cut = img[cut_coords[0]:cut_coords[1], cut_coords[2]:cut_coords[3]]  # 后面的是水平方向
        save_path_cut = os.path.join(self.temp_path, img_name + '_cut.png')
        cv2.imwrite(save_path_cut, img_cut)
        cv2.waitKey(0)
        return save_path_cut

    def is_right(self,save_path_cut, img_standard_str):
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         img_standard_str)
        img_current_path = save_path_cut
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def click_fueature_radio(self,feature_index):
        coord_x = right_tool_bar.add_feature_first_radio_button_coords[0] + (
                feature_index - 1) * right_tool_bar.add_feature_radio_button_spacing
        coords_y = right_tool_bar.add_feature_first_radio_button_coords[1]
        self.add_feature_window.click_input(coords=(coord_x,coords_y))

    def click_extractor_button(self):
        self.add_feature_window.click_input(coords=right_tool_bar.add_feature_extractor_coord)

class AddPad(PageAddFeature):
    def add_pad(self,symbol_name:str,symbol_standard=False):
        self.click_fueature_radio(2)
        self.add_feature_window.click_input(coords=right_tool_bar.add_pad_symbol_button_coords)
        self.symbol=PageSymbol()
        if symbol_standard:
            self.symbol.click_symbol(symbol_name)
        self.close()

class PageSymbol():
    def __init__(self):
        self.graphic_window = RunConfig.driver_epcam_ui.window(**page.graphic_window_para)
        # 切换到Symbol子窗口
        self.symbole_window = self.graphic_window.child_window(
            **right_tool_bar.symbol_window_para)

        self.temp_path = RunConfig.temp_path_base

        # self.symbol_window_path = self.capture_image("symbol_window")

    def close(self):
        self.symbole_window.child_window(title="关闭", control_type="Button").click_input()

    def capture_image(self, img_name):
        self.symbole_window.set_focus()  # 激活窗口
        time.sleep(0.1)
        drill_correlation_layer_pic = self.symbole_window.capture_as_image()  # 截图
        save_path = os.path.join(self.temp_path, img_name + '.png')
        drill_correlation_layer_pic.save(save_path)  # 保存到硬盘
        return save_path

    def click_symbol(self,symbol_name):
        symbol_type = re.search(r'^.*?(?=\d)', symbol_name).group(0)
        print("symbol",symbol_type)

        dict_symbol_standard = {
            'r': {'name': 'round', 'col':1, 'row':1, 'param' : {'r_diameter'}},
            's': {'name': 'square', 'col':2, 'row':1, 'param' : {'r_diameter'}},
            'rect': {'name': 'rectangle', 'col':3, 'row':1, 'param' : {'rect_width','rect_height'}},
            'rect_r': {'name': 'rect_r', 'col':4, 'row':1,'param' : {'rect_r_width':0,'rect_r_height':1,'rect_r_corner_radius':2},'type':{1:'rect_1',2:'rect_2',3:'rect_3',4:'rect_4'}},
            'rect_c': {'name': 'rect_c', 'col':1, 'row':2,'param' : {'rect_c_width':0,'rect_c_height':1,'rect_c_corner_radius':2},'type':{1:'rect_1',2:'rect_2',3:'rect_3',4:'rect_4'}},
            'oval': {'name': 'oval', 'col':2, 'row':2, 'param' : {'oval_width':0, 'oval_height':1}},
            'di': {'name': 'diamond', 'col':3, 'row':2, 'param' : {'diamond_width', 'diamond_height'}},
            'oct': {'name': 'octagon', 'col':4, 'row':2, 'param' : {'oct_width':0, 'oct_height':1, 'oct_corner_radius':2}},
            'donut_r': {'name': 'round_donut', 'col':1, 'row':3, 'param' : {'round_donut_outer_diam':0, 'round_donut_inner_diam':1}},
            'donut_s': {'name': 'square_donut', 'col':2, 'row':3, 'param' : {'square_donut_outer_diam':0, 'square_donut_inner_diam':1}},
            'hex_l': {'name': 'laying_hexagon', 'col':3, 'row':3, 'param' : {'hex_l_width':0, 'hex_l_height':1, 'hex_l_corner_radius':2}},
            'hex_s': {'name': 'standing_hexagon', 'col':4, 'row':3, 'param' : {'hex_s_width':0, 'hex_s_height':1, 'hex_s_corner_radius':2}},
            'bfr': {'name': 'round_butterfly', 'col':1, 'row':4, 'param' : {'r_diameter'}},
            'bfs': {'name': 'square_butterfly', 'col':2, 'row':4, 'param' : {'r_diameter'}},
            'tri': {'name': 'triangle', 'col':3, 'row':4, 'param' : {'triangle_base':0, 'triangle_height':1}},
            'oval_h': {'name': 'half_oval', 'col':4, 'row':4, 'param' : {'half_oval_width':0, 'half_oval_height':1}},
            'thr': {'name': 'round_round_thermal', 'col':1, 'row':5, 'param' : {'th_out':0, 'th_in':1, 'th_angle':2, 'th_num':3, 'th_spokes':4},'type':{0:'corner_style_1'}},
            'ths': {'name': 'round_round_thermal', 'col':1, 'row':5, 'param' : {'th_out':0, 'th_in':1, 'th_angle':2, 'th_num':3, 'th_spokes':4},'type':{0:'corner_style_2'}},
            's_ths': {'name': 'square_square_thermal', 'col':2, 'row':5, 'param' : {'th_out':0, 'th_in':1, 'th_angle':2, 'th_num':3, 'th_spokes':4},'type':{0:'corner_style_1'}},
            's_tho': {'name': 'square_square_thermal', 'col':2, 'row':5, 'param' : {'th_out':0, 'th_in':1, 'th_angle':2, 'th_num':3, 'th_spokes':4},'type':{0:'corner_style_2'}},
            'sr_ths': {'name': 'square_round_thermal', 'col':3, 'row':5, 'param' : {'sr_out':0, 'sr_in':1, 'sr_angle':2, 'sr_num':3, 'sr_spokes':4}},
            'rc_ths': {'name': 'rect_rect_thermal', 'col':4, 'row':5, 'param' : {'rc_out_w':0, 'rc_in_h':1, 'rc_angle':2, 'rc_num':3, 'rc_spokes':4, 'rc_air':5},'type':{0:'corner_style_1'}},
            'rc_tho': {'name': 'rect_rect_thermal', 'col':4, 'row':5, 'param' : {'rc_out_w':0, 'rc_in_h':1, 'rc_angle':2, 'rc_num':3, 'rc_spokes':4, 'rc_air':5},'type':{0:'corner_style_2'}},
            'el': {'name': 'ellipse', 'col':1, 'row':6, 'param' : {'ellipse_width':0, 'ellipse_height':1}},
            'moire': {'name': 'moire', 'col':2, 'row':6, 'param' : {'moire_r_w':0, 'moire_r_g':1, 'moire_n_r':2, 'moire_l_w':3, 'moire_l_g':4, 'moire_l_a':5}},
            'hole': {'name': 'hole', 'col':3, 'row':6, 'param': {'hole_d':0, 'hole_t_add':1, 'hole_t_sub':2},'type':{0:'h_t',1:'h_t_v',2:'h_t_n',3:'h_t_p'}},
            'null': {'name': 'null', 'col':4, 'row':6, 'param' : {'r_diameter'}}
        }

        if symbol_type == 'rect':
            x_count = len(re.findall(r'x', symbol_name))
            if x_count > 1:
                match = re.search(r'x.*?x([rc])(\d+)', symbol_name)
                if match.group(1) == 'r':
                    symbol_type = symbol_type + '_r'
                elif match.group(1) == 'c':
                    symbol_type = symbol_type + '_c'
        # self.click_symbol_radio_button(symbol_type)
        self.click_symbol_radio_button_by_coords(dict_symbol_standard,symbol_type)

        num = 0
        for symbol_param in dict_symbol_standard[symbol_type]['param']:
            text = re.findall(r'\d+', symbol_name)[num]
            self.send_keys_to_symbol(symbol_param,text)
            num = num + 1

        if symbol_type in ['rect_r','rect_c']:
            self.select_rect_type(dict_symbol_standard,symbol_name,symbol_type)

        if symbol_type in ['thr','ths','s_ths','s_tho','rc_ths','rc_tho']:
            self.select_corner_style(dict_symbol_standard, symbol_type)

        if symbol_type == 'hole':
            self.select_hole_type(dict_symbol_standard, symbol_name, symbol_type)

        self.click_apply()
        self.close()

    def click_symbol_radio_button_by_img(self, symbol_type):
        """
        根据symbol图片点击symbol单选按钮
        :param symbol_type:
        """
        from cc.cc_method import PictureMethod
        # large_pic_path = r'C:\cc\share\temp\symbol_window.png'
        large_pic_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                      'graphic','symbol_standard','symbol_window.png')
        small_pic_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                      'graphic','symbol_standard',symbol_type + '.png')
        # small_pic_path = os.path.join(self.temp_path, 'symbols', symbol_type + '.png')
        top_left, bottom_right = PictureMethod.get_small_pic_position_from_large_pic(small_pic_path, large_pic_path)
        x = int((top_left[0] + bottom_right[0]) / 2)
        y = int((top_left[1] + bottom_right[1]) / 2)
        print('x,y:', x, y)
        self.symbole_window.click_input(coords=(x, y))

    def click_symbol_radio_button_by_coords(self,dict_symbol_standard,symbol_type):
        """
        根据symbol的行和列点击symble单选按钮
        :param symbol_col:
        :param symbol_row:
        """
        symbol_col = dict_symbol_standard[symbol_type]['col']
        symbol_row = dict_symbol_standard[symbol_type]['row']
        first_button = right_tool_bar.symbol_first_radio_button_coords
        x_spacing = right_tool_bar.symbol_radio_button_x_spacing
        y_spacing = right_tool_bar.symbol_radio_button_y_spacing
        coord_x = first_button[0] + (symbol_col - 1) * x_spacing
        coord_y = first_button[1] + (symbol_row - 1) * y_spacing
        self.symbole_window.click_input(coords=(coord_x, coord_y))

    def send_keys_to_symbol(self, symbol_param, text):
        """
        输入图形
        :param coords:
        :param keys:
        """
        x,y =self.get_symbol_param_coords(symbol_param)
        self.symbole_window.click_input(coords=(x,y))
        send_keys("^a")
        send_keys(text)

    def get_symbol_param_coords(self,symbol_param,coord_x=100,coord_y=15):
        """
        获取symbol参数文本坐标
        :param symbol_param:
        :param coord_x:
        :param coord_y:
        :return:
        """
        from cc.cc_method import PictureMethod
        # large_pic_path = r'C:\cc\share\temp\symbol_window.png'
        large_pic_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                      'graphic', 'symbol_standard', 'symbol_window.png')
        small_pic_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                      'graphic', 'symbol_standard', symbol_param + '.png')
        top_left, bottom_right = PictureMethod.get_small_pic_position_from_large_pic(small_pic_path, large_pic_path)
        x = int(bottom_right[0] - coord_x)
        y = int(bottom_right[1] - coord_y)
        return x,y

    def select_hole_type(self,dict_symbol_standard, symbol_name, symbol_type):
        """
        选择Hole type
        :param dict_symbol_type:
        :param symbol_t
        """
        x, y = self.get_symbol_param_coords(dict_symbol_standard[symbol_type]['type'][0])
        self.symbole_window.click_input(coords=(x, y))
        type = re.search(r'x([vnp])x', symbol_name)
        if type.group(1) == 'v':
            x, y = self.get_symbol_param_coords(dict_symbol_standard[symbol_type]['type'][1])
            self.symbole_window.click_input(coords=(x, y))
        elif type.group(1) == 'n':
            x, y = self.get_symbol_param_coords(dict_symbol_standard[symbol_type]['type'][2])
            self.symbole_window.click_input(coords=(x, y))
        elif type.group(1) == 'p':
            x, y = self.get_symbol_param_coords(dict_symbol_standard[symbol_type]['type'][3])
            self.symbole_window.click_input(coords=(x, y))

    def select_corner_style(self,dict_symbol_standard, symbol_type):
        """
        选择Corner Styly
        :param dict_symbol_standard:
        :param symbol_type
        """
        coord_x = 15
        coord_y = 10
        x, y = self.get_symbol_param_coords(dict_symbol_standard[symbol_type]['type'][0], coord_x, coord_y)
        self.symbole_window.click_input(coords=(x, y))

    def select_rect_type(self,dict_symbol_standard,symbol_name,symbol_type):
        """
        选择Rect Type
        :param dict_symbol_standard:
        :param symbol_name:
        :param symbol_type:
        """
        coord_x = 15
        coord_y = 10
        match = re.search(r'x.*?x.*?x(\d+)', symbol_name)
        if match == None:
            for num in dict_symbol_standard[symbol_type]['type']:
                # print(dict_symbol_type[symbol_type]['type'][type])
                x, y = self.get_symbol_param_coords(dict_symbol_standard[symbol_type]['type'][num],coord_x,coord_y)
                self.symbole_window.click_input(coords=(x, y))
        else:
            for num in match.group(1):
                # print(dict_symbol_type[symbol_type]['type'][int(num)])
                x, y = self.get_symbol_param_coords(dict_symbol_standard[symbol_type]['type'][int(num)],coord_x,coord_y)
                self.symbole_window.click_input(coords=(x, y))

    def click_apply(self):
        self.symbole_window.click_input(coords=right_tool_bar.symbol_apply_button_coords)
