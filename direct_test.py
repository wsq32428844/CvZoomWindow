import cv2
import numpy as np

# 创建测试图像
img = np.full((500, 500, 3), 255, dtype=np.uint8)
cv2.rectangle(img, (100, 100), (400, 400), (0, 0, 255), -1)
cv2.rectangle(img, (150, 150), (350, 350), (0, 255, 0), -1)
cv2.rectangle(img, (200, 200), (300, 300), (255, 0, 0), -1)

# 窗口设置
window_name = 'Direct Zoom Test'
window_size = (800, 600)
cv2.namedWindow(window_name)

# 状态变量
mouse_down = False
old_x, old_y = 0, 0
scale = 1.0
pan_x, pan_y = 0, 0

# 鼠标回调函数
def mouse_callback(event, x, y, flags, param):
    global mouse_down, old_x, old_y, scale, pan_x, pan_y
    
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"左键按下 at ({x}, {y})")
        mouse_down = True
        old_x, old_y = x, y
    
    elif event == cv2.EVENT_LBUTTONUP:
        print(f"左键释放 at ({x}, {y})")
        mouse_down = False
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_down:
            dx = x - old_x
            dy = y - old_y
            pan_x += dx
            pan_y += dy
            print(f"拖动: dx={dx}, dy={dy}, pan=({pan_x}, {pan_y})")
            old_x, old_y = x, y
    
    elif event == cv2.EVENT_MOUSEWHEEL:
        # 滚轮缩放
        if flags > 0:
            scale *= 1.1
            print(f"放大: scale={scale}")
        else:
            scale /= 1.1
            print(f"缩小: scale={scale}")
        # 限制缩放范围
        scale = max(0.1, min(scale, 10.0))

# 设置鼠标回调
cv2.setMouseCallback(window_name, mouse_callback)

print("直接测试开始")
print("操作说明:")
print("- 左键拖动: 平移图像")
print("- 鼠标滚轮: 缩放图像")
print("- 按 'q' 退出")

# 主循环
while True:
    # 创建变换矩阵
    M = np.float32([
        [scale, 0, pan_x],
        [0, scale, pan_y]
    ])
    
    # 应用变换
    transformed = cv2.warpAffine(img, M, window_size, flags=cv2.INTER_LINEAR)
    
    # 显示图像
    cv2.imshow(window_name, transformed)
    
    # 检查键盘输入
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
print("测试结束")