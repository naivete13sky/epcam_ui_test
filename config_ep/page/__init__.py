from config import RunConfig

""" 以下为engineering模块信息"""
engineering_window_para = {'title': RunConfig.driver_epcam_ui_engineering_title}  # engineering_window
engineering_import_window_child_window_para = {'title': "Import Job", 'control_type': "Window"}  # import job窗口
engineering_import_input_path_file_type_window_para = {
    'title': "文件类型(T):", 'auto_id': "1136", 'control_type': "ComboBox"}  # import job窗口，获得选择文件类型控件
engineering_import_input_path_file_path_window_para = {
    'title': "文件名(N):", 'auto_id': "1148", 'control_type': "ComboBox"}  # 选择文件窗口中的文件路径对象
engineering_import_input_path_confirm_window_para = {
    'title': "打开(O)", 'auto_id': "1", 'control_type': "Button"}  # 确认选择中的文件
engineering_input_window_child_window_para = {'title': "Input", 'control_type': "Window"}  # input job窗口
engineering_file_input_path_window_para = {'title': "Open", 'control_type': "Window"}  # input 选择文件窗口中的文件路径对象
engineering_file_save_window_para = {'title': "Save", 'control_type': "Window"}
engineering_output_window_child_window_para = {'title': "Output", 'control_type': "Window"}  # output窗口

engineering_entity_filter_coord = (120, 120)

engineering_jobList_first_coord = (80, 280)
engineering_jobList_onlyOneJob_empty_coord = (600, 600)
engineering_jobList_empty_coord = (800, 600)
engineering_job_list_in_job_empty_coord = (950, 210)

engineering_jobList_col_space = 135  # engineering窗口job图标x轴中心间距-张
engineering_jobList_row_space = 170  # engineering窗口job图标y轴中心间距-张

engineering_file_coord = (20, 40)
engineering_file_create_coord = (20, 65)
engineering_file_create_x_coord = (650, 350)
engineering_file_create_close_coord = (620, 440)
engineering_file_create_entity_filter_coord = (580, 380)
engineering_file_create_database_filter_coord = (580, 412)
engineering_file_create_database_button_coord = (420, 412)
engineering_file_create_ok_button_coord = (400, 445)
engineering_file_create_apply_button_coord = (535, 445)
engineering_file_create_yes_button_coord = (560, 440)
engineering_file_import_coord = (20, 210)
engineering_file_input_coord = (20, 160)
engineering_file_output_coord = (20, 185)
engineering_file_save_coord = (20, 250)
engineering_file_close_coord = (20, 275)

engineering_action_coord = (80, 40)
engineering_action_open_coord = (80, 90)
engineering_action_select_coord = (80, 70)
engineering_action_select_unselect_all_coord = (280, 95)
engineering_action_select_select_all_coord = (280, 60)

engineering_option_coord = (190, 40)
engineering_option_language_coord = (190, 60)
engineering_option_language_EP_Default_coord = (390, 60)
engineering_option_language_Simplified_Chinese_coord = (390, 110)
engineering_option_About_Us_coord = (190, 120)
engineering_option_close_About_Us_coord = (660, 505)

engineering_job_right_click_open_coord = (20, 10)

engineering_inJob_go_up_coord = (80, 250)
engineering_inJob_steps_coord = (80 + 260, 250)
engineering_inJob_steps_step_first_coord = (80 + 130, 250)
engineering_inJob_steps_step_fourth_coord = (80 + 520, 250)
engineering_inJob_matrix_coord = (80 + 130, 250)
engineering_inJob_symbols_coord = (80+390, 250)

""" 以下为engineering--import模块信息"""
engineering_file_import_input_path_coord = (30, 80)  # 变形时，字体太大，异常情况,y = 100
engineering_file_import_ok_coord = (30, 180)  # 变形时，字体太大，异常情况,y = 200


""" 以下为engineering--input模块信息"""
engineering_file_input_path_coord = (30, 55)
engineering_file_input_path_file_name_coord = (100, 395)
engineering_file_input_path_first_folder_coord = (170, 100)
engineering_file_input_path_open_coord = (600, 400)
engineering_file_input_job_lineedit_coord = (120, 80)
engineering_file_input_step_lineedit_coord = (520, 80)
engineering_file_input_identify_coord = (30, 705)
engineering_file_input_translate_coord = (250, 705)
engineering_file_input_file_first_right_coord = (100, 320)
engineering_file_input_file_right_click_menu_window_para = {'title': "EP-CAM", 'control_type': "Pane"}
engineering_file_input_file_right_click_menu_clear_coord = (20, 190)
engineering_file_input_close_coord = (700, 705)
engineering_file_input_file_first_select_coord = (30, 320)
engineering_file_input_file_row_height = 30
engineering_file_input_file_right_click_menu_select_all_coord = (20, 160)
engineering_file_input_file_right_click_menu_tool_size_edit_coord = (20, 100)
engineering_file_input_tool_size_edit_window_para = {'title': "ToolSize Edit", 'control_type': "Window"}
engineering_file_input_tool_size_edit_close_coord = (650, 680)
engineering_file_input_file_right_click_menu_dcode_edit_coord = (20, 75)
engineering_file_input_dcode_edit_window_para = {'title': "D code Edit", 'control_type': "Window"}
engineering_file_input_dcode_edit_close_coord = (650, 680)
engineering_file_input_file_right_click_menu_view_ascii_coord = (20, 50)
engineering_file_input_view_ascii_window_para = {
    'title': r"C:\cc\share\temp\268\compressed\760tbv01\0114-1240-1-10.drl", 'control_type': "Window"}
engineering_file_input_view_ascii_close_coord = (500, 800)

engineering_file_input_view_graphic_window_para = {'title': "EP-CAM", 'control_type': "Window"}
engineering_file_input_view_graphic_close_coord = (810, 155)

engineering_file_parameters_coord = (272, 320)
engineering_file_parameters_menu_coord = (300, 350)
engineering_file_input_view_graphic_coord = (272, 320)
engineering_file_input_view_graphic_menu_coord = (300, 330)
engineering_file_input_right_click_menu_coord = (300, 330)  # 右击层别栏，调出右击菜单栏
engineering_file_input_job_window_menu_coord = (56, 85)
engineering_file_input_job_window_close_menu_coord = (573, 617)
engineering_file_input_step_window_menu_coord = (455, 85)
engineering_file_input_step_window_close_menu_coord = (580, 617)


""" 以下为graphic模块信息"""
graphic_window_para = {'title': RunConfig.driver_epcam_ui_graphic_title, 'control_type': "Window"}
graphic_step_coord = (88, 40)
graphic_step_panelzation_coord = (88, 140)
graphic_step_panelization_by_table_coord = (320, 170)
graphic_by_table_new_step_coord = (350, 450)
graphic_by_table_new_step_pcs_coord = (700, 640)
graphic_by_table_new_step_pcs_ok_coord = (700, 755)
graphic_by_table_new_step_mirror_coord = (1050, 450)
graphic_by_table_new_step_mirror_yes_coord = (1050, 500)
graphic_by_table_window_close_coord = (1100, 380)
graphic_step_open_left_two_layer = (180, 190)
graphic_step_right_home = (1290, 70)
graphic_edit_coord = (88+66, 40)
graphic_edit_usersymbol_coord = (88+66, 288)
graphic_edit_usersymbol_angle_for_usersymbol_coord = (450, 315)
graphic_edit_usersymbol_angle_for_usersymbol_ok_coord = (745, 440)


'''右侧工具栏坐标'''
graphic_zoom_home_coord = (1295, 80)
graphic_feature_seletion_coord = (1210, 450)


grahic_left_layer_bar_row_height = 25  # graphic窗口左侧层别栏行高  -张
graphic_left_layer_bar_first_row_coord = (130, 175)  # graphic窗口左侧层别栏第一行的坐标 -张

graphic_canvas_centre_coord = (690, 400)  # graphic窗口画布中的坐标 -张
graphic_canvas_right_click_menu_window_para = {'title': "EP-CAM", 'control_type': "Pane"}
graphic_canvas_right_click_menu_measure_coords = (40, 60)

graphic_left_layer_bar_right_click_menu_window_para = {'title': "EP-CAM", 'control_type': "Pane"}
graphic_left_layer_bar_right_click_menu_copper_exposed_area_coords = (40, 200)  # layer右击copper/exposed area坐标 -张
graphic_left_layer_bar_right_click_menu_multi_layer_copy_coords = (40, 160)  # layer右击multi layer copy坐标 -张

graphic_copper_exposed_area_window_para = {'title': "Copper/Exposed Area", 'control_type': "Window"}
graphic_copper_exposed_area_measurement_copper_area_coords = (113, 51)  # copper_area单选按钮坐标 -张
graphic_copper_exposed_area_measurement_exposed_area_coords = (213, 51)  # exposed_area单选按钮坐标 -张
graphic_copper_exposed_area_apply_button_coords = (100, 205)  # button按钮坐标 -张
graphic_copper_exposed_area_warning_window_para = {'title': "warning", 'control_type': "Window"}


graphic_multi_layer_copy_window_para = {'title': "Multi Layer Copy", 'control_type': "Window"}
graphic_multi_layer_copy_source_step_button_coords = (60, 85)
graphic_multi_layer_copy_add_layers_button_coords = (60, 115)
graphic_multi_layer_copy_suffix_text_coords = (160, 150)
graphic_multi_layer_copy_ok_button_coords = (60, 540)

graphic_multi_layer_copy_steps_pop_window_para = {'title': "Steps Popup", 'control_type': "Window"}
graphic_multi_layer_copy_steps_pop_row_spacing = 20
graphic_multi_layer_copy_steps_pop_first_row_coords = (40, 80)

graphic_multi_layer_copy_layers_pop_window_para = {'title': "Layers Popup", 'control_type': "Window"}
graphic_multi_layer_copy_layers_pop_row_spacing = 20
graphic_multi_layer_copy_layers_pop_first_row_coords = (40, 80)
graphic_multi_layer_copy_layers_pop_ok_button_coords = (70, 320)

graphic_multi_layer_copy_information_window_para = {'title': "Information", 'control_type': "Window"}
graphic_multi_layer_copy_information_ok_button_coords = (150, 110)


graphic_measuremen_mark_window_para = {'title': "Measurement Mark", 'control_type': "Window"}
graphic_measuremen_mark_first_mode_coords = (25, 75)  # Measuremen Mark窗口第一个mode的坐标 -张
graphic_measuremen_mark_mode_spacing = 27  # mode间距 -张

""" 以下为matrix模块信息"""
matrix_window_pare = {'title': RunConfig.driver_epcam_ui_matrix_title, 'control_type': "Window"}  # -张
