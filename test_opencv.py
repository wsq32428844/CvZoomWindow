import cv2
import numpy as np

# 创建一个简单的彩色图像
width, height = 200, 200
image = np.zeros((height, width, 3), dtype=np.uint8)

# 在图像上绘制一些几何图形
cv2.rectangle(image, (50, 50), (150, 150), (0, 255, 0), 2)
cv2.circle(image, (100, 100), 30, (0, 0, 255), -1)
cv2.putText(image, "OpenCV Test", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

# 创建一个窗口
cv2.namedWindow("OpenCV Test", cv2.WINDOW_NORMAL)

# 显示图像
cv2.imshow("OpenCV Test", image)

# 添加waitKey以确保图像显示
print("Press any key to exit...")
cv2.waitKey(0)

# 关闭所有窗口
cv2.destroyAllWindows()