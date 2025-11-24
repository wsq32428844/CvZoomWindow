import cv2
import numpy as np
import time
from CvZoomWindow.cvzoomwindow import CvZoomWindow

# 创建一个简单的测试图像
img = np.zeros((256, 256, 3), dtype=np.uint8)
# 绘制一些彩色方块以便于观察平移缩放效果
img[50:100, 50:100] = (0, 0, 255)  # 红色方块
img[150:200, 150:200] = (0, 255, 0)  # 绿色方块
img[50:100, 150:200] = (255, 0, 0)  # 蓝色方块

# 创建CvZoomWindow实例
zw = CvZoomWindow("Test Zoom Window")
print("\n测试平移缩放功能说明：")
print("1. 鼠标左键拖动：平移图像")
print("2. 鼠标滚轮：缩放图像")
print("3. 鼠标左键双击：适应窗口显示")
print("4. 鼠标右键双击：原始大小显示")
print("5. 按'q'键退出")

# 主循环
running = True
first_time = True
while running:
    # 显示图像 - 只在第一次调用zoom_fit
    if first_time:
        zw.imshow(img, zoom_fit=True)
        first_time = False
    else:
        # 直接调用redraw_image更新显示，保持当前的平移缩放状态
        zw.redraw_image()
    
    # 检查按键
    key = cv2.waitKey(50)
    if key == ord('q') or key == 27:  # 27是ESC键
        running = False
    
    # 每5秒打印一次调试信息
    current_time = time.time()
    if not hasattr(zw, '_last_print_time'):
        zw._last_print_time = current_time
    elif current_time - zw._last_print_time > 5:
        print("Still running... Try dragging with left mouse button or using mouse wheel.")
        zw._last_print_time = current_time

# 清理
cv2.destroyAllWindows()
print("Window closed.")
