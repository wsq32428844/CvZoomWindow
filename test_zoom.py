#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证滚轮缩放功能是否正确以鼠标位置为中心进行缩放
"""

import cv2
import numpy as np
from cvzoomwindow import CvZoomWindow
import time

def test_mouse_zoom():
    print("=== 滚轮缩放功能测试 ===")
    print("测试步骤:")
    print("1. 将鼠标移动到窗口中的不同位置")
    print("2. 使用鼠标滚轮向上滚动进行放大")
    print("3. 使用鼠标滚轮向下滚动进行缩小")
    print("4. 观察缩放是否以鼠标位置为中心进行")
    print("5. 按ESC键退出测试")
    print()
    
    # 创建一个带有明显特征点的测试图像
    img = np.ones((600, 800, 3), dtype=np.uint8) * 240  # 浅灰色背景
    
    # 添加明显的标记点，方便观察缩放中心
    cv2.circle(img, (200, 150), 5, (0, 0, 255), -1)  # 左上角红点
    cv2.putText(img, "A", (210, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    cv2.circle(img, (600, 150), 5, (0, 0, 255), -1)  # 右上角红点
    cv2.putText(img, "B", (610, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    cv2.circle(img, (400, 450), 5, (0, 0, 255), -1)  # 中心红点
    cv2.putText(img, "C", (410, 455), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # 添加网格线，帮助观察缩放
    for i in range(0, 800, 50):
        cv2.line(img, (i, 0), (i, 600), (200, 200, 200), 1)
    for i in range(0, 600, 50):
        cv2.line(img, (0, i), (800, i), (200, 200, 200), 1)
    
    # 添加使用说明
    instructions = [
        "测试说明:",
        "- 将鼠标移动到任意位置",
        "- 使用滚轮向上滚动放大",
        "- 使用滚轮向下滚动缩小",
        "- 观察缩放是否以鼠标为中心",
        "- 按ESC键退出"
    ]
    
    y_pos = 50
    for instruction in instructions:
        cv2.putText(img, instruction, (50, y_pos), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
        y_pos += 25
    
    # 创建窗口并显示图像
    print("创建窗口并显示测试图像...")
    win = CvZoomWindow('Mouse Zoom Test')
    win.imshow(img)
    
    print("\n开始测试...")
    print("请在窗口中移动鼠标并使用滚轮进行缩放操作")
    print("注意观察日志输出，确认缩放中心是否为鼠标位置")
    print()
    
    # 等待用户操作
    cv2.waitKey(0)
    
    print("\n测试结束，清理资源...")
    cv2.destroyAllWindows()
    print("测试完成！")

if __name__ == "__main__":
    try:
        test_mouse_zoom()
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
