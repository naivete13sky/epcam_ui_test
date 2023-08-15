import os
import time

from PIL import Image

from cc_method import PictureMethod


def f1():
    pass
    from pywinauto.application import Application

    # 定义.exe程序的路径
    exe_path = r"C:\cc\ep_local\product\EP-CAM\version\20230717\EPCAM_1.1.7.2_release_r12827_jiami_3\Release\EP-CAM.exe"

    # 获取.exe文件所在的目录路径
    exe_dir = os.path.dirname(exe_path)

    # 切换当前工作目录为.exe所在目录
    os.chdir(exe_dir)

    # 使用Application类来启动.exe程序
    app = Application(backend="uia").start(exe_path)

    time.sleep(15)
    # 使用窗口标题来连接到应用程序的主窗口
    main_window = app.window(title="Engineering 1.1.7.2")

    # 可以通过main_window来执行其他操作，如点击按钮、输入文本等
    main_window.print_control_identifiers()

    # 等待一段时间或执行其他操作

def f2():
    pass
    import os

    exe_path = r"C:\cc\ep_local\product\EP-CAM\version\20230717\EPCAM_1.1.7.2_release_r12827_jiami_3\Release\EP-CAM.exe"

    # 获取.exe文件所在的目录路径
    exe_dir = os.path.dirname(exe_path)

    # 切换当前工作目录为.exe所在目录
    os.chdir(exe_dir)


    # 使用os.system启动应用程序
    os.system(exe_path)

def f3():
    pass
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 根据你的Tesseract安装路径设置
    tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
    # im = Image.open(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese.png")
    # im = Image.open(r"C:\cc\share\temp\8.png")
    im = Image.open(r'C:\cc\software\ocr\train5\6.png')
    text = pytesseract.image_to_string(im, config=tessdata_dir_config, lang='chi_sim')  # 使用Tesseract进行文字识别,使用简体中文语言包
    # text = pytesseract.image_to_string(im, config=tessdata_dir_config, lang='chi_sim_cc')  # 使用Tesseract进行文字识别,使用简体中文语言包
    print('textcc:', text)


def f4():
    pass
    import numpy as np
    import pytesseract
    from pytesseract import Output
    import cv2

    try:
        from PIL import Image
        from PIL import ImageDraw
        from PIL import ImageFont
    except ImportError:
        import Image

    img = cv2.imread(r'C:\cc\software\ocr\train5\3.png')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    width_list = []
    for c in cnts:
        _, _, w, _ = cv2.boundingRect(c)
        width_list.append(w)
    wm = np.median(width_list)

    tess_text = pytesseract.image_to_data(img, output_type=Output.DICT, lang='chi_sim')
    print('tess_text:',tess_text)
    for i in range(len(tess_text['text'])):
        word_len = len(tess_text['text'][i])
        if word_len > 1:
            world_w = int(wm * word_len)
            (x, y, w, h) = (tess_text['left'][i], tess_text['top'][i], tess_text['width'][i], tess_text['height'][i])
            cv2.rectangle(img, (x, y), (x + world_w, y + h), (255, 0, 0), 1)
            im = Image.fromarray(img)
            draw = ImageDraw.Draw(im)
            # font = ImageFont.truetype(font="simsun.ttc", size=18, encoding="utf-8")
            font = ImageFont.truetype(font="simhei.ttf", size=18, encoding="utf-8")
            draw.text((x, y - 20), tess_text['text'][i], (255, 0, 0), font=font)
            img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

    cv2.imshow("TextBoundingBoxes", img)
    cv2.waitKey(0)



def f5():
    pass
    # 输入和输出文件路径
    input_png_path = r"C:\cc\software\ocr\train5\png\1.png"  # 替换为您的PNG文件路径
    output_tiff_path = r"C:\cc\software\ocr\train5\tif\1.tif"  # 替换为您想要保存的TIFF文件路径

    # 调用函数进行转换
    PictureMethod.png_to_tiff_one_file(input_png_path, output_tiff_path)

if __name__ == '__main__':
    pass
    f5()


