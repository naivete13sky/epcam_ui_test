from config import RunConfig

""" 以下为engineering模块信息"""
engineering_window_para = {'title': RunConfig.driver_epcam_ui_engineering_title} # engineering_window
engineering_import_window_child_window_para = {'title': "Import Job", 'control_type': "Window"} # import job窗口
engineering_import_input_path_file_type_window_para = {'title': "文件类型(T):", 'auto_id': "1136",'control_type': "ComboBox"} # import job窗口，获得选择文件类型控件
engineering_import_input_path_file_path_window_para = {'title': "文件名(N):", 'auto_id': "1148",'control_type': "ComboBox"} # 选择文件窗口中的文件路径对象
engineering_import_input_path_confirm_window_para = {'title': "打开(O)", 'auto_id': "1", 'control_type': "Button"} # 确认选择中的文件
engineering_input_window_child_window_para = {'title': "Input", 'control_type': "Window"} # input job窗口
engineering_input_path_file_path_window_para = {'title': "Open", 'control_type': "Window"} # input 选择文件窗口中的文件路径对象

engineering_entity_filter_coor = (120, 120)

engineering_jobList_first_coor = (80, 280)
engineering_jobList_onlyOneJob_empty_coor = (600, 600)

engineering_file_coor = (20, 40)
engineering_file_import_coor = (20, 210)
engineering_file_input_coor = (20, 160)
engineering_file_save_coor = (20, 250)
engineering_file_close_coor = (20, 275)

engineering_action_coor = (80, 40)
engineering_action_open_coor = (80, 90)
engineering_action_select_coor = (80, 70)
engineering_action_select_unselect_all_coor = (280, 95)

engineering_option_coor = (190, 40)
engineering_option_language_coor = (190, 60)
engineering_option_language_EP_Default_coor = (390, 60)
engineering_option_language_Simplified_Chinese_coor = (390, 110)

engineering_job_right_click_open_coor = (20, 10)

engineering_inJob_go_up_coor = (80, 250)
engineering_inJob_steps_coor = (80 + 260, 250)
engineering_inJob_steps_step_first_coor = (80 + 130, 250)

""" 以下为engineering--import模块信息"""
engineering_file_import_input_path_coor = (30, 80) # 变形时，字体太大，异常情况,y = 100
engineering_file_import_ok_coor = (30, 180) # 变形时，字体太大，异常情况,y = 200


""" 以下为engineering--input模块信息"""
engineering_file_input_path_coor = (30, 55)




""" 以下为graphic模块信息"""
graphic_window_para = {'title': RunConfig.driver_epcam_ui_graphic_title,'control_type':"Window"}







