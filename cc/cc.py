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
    im = Image.open(r"C:\cc\share\temp\cc.png")
    # im = Image.open(r"C:\cc\share\temp\8.png")
    # im = Image.open(r'C:\cc\software\ocr\train5\6.png')
    # text = pytesseract.image_to_string(im, config=tessdata_dir_config, lang='chi_sim')  # 使用Tesseract进行文字识别,使用简体中文语言包
    text = pytesseract.image_to_string(im, config=tessdata_dir_config, lang='chi_sim_cc')  # 使用Tesseract进行文字识别,使用简体中文语言包
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


def f6():
    pass
    import cv2
    import pytesseract

    # 设置Tesseract的路径（如果不在系统路径中）
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def locate_text(image_path, target_text):
        # 读取图像
        image = cv2.imread(image_path)

        # 将图像转换为灰度
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 使用Tesseract进行OCR
        ocr_result = pytesseract.image_to_string(gray_image)
        print('ocr_result:',ocr_result)

        # 查找目标文本的位置
        target_coordinates = []
        lines = ocr_result.split('\n')
        for i, line in enumerate(lines):
            if target_text in line:
                y = i * 20  # 假设每行的高度是20像素
                target_coordinates.append((0, y))

        return target_coordinates

    # 图像路径和目标文本
    image_path = r"C:\cc\share\temp\cc2.png"
    target_text = 'steps'

    # 定位并打印文本位置
    text_coordinates = locate_text(image_path, target_text)
    if text_coordinates:
        for coord in text_coordinates:
            print(f"找到目标文本 '{target_text}' 在图像中的位置：(x={coord[0]}, y={coord[1]})")
    else:
        print(f"未找到目标文本 '{target_text}'")

def f7():
    import pytesseract
    from PIL import Image

    # 读取图片并进行 OCR
    image_path = r"C:\cc\share\temp\cc2.png"
    image = Image.open(image_path)  # 打开图像
    text = pytesseract.image_to_string(image)

    # 要识别的指定文本
    target_text = 'steps'

    # 在提取的文本中查找指定文本
    text_position = text.find(target_text)

    if text_position != -1:
        # 获取文本的边界框信息
        boxes = pytesseract.image_to_boxes(image)

        # 解析边界框信息
        for box in boxes.splitlines():
            box_data = box.split()
            character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

            # 检查文本的位置是否在边界框范围内
            if x <= text_position <= x + w:
                relative_x = (text_position - x) / w
                relative_y = 1.0 - (y / image.height)
                print(f"Relative X: {relative_x}, Relative Y: {relative_y}")
                break
    else:
        print("Target text not found in the image.")

def f8():
    import pytesseract
    from PIL import Image

    # 读取图片并进行 OCR
    image_path = r"C:\cc\share\temp\cc2.png"
    image = Image.open(image_path)  # 打开图像
    text = pytesseract.image_to_string(image)

    # 要识别的指定文本
    target_text = 'steps'

    # 在提取的文本中查找指定文本
    text_position = text.find(target_text)

    if text_position != -1:
        # 计算指定文本的相对位置
        image_width, image_height = image.size
        relative_x = text_position / image_width
        relative_y = image.getbbox()[1] / image_height

        print(f"Relative X: {relative_x}, Relative Y: {relative_y}")
    else:
        print("Target text not found in the image.")

def f9():
    import pytesseract
    from PIL import Image

    # 读取图片并进行 OCR
    image_path = r"C:\cc\share\temp\cc2.png"
    image = Image.open(image_path)  # 打开图像

    # 使用 Tesseract 进行文本块检测和识别
    text_boxes = pytesseract.image_to_boxes(image, config='--psm 6')

    image_width, image_height = image.size
    for box in text_boxes.splitlines():
        box_data = box.split()
        character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

        # 获取字符的文本内容
        character_text = character

        # 计算相对于图像左上角的坐标
        relative_x = x / image_width
        relative_y = 1.0 - (y / image_height)

        print(f"Text: {character_text}, Relative X: {relative_x}, Relative Y: {relative_y}")

def f10():

    import pytesseract
    from PIL import Image

    # 读取图片并进行 OCR
    image_path = r"C:\cc\share\temp\cc2.png"
    image = Image.open(image_path)  # 打开图像

    # 使用 Tesseract 进行文本块检测和识别
    text_boxes = pytesseract.image_to_boxes(image, config='--psm 6')

    image_width, image_height = image.size

    # 目标单词
    target_word = 'steps'

    # 将文本块存储为列表
    text_boxes_list = text_boxes.splitlines()

    # 遍历文本块，找到目标单词的位置
    for i in range(len(text_boxes_list)):
        box_data = text_boxes_list[i].split()
        character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

        if character == target_word[0]:
            potential_word = character
            for j in range(1, len(target_word)):
                next_box_data = text_boxes_list[i + j].split()
                next_character = next_box_data[0]
                potential_word += next_character

            if potential_word == target_word:
                # 计算左上角和右下角的相对坐标
                left_top_relative_x = x / image_width
                left_top_relative_y = 1.0 - (y / image_height)
                right_bottom_relative_x = (x + w) / image_width
                right_bottom_relative_y = 1.0 - ((y + h) / image_height)

                print(f"Target Word: {target_word}")
                print(f"Left Top Relative Coordinates: ({left_top_relative_x}, {left_top_relative_y})")
                print(f"Right Bottom Relative Coordinates: ({right_bottom_relative_x}, {right_bottom_relative_y})")

def f11():

    import pytesseract
    from PIL import Image

    # 读取图片并进行 OCR
    image_path = r"C:\cc\share\temp\cc2.png"
    image = Image.open(image_path)  # 打开图像

    # 使用 Tesseract 进行文本块检测和识别
    text_boxes = pytesseract.image_to_boxes(image, config='--psm 6')

    image_width, image_height = image.size

    for box in text_boxes.splitlines():
        box_data = box.split()
        character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

        # 获取字符的文本内容
        character_text = character

        # 计算相对于图像左上角的坐标
        relative_x = x / image_width
        relative_y = 1.0 - (y / image_height)

        print(f"Text: {character_text}, Relative X: {relative_x}, Relative Y: {relative_y}")

    # 目标单词
    target_word = 'steps'

    # 将文本块存储为列表
    text_boxes_list = text_boxes.splitlines()
    # print('text_boxes_list:',text_boxes_list)

    # 遍历文本块，找到目标单词的位置
    for i in range(len(text_boxes_list)):
        box_data = text_boxes_list[i].split()
        character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

        if character == target_word[0]:
            potential_word = character
            for j in range(1, len(target_word)):
                next_box_data = text_boxes_list[i + j].split()
                next_character = next_box_data[0]
                potential_word += next_character

            if potential_word == target_word:
                # 计算左上角和右下角的相对坐标
                left_top_relative_x = x / image_width
                left_top_relative_y = 1.0 - (y / image_height)

                right_bottom_relative_x = (x + w) / image_width
                right_bottom_relative_y = 1.0 - ((y + h) / image_height)

                print(f"Target Word: {target_word}")
                print(f"Left Top Relative Coordinates: ({left_top_relative_x}, {left_top_relative_y})")
                print(f"Right Bottom Relative Coordinates: ({right_bottom_relative_x}, {right_bottom_relative_y})")

def f12():

    import pytesseract
    from PIL import Image

    # 读取图片并进行 OCR
    image_path = r"C:\cc\share\temp\cc2.png"
    image = Image.open(image_path)  # 打开图像

    # 使用 Tesseract 进行文本块检测和识别
    text_boxes = pytesseract.image_to_boxes(image, config='--psm 6')

    image_width, image_height = image.size

    for box in text_boxes.splitlines():
        box_data = box.split()
        character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

        # 获取字符的文本内容
        character_text = character

        # 计算相对于图像左上角的坐标
        relative_x = x / image_width
        relative_y = 1.0 - (y / image_height)

        # print(f"Text: {character_text}, Relative X: {relative_x}, Relative Y: {relative_y}")

    # 目标单词
    target_word = 'steps'

    # 将文本块存储为列表
    text_boxes_list = text_boxes.splitlines()
    # print('text_boxes_list:',text_boxes_list)

    # 遍历文本块，找到目标单词的位置
    target_word_start = -1
    target_word_end = -1
    for i in range(len(text_boxes_list)):
        box_data = text_boxes_list[i].split()
        # print('box_data:',box_data)
        character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

        if character == target_word[0]:
            print("i:",i)
            potential_word = character
            for j in range(1, len(target_word)):
                next_box_data = text_boxes_list[i + j].split()
                next_character = next_box_data[0]
                potential_word += next_character

            if potential_word == target_word:
                target_word_start = i
                target_word_end = i + j
                print('target_word_start,target_word_end:',target_word_start,target_word_end)
                print('target_word_start_pos:',text_boxes_list[target_word_start],'target_word_end_pos:',text_boxes_list[target_word_end])
                # 计算左上角和右下角的相对坐标
                left_top_relative_x = x / image_width
                left_top_relative_y = 1.0 - (y / image_height)

                right_bottom_relative_x = (x + w) / image_width
                right_bottom_relative_y = 1.0 - ((y + h) / image_height)

                print(f"Target Word: {target_word}")
                print(f"Left Top Relative Coordinates: ({left_top_relative_x}, {left_top_relative_y})")
                print(f"Right Bottom Relative Coordinates: ({right_bottom_relative_x}, {right_bottom_relative_y})")
                break#只找到第一个符合的就行

    print('target_word_start,target_word_end:', target_word_start, target_word_end)
    print('target_word_start_pos:', text_boxes_list[target_word_start], 'target_word_end_pos:', text_boxes_list[target_word_end])

    # 计算左上角的相对坐标
    box_data_start = text_boxes_list[target_word_start].split()
    character_start, x_start, y_start, w_start, h_start = box_data_start[0], int(box_data_start[1]), int(box_data_start[2]), int(box_data_start[3]), int(box_data_start[4])
    left_top_relative_x_start = x_start / image_width
    left_top_relative_y_start = 1.0 - (y_start / image_height)
    print('left_top_relative_x_start,left_top_relative_y_start:',left_top_relative_x_start,left_top_relative_y_start)

    # 计算右下角的相对坐标
    box_data_end = text_boxes_list[target_word_end].split()
    character_end, x_end, y_end, w_end, h_end = box_data_end[0], int(box_data_end[1]), int(box_data_end[2]), int(box_data_end[3]), int(box_data_end[4])
    left_top_relative_x_end = x_end / image_width
    left_top_relative_y_end = 1.0 - (y_end / image_height)
    print('left_top_relative_x_end,left_top_relative_y_end:', left_top_relative_x_end, left_top_relative_y_end)

def f13():

    import pytesseract
    from PIL import Image

    # 读取图片并进行 OCR
    image_path = r"C:\cc\share\temp\cc2.png"
    image = Image.open(image_path)  # 打开图像

    # 使用 Tesseract 进行文本块检测和识别
    text_boxes = pytesseract.image_to_boxes(image, config='--psm 6')

    image_width, image_height = image.size

    for box in text_boxes.splitlines():
        box_data = box.split()
        character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

        # 获取字符的文本内容
        character_text = character

        # 计算相对于图像左上角的坐标
        relative_x = x / image_width
        relative_y = 1.0 - (y / image_height)

        # print(f"Text: {character_text}, Relative X: {relative_x}, Relative Y: {relative_y}")

    # 目标单词
    target_word = 'steps'

    # 将文本块存储为列表
    text_boxes_list = text_boxes.splitlines()
    # print('text_boxes_list:',text_boxes_list)

    # 遍历文本块，找到目标单词的位置
    target_word_start = -1
    target_word_end = -1
    for i in range(len(text_boxes_list)):
        box_data = text_boxes_list[i].split()
        # print('box_data:',box_data)
        character, x, y, w, h = box_data[0], int(box_data[1]), int(box_data[2]), int(box_data[3]), int(box_data[4])

        if character == target_word[0]:
            # print("i:",i)
            potential_word = character
            for j in range(1, len(target_word)):
                next_box_data = text_boxes_list[i + j].split()
                next_character = next_box_data[0]
                potential_word += next_character
            if potential_word == target_word:
                target_word_start = i
                target_word_end = i + j
                break#只找到第一个符合的就行

    print(f"Target Word: {target_word}")
    print('target_word_start,target_word_end:', target_word_start, target_word_end)

    # 计算左上角的相对坐标
    box_data_start = text_boxes_list[target_word_start].split()
    character_start, x_start, y_start, w_start, h_start = box_data_start[0], int(box_data_start[1]), int(box_data_start[2]), int(box_data_start[3]), int(box_data_start[4])
    left_top_relative_x_start = x_start / image_width
    left_top_relative_y_start = 1.0 - (y_start / image_height)
    print(f"Left Top Relative Coordinates: ({left_top_relative_x_start}, {left_top_relative_y_start})")
    # 计算右下角的相对坐标
    box_data_end = text_boxes_list[target_word_end].split()
    character_end, x_end, y_end, w_end, h_end = box_data_end[0], int(box_data_end[1]), int(box_data_end[2]), int(box_data_end[3]), int(box_data_end[4])
    left_top_relative_x_end = x_end / image_width
    left_top_relative_y_end = 1.0 - (y_end / image_height)
    print(f"Right Bottom Relative Coordinates: ({left_top_relative_x_end}, {left_top_relative_y_end})")


def f14():
    pass
    from appium import webdriver
    # os.system(r'start "" /d "C:\Program Files (x86)\Windows Application Driver\"  "WinAppDriver.exe"')


    des_cap = {}
    des_cap['app'] = r'C:\Windows\System32\notepad.exe'
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4723/wd/hub',
                              desired_capabilities=des_cap)
    driver.implicitly_wait(5)
    driver.find_element_by_name('文件(F)').click()
    from time import sleep
    sleep(2)
    driver.find_element_by_name('保存(S)	Ctrl+S').click()
    # driver.find_element_by_name('退出(X)').click()
    sleep(1)
    import pyautogui
    pyautogui.PAUSE = 0.5
    pyautogui.typewrite(r'D:\hello.txt')
    pyautogui.press('enter')

def f15():
    pass
    from appium import webdriver

    desired_caps = {
        "platformName": "Windows",
        "deviceName": "WindowsPC",
        "app": "C:\\Windows\\System32\\notepad.exe"
    }

    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723',
        desired_capabilities=desired_caps
    )

    # 执行一些测试操作，比如点击、输入文本等
    # 例如：element = driver.find_element_by_name("Untitled - Notepad")
    #       element.send_keys("Hello, World!")

    # 关闭应用程序和驱动
    driver.quit()


if __name__ == '__main__':
    pass
    f15()




