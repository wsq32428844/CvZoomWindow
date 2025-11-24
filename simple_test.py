#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本：验证滚轮缩放功能
"""

import cv2
import numpy as np
from cvzoomwindow import CvZoomWindow

# 创建一个简单的测试图像
img = np.zeros((500, 500, 3), dtype=np.uint8)
cv2.rectangle(img, (100, 100), (400, 400), (0, 255, 0), 2)
cv2.circle(img, (250, 250), 10, (0, 0, 255), -1)  # 中心红点

# 创建窗口并显示图像
print("创建CvZoomWindow并显示图像")
print("请移动鼠标到不同位置并使用滚轮缩放")
print("注意观察控制台输出中鼠标位置和缩放信息")

win = CvZoomWindow('Simple Zoom Test')
win.imshow(img)

# 等待用户操作
print("按ESC键退出")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("测试结束")
