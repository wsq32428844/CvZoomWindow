import cv2
import numpy as np
from CvZoomWindow.cvzoomwindow import CvZoomWindow

def main():
    # 创建一个简单的测试图像
    width, height = 500, 500
    image = np.ones((height, width, 3), dtype=np.uint8) * 255  # 白色背景
    
    # 绘制彩色图案以便于观察旋转
    # 中心圆
    cv2.circle(image, (width//2, height//2), 50, (0, 0, 255), -1)
    # 十字线
    cv2.line(image, (width//2 - 100, height//2), (width//2 + 100, height//2), (0, 0, 0), 3)
    cv2.line(image, (width//2, height//2 - 100), (width//2, height//2 + 100), (0, 0, 0), 3)
    # 四个角的彩色方块
    cv2.rectangle(image, (50, 50), (100, 100), (255, 0, 0), -1)
    cv2.rectangle(image, (width-100, 50), (width-50, 100), (0, 255, 0), -1)
    cv2.rectangle(image, (50, height-100), (100, height-50), (0, 0, 255), -1)
    cv2.rectangle(image, (width-100, height-100), (width-50, height-50), (0, 255, 255), -1)
    
    # 添加使用说明
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "旋转功能测试", (20, 30), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(image, "右键点击: 设置旋转中心", (20, 60), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, "右键拖拽: 旋转图像", (20, 90), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, "中键点击: 取消旋转", (20, 120), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, "左键拖拽: 平移", (20, 150), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, "滚轮: 缩放", (20, 180), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, "ESC: 退出", (20, 210), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    
    # 创建窗口实例
    win = CvZoomWindow("旋转功能测试")
    
    # 显示图像
    win.imshow(image)
    
    print("旋转功能测试开始!")
    print("操作说明:")
    print("1. 右键点击任意位置 - 设置旋转中心（会显示红色十字标记）")
    print("2. 设置旋转中心后，按住右键并拖动鼠标 - 围绕旋转中心旋转图像")
    print("3. 中键点击 - 取消旋转并清除旋转中心标记")
    print("4. 左键拖拽 - 平移图像")
    print("5. 滚轮 - 缩放图像")
    print("6. 按ESC键退出")
    
    # 主循环
    while True:
        # 处理按键事件
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC键
            break
    
    # 清理资源
    win.destroyWindow()
    print("测试完成，程序已退出")

if __name__ == "__main__":
    main()