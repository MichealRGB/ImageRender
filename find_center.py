#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import cv2
import numpy as np
import sys

## 还是得用轮廓提取，自己画圆环不精准,先提取轮廓，用面积过滤掉杂点，每个轮廓之间最好有个关系（因为6环是分成三个部分的，5环也有三个部分），不然不好判断是几环，然后用图片相减的方法去搞定打中靶子的点，然后在对这些点进行提取轮廓（实际测试后发现，压线的点可能会出现多个轮廓，现在还没有太好的办法去处理），然后判断这些点分布在几环

image = cv2.imread('images/zhenshiba4.jpg')
if image is None:
    print('Failed to load image:', image)
    sys.exit(1)

## 膨胀处理(验证后发现膨胀处理后靶子的一些线条变粗了我之前没发现卧槽)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4),(-1,-1))
eroded_image = cv2.erode(image,kernel)

## 灰度处理
gray_image = cv2.cvtColor(eroded_image,cv2.COLOR_BGR2GRAY)

## 二值法处理
ret,thresh = cv2.threshold(eroded_image,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

## 提取轮廓
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

## 过滤小面积的元素，现在要找到中心圆环的轮廓
tmp_contours = []
less_pixels = 20 * 20
for i in range(0,len(contours)):
    if cv2.contourArea(contours[i]) > less_pixels:
        tmp_contours.append(contours[i])

print 'contours ->' + str(len(contours))
print 'tmp_contours ->' + str(len(tmp_contours))

# for i in range(0,len(tmp_contours)):
#     ## 取出质心坐标
#     cnt = tmp_contours[i]
#     moment = cv2.moments(cnt)
#     if moment['m00'] != 0:
#         ## CenterPoint
#         cx = int(moment['m10'] / moment['m00'])
#         cy = int(moment['m01'] / moment['m00'])
#         print cx, cy
#         print '\n'
#         cv2.circle(image, (cx, cy), 2, (0, 0, 255), 2)

# 最中心的圆环是数组中的第一个
cv2.drawContours(image, tmp_contours, 1, (0, 255, 0), 2)

# print hierarchy
#
# 取出质心坐标
cnt = tmp_contours[1]
moment = cv2.moments(cnt)

## CenterPoint
cx = int(moment['m10'] / moment['m00'])
cy = int(moment['m01'] / moment['m00'])

print cx,cy

## 标出质心
cv2.circle(image, (cx, cy), 2, (0, 0, 255), 2)

(x,y),radius = cv2.minEnclosingCircle(cnt)

print int(radius)

for i in range(0,6):
    cv2.circle(image,(int(x),int(y)),int(radius * i),(0,0,255),2)


# cv2.drawContours(image, tmp_contours, -1, (0, 255, 0), 2)

cv2.imshow("find_center", image)
cv2.waitKey(0)
cv2.destroyAllWindows()