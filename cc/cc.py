import os
import time

import cv2
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


def f5():
    pass
    # 输入和输出文件路径
    input_png_path = r"C:\cc\software\ocr\train5\png\1.png"  # 替换为您的PNG文件路径
    output_tiff_path = r"C:\cc\software\ocr\train5\tif\1.tif"  # 替换为您想要保存的TIFF文件路径

    # 调用函数进行转换
    PictureMethod.png_to_tiff_one_file(input_png_path, output_tiff_path)


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


def f16():
    pass
    import cv2

    # 读取图像
    img = cv2.imread(r'C:\cc\share\temp\engineering_window.png')

    # 重排通道顺序为 RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 显示图像
    cv2.imshow("Original Image", img_rgb)
    cv2.waitKey(0)

    # 截取图像并显示
    img_cut = img_rgb[30:60, 10:40]
    cv2.imshow("Cropped Image", img_cut)
    cv2.waitKey(0)

    # 关闭窗口
    cv2.destroyAllWindows()


def f17():
    pass
    from PIL import Image

    # 读取图像
    img = Image.open(r'C:\cc\share\temp\engineering_window.png')

    # 显示图像
    img.show()

    # 截取图像并显示
    img_cut = img.crop((10, 30, 40, 60))  # 坐标是左上右下
    img_cut.show()


def f18():
    pass
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 根据你的Tesseract安装路径设置
    tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
    im = Image.open(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese_file_option.png")
    # im = Image.open(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese_file.png")
    # im.show()
    text_option = pytesseract.image_to_string(im, config=tessdata_dir_config,
                                              lang='chi_sim_cc')  # 使用Tesseract进行文字识别,使用简体中文语言包
    print('text_option:', text_option)


def f19():
    pass
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 根据你的Tesseract安装路径设置
    im = Image.open(r"C:\cc\share\temp\engineering_window_job_info.png")
    # im = Image.open(r"C:\cc\share\temp\engineering_menu_file_Simplified_Chinese_file.png")
    # im.show()
    text_option = pytesseract.image_to_string(im)
    print('text_option:', text_option)

def f20():
    pass
    img = cv2.imread(r'C:\cc\share\temp\engineering_file_input_window_png.png')
    # img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
    img_cut = img[315:335, 20:40]  # 后面的是水平方向
    cv2.imwrite(r"C:\cc\share\temp\engineering_file_input_window_png_cleared.png", img_cut)
    cv2.imshow("Cropped Image", img_cut)
    cv2.waitKey(0)

if __name__ == '__main__':
    pass
    f20()
