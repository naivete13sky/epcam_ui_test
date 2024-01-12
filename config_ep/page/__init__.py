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

engineering_create_window_para = {'title': "Create", 'control_type': "Window"}
create_entity_name_input_coord = (200, 55)
create_database_input_coord = (200, 85)
create_database_button_coord = (65, 85)
create_ok_button_coord = (55, 120)
create_apply_button_coord = (160, 120)
create_close_button_coord = (260, 120)
engineering_create_information_window_para = {'title': "Information", 'control_type': "Window"}
create_information_yes_button_coord = (240, 100)
create_information_no_button_coord = (320, 100)

engineering_file_import_coord = (20, 210)
engineering_file_input_coord = (20, 160)
engineering_file_output_coord = (20, 185)
engineering_file_output_close_coord = (845, 735)
engineering_file_save_coord = (20, 250)
engineering_file_close_coord = (20, 275)
engineering_file_delete_coord=(75, 137)
engineering_file_delete_yes_coord=(550, 440)
engineering_file_delete_ok_coord=(550, 440)

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
engineering_inJob_steps_step_first_coords = (80 + 130, 250)
engineering_injob_steps_right_click_step_delete_coords = (246, 300)  # 朱
engineering_inJob_matrix_coord = (80 + 130, 250)
engineering_inJob_symbol_Left_clickon1_coord = (1012, 760)  # 朱
engineering_inJob_symbol_Left_clickon2_coord = (1012, 230)  # 朱


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

engineering_file_input_parametes_window_para = {'title': "Parameters Popup", 'control_type': "Window"} # 朱
engineering_file_parameters_open_menu_coord = (285, 355)  # 朱

engineering_file_input_jobs_window_para = {'title': "Jobs Popup", 'control_type': "Window"}  # 朱
engineering_file_input_jobs_menu_coord = (56, 85)  # 朱

engineering_file_input_steps_window_para = {'title': "Steps Popup", 'control_type': "Window"}  # 朱
engineering_file_input_steps_window_menu_coord = (455, 85)  # 朱

engineering_file_input_right_click_menu_coord = (240, 322)  # 右键单击Input视窗的层别栏，调出右击菜单栏  # 朱


engineering_file_input_view_graphic_menu_coord = (285, 328)  # 朱





""" 以下为graphic模块信息"""
graphic_window_para = {'title': RunConfig.driver_epcam_ui_graphic_title, 'control_type': "Window"}

graphic_step_open_left_two_layer = (180, 190)
graphic_step_right_home = (1290, 70)

'''右侧工具栏坐标'''
graphic_first_layer_coord = (97, 175)
graphic_right_feature_selection_coord = (1195, 440)
graphic_select_canvas_feature_coord = (370,485)
graphic_right_home = (1290, 70)
graphic_edit_coord = (150, 40)
graphic_edit_usersymbol_coord = (170, 288)
graphic_edit_usersymbol_creat_usersymbol_coord = (520, 288)
graphic_edit_usersymbol_creat_usersymbol_symbolname_coord = (740, 380)
graphic_edit_usersymbol_creat_button_ok_coord = (670, 590)
graphic_edit_usersymbol_creat_button_ok_information_coord = (865, 525)
graphic_step_robotcam_ok_information_window_coord = (440, 415)
graphic_step_robotcam_close_coord = (815, 12)
graphic_analysis_solder_mask_coord = (400, 145)
graphic_analysis_solder_mask_run_globally_coord =(665, 880)


""" 以下为matrix模块信息"""
matrix_window_pare = {'title': RunConfig.driver_epcam_ui_matrix_title, 'control_type': "Window"}  # -张
