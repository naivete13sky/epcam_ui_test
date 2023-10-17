from config import RunConfig

""" 以下为engineering模块信息"""
# engineering_window
engineering_window_para = {'title': RunConfig.driver_epcam_ui_engineering_title}
# import job窗口
engineering_import_window_child_window_para = {'title': "Import Job", 'control_type': "Window"}
# import job窗口，获得选择文件类型控件
engineering_import_input_path_file_type_window_para = {'title': "文件类型(T):", 'auto_id': "1136",
                                                       'control_type': "ComboBox"}
# 选择文件窗口中的文件路径对象
engineering_import_input_path_file_path_window_para = {'title': "文件名(N):", 'auto_id': "1148",
                                                       'control_type': "ComboBox"}
# 确认选择中的文件
engineering_import_input_path_confirm_window_para = {'title': "打开(O)", 'auto_id': "1",
                                                     'control_type': "Button"}
# input job窗口
engineering_input_window_child_window_para = {'title': "Input", 'control_type': "Window"}
# input 选择文件窗口中的文件路径对象
engineering_input_path_file_path_window_para = {'title': "Open", 'control_type': "Window"}

engineering_jobList_first_coor = (80, 280)
engineering_file_coor = (20, 40)
engineering_file_import_coor = (20, 210)
engineering_file_import_input_path_coor = (30, 80) # 变形时，字体太大，异常情况,y = 100
engineering_file_import_ok_coor = (30, 180) # 变形时，字体太大，异常情况,y = 200

