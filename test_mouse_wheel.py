import cv2
import numpy as np
from CvZoomWindow.cvzoomwindow import CvZoomWindow

# 创建一个简单的彩色图像作为测试
width, height = 800, 600
image = np.zeros((height, width, 3), dtype=np.uint8)

# 绘制一些彩色图形以便于观察缩放效果
# 绘制彩色渐变背景
for y in range(height):
    for x in range(width):
        image[y, x] = [x % 256, y % 256, (x + y) % 256]

# 绘制一些几何图形作为参考点
cv2.rectangle(image, (100, 100), (200, 200), (0, 255, 0), 2)
cv2.circle(image, (400, 300), 50, (0, 0, 255), -1)
cv2.rectangle(image, (600, 400), (700, 500), (255, 0, 0), 2)

# 添加文字说明
cv2.putText(image, "测试鼠标滚轮缩放功能", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(image, "向上滚动：放大", (50, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
cv2.putText(image, "向下滚动：缩小", (500, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)

print("创建CvZoomWindow实例...")
window = CvZoomWindow("测试鼠标滚轮")

print("显示图像...")
window.imshow(image)

print("进入主循环，请测试鼠标滚轮功能...")
print("按ESC键退出")

# 主循环
while True:
    key = cv2.waitKey(1)
    if key == 27:  # ESC键退出
        print("ESC键被按下，退出程序")
        break

print("销毁窗口...")
window.destroyWindow()
print("程序结束")
