import cv2
import numpy as np
from CvZoomWindow.cvzoomwindow import CvZoomWindow

# 创建一个简单的图像作为测试
width, height = 800, 600
image = np.zeros((height, width, 3), dtype=np.uint8)
image[:] = (255, 255, 255)  # 白色背景

# 添加文字说明
cv2.putText(image, "滚轮测试：向上滚动放大，向下滚动缩小", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

print("创建CvZoomWindow实例...")
window = CvZoomWindow("滚轮测试")

# 显示图像
print("显示图像，开始滚轮测试...")
window.imshow(image)

print("请测试鼠标滚轮功能，按ESC键退出")

# 主循环
while True:
    key = cv2.waitKey(1)
    if key == 27:  # ESC键退出
        print("ESC键被按下，退出程序")
        break

# 销毁窗口
window.destroyWindow()
print("测试完成")
