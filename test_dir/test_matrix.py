import os

import pytest
from config_ep.page.page_engineering import PageEngineering
from cc.cc_method import GetTestData, PictureMethod
from config_ep.page.matrix.page_matrix import PageMatrix
from config_ep.page.page_view_graphic import PageViewGraphic
from config_ep.page.graphic.page_graphic import PageGraphic
from config_ep.base.base import MyODB


class Test_Matrix_UI:
    def setup_method(self):
        self.engineering = PageEngineering()
        # self.engineering.engineering_window.set_focus()  # 激活窗口
        self.graphic = PageGraphic()
        self.view_graphic = PageViewGraphic()
        self.matrix = PageMatrix()

    @pytest.mark.matrix
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Change_Matrix'))
    def test_matrix_ui_all(self, job_id,epcam_ui_start,
                           download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        验证matrix窗口
        禅道用例ID：4608
        :param job_id:42983
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(
            job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_matrix_by_double_click()  # 双击Matrix,打开Matrix窗口

        img_name = 'matrix_window'

        img_path = self.matrix.capture_image(img_name) # 捉取图片

        cut_coords = [30, 60, 10, 42]  # File菜单，后面的是水平方向
        save_path_cut = self.matrix.cut_img(img_path, img_name, cut_coords) #剪切图像
        text = PictureMethod.get_text_from_img(save_path_cut)
        assert text == "File\n" # 验证matrix窗口中存在file菜单

        cut_coords = [30, 60, 75, 104]  # Edit菜单，后面的是水平方向
        save_path_cut = self.matrix.cut_img(img_path, img_name, cut_coords)
        text = PictureMethod.get_text_from_img(save_path_cut)
        assert text == "Edit\n" # 验证matrix窗口中存在edit菜单

        cut_coords = [30, 60, 135, 184]  # Option菜单，后面的是水平方向
        save_path_cut = self.matrix.cut_img(img_path, img_name, cut_coords)
        text = PictureMethod.get_text_from_img(save_path_cut)
        assert text == "Option\n" # 验证matrix窗口中存在option菜单

        width_scale_factor = 3.1 # 图片宽度缩放比例
        height_scale_factor = 2.3 # 图片高度缩放比例
        # illegals = [' ', '_', '-'] # 非法字符集合
        # case = 'lower' # 英文大、小写
        cut_coords = [60, 90, 15, 1025] # job名，后面的是水平方向
        save_path_cut = self.matrix.cut_img(img_path, img_name, cut_coords)
        text = PictureMethod.get_text_from_img(save_path_cut, width_scale_factor, height_scale_factor)
        # for illegal in illegals:
        #     job_name = job_name.replace(illegal,'')
        job_name = 'Job : ' + job_name + '\n'
        assert text == job_name # 验证matrix窗口的job名和测试料号是否一致

        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 得到odb的matrix文件路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        odb_steps_folder_path = os.path.join(odb_folder_path, 'steps')
        job_info["step_info"] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info["layer_info"] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        job_info["layer_feature_info"] = MyODB.get_layer_featur_from_odb_file(odb_steps_folder_path)
        self.matrix.check_layer_img(job_info, img_path) # 验证matrix窗口每个layer图片

        cut_coords = [759, 788, 400, 600]  # Close按钮，后面的是水平方向
        save_path_cut = self.matrix.cut_img(img_path, img_name, cut_coords)
        text = PictureMethod.get_text_from_img(save_path_cut, width_scale_factor, height_scale_factor)
        assert text == "close\n"  # 验证matrix窗口中存在close按钮

        self.matrix.close()  # 关闭matrix窗口
        self.engineering.go_up()  # 鼠标双击go_up

    @pytest.mark.matrix
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Change_Matrix'))
    def test_matrix_change_drill_cross(self,job_id,epcam_ui_start,
                                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        调整孔带
        禅道用例ID：4608
        :param job_id:42983
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_matrix_by_double_click() # 双击Matrix,打开Matrix窗口

        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 得到odb的matrix文件路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file) # 得到料号layer信息

        self.matrix.change_drill_cross(job_info,'drl1-10','top','bot') # 修改孔带

        img_name = 'drill_cross'
        img_path = self.matrix.capture_image(img_name)
        cut_coords = [100, 799, 8, 1032] # 后面的是水平方向
        save_path_cut = self.matrix.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "matrix\\" + img_name + "_cut_standard.png"
        assert self.matrix.is_right(save_path_cut, img_standard_str)
        self.matrix.close()  # 关闭matrix窗口
        self.engineering.go_up()  # 鼠标双击go_up

    @pytest.mark.matrix
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Change_Matrix'))
    def test_matrix_double_click_layer_has_step(self, job_id, epcam_ui_start,
                                                   download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        双击有step名的对应layer单元格
        禅道用例ID：4194
        :param job_id:42983
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_matrix_by_double_click()  # 双击Matrix,打开Matrix窗口

        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 得到odb的matrix文件路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)

        self.matrix.double_click_layer_has_step(job_info,'orig','top') # 双击有step的layer单元格

        img_name = 'view_graphic_window'
        img_path = self.view_graphic.capture_image(img_name)
        cut_coords = [30, 511, 8, 648]  # 后面的是水平方向
        save_path_cut = self.view_graphic.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "engineering\\" + img_name + "_cut_standard.png"
        assert self.view_graphic.is_right(save_path_cut, img_standard_str)
        self.view_graphic.close()

        self.matrix.close()
        self.engineering.go_up()

    @pytest.mark.matrix
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Change_Matrix'))
    def test_matrix_double_click_step(self, job_id, epcam_ui_start,
                                                download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        双击有step名的对应layer单元格
        禅道用例ID：4193
        :param job_id:42983
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_matrix_by_double_click()  # 双击Matrix,打开Matrix窗口

        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 得到odb的matrix文件路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info['step_info'] = MyODB.get_step_info_from_odb_file(odb_matrix_file)
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)

        self.matrix.double_click_step(job_info, 'orig')  # 双击有step的layer单元格

        img_name = 'matrix_to_graphic_window'
        img_path = self.graphic.capture_image(img_name)
        cut_coords = [30, 799, 8, 1374] # 截图坐标，后面的是水平方向
        save_path_cut = self.graphic.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "graphic\\" + img_name + "_cut_standard.png"
        self.graphic.is_right(save_path_cut, img_standard_str)

        self.graphic.close()
        self.matrix.close()
        self.engineering.go_up()

    @pytest.mark.matrix
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Change_Matrix'))
    def test_matrix_click_layer(self, job_id, epcam_ui_start,
                                      download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        单击layer名后显示
        禅道用例ID：4182
        :param job_id:42983
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_matrix_by_double_click()  # 双击Matrix,打开Matrix窗口

        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 得到odb的matrix文件路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)
        self.matrix.click_layer(job_info, 'top')  # 单击layer

        img_name = 'click_layer'
        img_path = self.matrix.capture_image(img_name)
        cut_coords = [100, 799, 8, 1032]  # 后面的是水平方向
        save_path_cut = self.matrix.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "matrix\\" + img_name + "_cut_standard.png"
        assert self.matrix.is_right(save_path_cut, img_standard_str)

        self.matrix.close()
        self.engineering.go_up()

    @pytest.mark.matrix
    @pytest.mark.parametrize("job_id", GetTestData().get_job_id('Change_Matrix'))
    def test_matrix_selections_layer(self, job_id, epcam_ui_start,
                                download_file_compressed_entity_filter_delete_all_jobs_import):
        """
        选中多层layer后
        禅道用例ID：4183
        :param job_id:42983
        :param epcam_ui_start:
        :return:
        """
        job_name, file_compressed_path = download_file_compressed_entity_filter_delete_all_jobs_import(job_id)  # 调用 fixture 并传递参数值,下载料号
        self.engineering.open_job_first_by_double_click()  # 双击打开料号
        self.engineering.open_matrix_by_double_click()  # 双击Matrix,打开Matrix窗口

        job_info = {}
        odb_folder_path = MyODB.get_odb_folder_path(file_compressed_path)  # 得到odb的matrix文件路径
        odb_matrix_file = os.path.join(odb_folder_path, r'matrix\matrix')
        job_info['layer_info'] = MyODB.get_layer_info_from_odb_file(odb_matrix_file)

        self.matrix.click_layer(job_info, 'top')  # 单击layer

        self.matrix.selections_layer(job_info,'bot') # 选中多层layer

        img_name = 'selections_layer'
        img_path = self.matrix.capture_image(img_name)
        cut_coords = [100, 799, 8, 1032]  # 后面的是水平方向
        save_path_cut = self.matrix.cut_img(img_path, img_name, cut_coords)
        img_standard_str = "matrix\\" + img_name + "_cut_standard.png"
        assert self.matrix.is_right(save_path_cut, img_standard_str)

        self.matrix.close()
        self.engineering.go_up()


