import cv2
import time
import cvzoomwindow

# Image loading
import os
# 获取当前脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建图像文件的完整路径q
image_path = os.path.join(script_dir, "image.bmp")
img = cv2.imread(image_path)
print(f"Loading image from: {image_path}")
if img is None:
    print("Error: Could not load image!")
else:
    print(f"Image loaded successfully! Shape: {img.shape}")

# Instance of CvZoomWindow class
zw = cvzoomwindow.CvZoomWindow(
    "Zoom Window" # Name of the window 
    )

# Displays an image
zw.imshow(img)

# 添加主循环来保持窗口打开并持续刷新
print("Window opened. Press 'q' to quit...")
start_time = time.time()
while True:
    # 持续刷新图像
    zw.imshow(img)
    
    # 检查按键
    key = cv2.waitKey(50)  # 50ms延迟
    if key == ord('q') or key == 27:  # 'q'键或ESC键
        break
    
    # 每5秒打印一次调试信息
    if time.time() - start_time > 5:
        print("Still running... Press 'q' to quit.")
        start_time = time.time()

# 关闭所有窗口
cv2.destroyAllWindows()
print("Window closed.")
