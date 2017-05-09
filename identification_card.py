#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import cv2
import numpy as np
from matplotlib import pyplot as plt


img = cv2.imread('images/1111.jpg')
## 先进行灰度处理
gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
## 二值法进行处理
ret,thresh = cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)
## 腐蚀处理
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
eroded = cv2.erode(thresh, kernel)
## 提取轮廓
tmp_image, contours, hierarchy = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
## 绘制轮廓
cv2.drawContours(img, contours, -1, (0, 0, 255), 2)


cv2.imshow('image',eroded)
cv2.waitKey(0)
cv2.destroyAllWindows()
