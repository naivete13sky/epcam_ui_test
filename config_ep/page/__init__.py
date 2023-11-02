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

engineering_entity_filter_coord = (120, 120)

engineering_jobList_first_coord = (80, 280)
engineering_jobList_onlyOneJob_empty_coord = (600, 600)
engineering_jobList_empty_coord = (800, 600)
engineering_job_list_in_job_empty_coord = (950, 210)

engineering_file_coord = (20, 40)
engineering_file_import_coord = (20, 210)
engineering_file_input_coord = (20, 160)
engineering_file_save_coord = (20, 250)
engineering_file_close_coord = (20, 275)

engineering_action_coord = (80, 40)
engineering_action_open_coord = (80, 90)
engineering_action_select_coord = (80, 70)
engineering_action_select_unselect_all_coord = (280, 95)

engineering_option_coord = (190, 40)
engineering_option_language_coord = (190, 60)
engineering_option_language_EP_Default_coord = (390, 60)
engineering_option_language_Simplified_Chinese_coord = (390, 110)

engineering_job_right_click_open_coord = (20, 10)

engineering_inJob_go_up_coord = (80, 250)
engineering_inJob_steps_coord = (80 + 260, 250)
engineering_inJob_steps_step_first_coord = (80 + 130, 250)

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

""" 以下为graphic模块信息"""
graphic_window_para = {'title': RunConfig.driver_epcam_ui_graphic_title, 'control_type': "Window"}
