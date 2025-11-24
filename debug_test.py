#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细调试脚本：验证滚轮缩放功能
"""

import cv2
import numpy as np
import sys
import os

# 确保日志实时输出
sys.stdout.flush()

print("=== 开始滚轮缩放功能详细测试 ===")
print("加载cvzoomwindow模块...")
from cvzoomwindow import CvZoomWindow

# 创建一个带有明显标记的测试图像
print("创建测试图像...")
img = np.ones((600, 800, 3), dtype=np.uint8) * 240  # 浅灰色背景

# 添加多个彩色标记点，方便观察缩放中心
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255)]
points = [(100, 100), (700, 100), (400, 300), (100, 500), (700, 500)]
labels = ["A", "B", "C", "D", "E"]

for i, (x, y) in enumerate(points):
    cv2.circle(img, (x, y), 10, colors[i], -1)
    cv2.putText(img, labels[i], (x+15, y+5), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, colors[i], 2)

# 添加网格线，帮助观察缩放效果
for i in range(0, 800, 50):
    cv2.line(img, (i, 0), (i, 600), (200, 200, 200), 1)
for i in range(0, 600, 50):
    cv2.line(img, (0, i), (800, i), (200, 200, 200), 1)

# 创建窗口并显示图像
print("创建窗口...")
print("=== 调试信息将实时显示在控制台 ===")
print("请执行以下操作进行测试:")
print("1. 将鼠标移动到标记点A附近，使用滚轮缩放")
print("2. 将鼠标移动到标记点B附近，使用滚轮缩放")
print("3. 将鼠标移动到标记点C附近，使用滚轮缩放")
print("4. 观察缩放是否以鼠标位置为中心进行")
print("5. 按ESC键退出测试")

win = CvZoomWindow('Debug Zoom Test')

# 强制刷新输出
sys.stdout.flush()

print("显示图像...")
win.imshow(img)

print("等待用户操作...")
print("注意观察控制台中鼠标移动和滚轮事件的详细日志")

# 等待用户操作
while True:
    key = cv2.waitKey(100)  # 短暂等待并检查键盘输入
    if key == 27:  # ESC键
        break
    sys.stdout.flush()  # 定期刷新输出缓冲区

print("\n测试完成，清理资源...")
cv2.destroyAllWindows()
print("程序已退出")
