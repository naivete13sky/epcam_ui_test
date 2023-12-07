import os
import cv2
import time
from config_ep import page
from config import RunConfig
from cc.cc_method import opencv_compare
from pywinauto.keyboard import send_keys


class PageFile(object):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数
        self.engineering_window = RunConfig.driver_epcam_ui.window(**page.engineering_window_para)

    def open_create_window(self):
        self.engineering_window.click_input(coords=page.engineering_file_coord)  # 单击打开File菜单
        self.engineering_window.click_input(coords=page.engineering_file_create_coord)  # 单击打开Create窗口

    def close_create_window(self, button):
        if button == 'x':
            self.engineering_window.click_input(coords=page.engineering_file_create_x_coord)  # 右上角X关闭窗口
        elif button == 'close':
            self.engineering_window.click_input(coords=page.engineering_file_create_close_coord)  # close按钮关闭

    def create_window_is_closed(self):
        engineering_file_create_entity_pic = self.engineering_window.capture_as_image()  # 截图
        engineering_file_create_entity_pic.save(r'C:\cc\share\temp\create_window_is_closed_pic.png')  # 保存到硬盘
        img = cv2.imread(r'C:\cc\share\temp\create_window_is_closed_pic.png')
        img_cut = img[55:780, 200:810]  # 前面纵向，后面横向
        cv2.imwrite(r"C:\cc\share\temp\create_window_is_closed_pic_cut.png", img_cut)
        cv2.waitKey(0)
        # 加载两张图片
        img_standard_path = os.path.join(RunConfig.epcam_ui_standard_pic_base_path,
                                         r'engineering\create_window_is_closed_pic_cut_standard.png')  # 要改图片
        img_current_path = r'C:\cc\share\temp\create_window_is_closed_pic_cut.png'
        rectangle_count = opencv_compare(img_standard_path, img_current_path)
        return rectangle_count == 0

    def entity_name_input(self):
        self.engineering_window.click_input(coords=page.engineering_file_create_entity_filter_coord)
        send_keys('666abc-')
        send_keys('+{_}')
        send_keys('+{+}')
        send_keys('{TAB}')  # Tab切走，光标影响截图

    def entity_name_illegal_input(self):
        self.engineering_window.click_input(coords=page.engineering_file_create_entity_filter_coord)
        send_keys('ABC')
        send_keys('!@#$')
        send_keys('你瞅啥？')
        send_keys('{TAB}')  # Tab切走，光标影响截图

    def clear_entity_name(self):
        self.engineering_window.click_input(coords=page.engineering_file_create_entity_filter_coord)
        send_keys('^a')
        send_keys('{BACK}')  # 输入框全选删除

    def database_reset(self):
        self.engineering_window.click_input(coords=page.engineering_file_create_database_filter_coord)
        send_keys('^a')
        send_keys('{BACK}')
        time.sleep(0.2)
        self.engineering_window.click_input(coords=page.engineering_file_create_database_button_coord)
        self.engineering_window.click_input(coords=page.engineering_file_create_database_filter_coord)
        send_keys('^a')
        send_keys('{BACK}')
        send_keys('666abc-')
        send_keys('+{_}')
        send_keys('+{+}')
        send_keys('ABC')
        send_keys('!@#$')
        send_keys('你说啥？')
        time.sleep(0.2)
        self.engineering_window.click_input(coords=page.engineering_file_create_database_button_coord)
        self.engineering_window.click_input(coords=page.engineering_file_create_database_filter_coord)
        send_keys('666abc-')
        send_keys('+{_}')
        send_keys('+{+}')
        send_keys('ABC')
        send_keys('!@#$')
        send_keys('你说啥？')
        time.sleep(0.2)
        self.engineering_window.click_input(coords=page.engineering_file_create_database_button_coord)

    def create_job(self, job_name, button):
        self.engineering_window.click_input(coords=page.engineering_file_create_entity_filter_coord)
        send_keys(job_name)
        if button == 'ok':
            self.engineering_window.click_input(coords=page.engineering_file_create_ok_button_coord)
        elif button == 'apply':
            self.engineering_window.click_input(coords=page.engineering_file_create_apply_button_coord)
        self.engineering_window.click_input(coords=page.engineering_file_create_yes_button_coord)
