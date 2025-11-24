import cv2
import numpy as np

# 创建一个简单的测试图像
img = np.zeros((256, 256, 3), dtype=np.uint8)
img[50:100, 50:100] = (0, 0, 255)  # 红色方块

# 简单的鼠标事件回调函数
def mouse_callback(event, x, y, flags, param):
    print(f"Mouse event: {event}, position: ({x}, {y}), flags: {flags}")

# 创建窗口
cv2.namedWindow("Minimal Test")
cv2.setMouseCallback("Minimal Test", mouse_callback)

print("简易鼠标事件测试")
print("按ESC键退出")

# 主循环
while True:
    cv2.imshow("Minimal Test", img)
    key = cv2.waitKey(50)
    if key == 27:  # ESC键
        break

# 清理
cv2.destroyAllWindows()
print("测试结束")
