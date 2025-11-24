import cv2
import numpy as np

import cvzoomwindow

# Image loading
img = cv2.imread("/Volumes/T7/三期-seed_codeer_trae_05/CvZoomWindow/CvZoomWindow/image.bmp")
print(f"Image loaded: {img is not None}")
if img is not None:
    print(f"Image shape: {img.shape}")

# Instance of CvZoomWindow class
zw = cvzoomwindow.CvZoomWindow(
    "Zoom Window" # Name of the window 
    )

# Displays an image
zw.imshow(img)
print("Image shown")
# 强制刷新窗口
cv2.waitKey(1)
 
# Waits for a pressed key.
cv2.waitKey()
