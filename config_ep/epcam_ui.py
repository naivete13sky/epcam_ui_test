import sys
import re

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

class EPCAM(object):
    pass
    def get_engineering_left_top_Coor(win_text):
        win_text2 = get_print_control_identifiers_text(win_text)
        coor_ok = get_coor_of_object('Engineering 1.1.7.2',win_text2)
        return coor_ok

    def getFileCoor(win_text):
        win_text2 = get_print_control_identifiers_text(win_text)
        coor_ok = get_coor_of_object('关闭',win_text2)
        return coor_ok