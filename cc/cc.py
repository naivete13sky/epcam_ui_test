def f1():
    import cv2
    img = cv2.imread(r'C:\cc\share\temp\input_view_ascii_window.png')
    # img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
    img_cut = img[70:135, 975:1005]  # 后面的是水平方向
    cv2.imwrite(r"C:\cc\share\temp\input_view_ascii_window_scroll.png", img_cut)

# f1()

def f2():
    import cv2
    import numpy as np
    # 读取大图和小图
    large_image = cv2.imread(r"C:\cc\share\temp\input_view_ascii_window.png")
    small_image = cv2.imread(r"C:\cc\share\temp\input_view_ascii_window_scroll.png")
    # 执行模板匹配
    result = cv2.matchTemplate(large_image, small_image, cv2.TM_CCOEFF_NORMED)
    # 获取匹配的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val, max_val, min_loc, max_loc)
    # 如果使用TM_SQDIFF_NORMED方法，min_loc包含最佳匹配的位置
    # 如果使用其他方法，max_loc包含最佳匹配的位置
    # 绘制矩形框来标记小图的位置
    h, w, _ = small_image.shape
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(large_image, top_left, bottom_right, (0, 255, 0), 2)
    print('top_left:',top_left,'bottom_right',bottom_right)
    # 显示结果
    cv2.imshow('Result', large_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
f2()

