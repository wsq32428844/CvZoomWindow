import cv2
import numpy as np

# 创建一个简单的彩色图像
img = np.full((500, 500, 3), 255, dtype=np.uint8)
cv2.rectangle(img, (100, 100), (400, 400), (0, 0, 255), -1)
cv2.rectangle(img, (150, 150), (350, 350), (0, 255, 0), -1)
cv2.rectangle(img, (200, 200), (300, 300), (255, 0, 0), -1)

window_name = 'Event Test Window'
cv2.namedWindow(window_name)

# 事件类型映射
event_types = {
    0: 'EVENT_MOUSEMOVE',
    1: 'EVENT_LBUTTONDOWN',
    2: 'EVENT_RBUTTONDOWN',
    3: 'EVENT_MBUTTONDOWN',
    4: 'EVENT_LBUTTONUP',
    5: 'EVENT_RBUTTONUP',
    6: 'EVENT_MBUTTONUP',
    7: 'EVENT_LBUTTONDBLCLK',
    8: 'EVENT_RBUTTONDBLCLK',
    9: 'EVENT_MBUTTONDBLCLK',
    10: 'EVENT_MOUSEWHEEL',
    11: 'EVENT_MOUSEHWHEEL'
}

# 简单的鼠标事件回调函数
def mouse_callback(event, x, y, flags, param):
    event_name = event_types.get(event, f'Unknown({event})')
    print(f"EVENT: {event_name} at ({x}, {y}), flags: {flags}")
    
    # 特别处理左键按下
    if event == cv2.EVENT_LBUTTONDOWN:
        print("  LEFT BUTTON DOWN DETECTED!")
    
    # 特别处理滚轮
    elif event == cv2.EVENT_MOUSEWHEEL:
        direction = "UP" if flags > 0 else "DOWN"
        print(f"  MOUSE WHEEL {direction} DETECTED!")

# 设置鼠标回调
cv2.setMouseCallback(window_name, mouse_callback)

print("事件测试开始")
print("请尝试以下操作：")
print("1. 移动鼠标")
print("2. 按下左键并拖动")
print("3. 使用鼠标滚轮")
print("4. 双击左键")
print("按 'q' 退出")

# 显示图像并等待键盘输入
while True:
    cv2.imshow(window_name, img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
print("测试结束")