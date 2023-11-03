import cv2

img = cv2.imread(r'C:\cc\share\temp\input_view_ascii_window.png')
# img_cut = img[249:331, 46:137]  # 后面的是水平方向，异常时，字体过大时
img_cut = img[0:880, 8:1005]  # 后面的是水平方向
cv2.imwrite(r"C:\cc\share\temp\input_view_ascii_window_cut.png", img_cut)