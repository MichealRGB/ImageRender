#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import cv2
import sys

image = cv2.imread('images/zhenshiba4.jpg')
if image is None:
    print('Failed to load image:', image)
    sys.exit(1)

## 膨胀处理(验证后发现膨胀处理后靶子的一些线条变粗了我之前没发现卧槽)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4),(-1,-1))

# eroded_image = cv2.erode(image,kernel)
dilate_image = cv2.dilate(image, kernel)

## 灰度处理
gray_image = cv2.cvtColor(dilate_image,cv2.COLOR_BGR2GRAY)

## 二值法处理
ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

## 提取轮廓
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

## 过滤小面积的元素，现在要找到中心圆环的轮廓
tmp_contours = []
less_pixels = 25 * 25
for i in range(0,len(contours)):
    if cv2.contourArea(contours[i]) > less_pixels:
        tmp_contours.append(contours[i])

print 'contours ->' + str(len(contours))
print 'tmp_contours ->' + str(len(tmp_contours))

# tmp_contours.pop(3)
# tmp_contours.pop(2)
# for i in range(0,len(tmp_contours)):
#     print cv2.contourArea(tmp_contours[i])


## 绘制轮廓
cv2.drawContours(image, tmp_contours, -1, (255, 0, 0), 3)



cv2.imshow("find_center", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

