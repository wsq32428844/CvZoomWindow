import cv2
import numpy as np

# 读取图像
img = cv2.imread("image.bmp")
print(f"Image loaded: {img is not None}")
if img is not None:
    print(f"Image shape: {img.shape}")

# 创建窗口
cv2.namedWindow("Test Window", cv2.WINDOW_NORMAL)

# 显示图像
cv2.imshow("Test Window", img)
print("Image shown")

# 等待按键
cv2.waitKey()

# 销毁窗口
cv2.destroyAllWindows()