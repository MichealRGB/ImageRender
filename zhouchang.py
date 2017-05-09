#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import cv2
import numpy as np
import sys
import math

image = cv2.imread('images/yuan.jpg')

if image is None:
    print 'xxx'

## 灰度处理
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

## 二值法处理
ret,thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
# cv2.drawContours(image, contours[1], -1, (0, 255, 0), 2)


are = cv2.contourArea(contours[1])
rect = cv2.boundingRect(contours[1])
print rect
rect = np.int0(rect)

print rect
x1,y1,w,h = rect
print type(rect)
print w,h
r = (w + h)/4
print '自己计算结果' + str(r * r * 3.1415926)
print 'cv2计算'+ str(are)
print '自己计算半径' + str(r)
print '\n'

cnt = contours[1]
M = cv2.moments(cnt)
(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
cv2.circle(image,center,radius,(0,255,0),2)

print '系统计算半径'+ str(radius)




cv2.imshow("shooting_rings", image)
cv2.waitKey(0)
cv2.destroyAllWindows()