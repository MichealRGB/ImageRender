#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import cv2
import numpy as np
import sys
import math

## 这次不考虑所有的数字问题了，直接判断提取轮廓后过滤掉不是圆形的轮廓，利用 pi * r * r试试

def is_circle_contour(contour,minRadius):
    ## 返回值
    is_circle = False
    ## 周长
    perimeter = cv2.arcLength(contour,True)
    ## 面积
    area = cv2.contourArea(contour)
    pi = 3.1415926
    ## 外接矩形
    rect = cv2.boundingRect(contour)
    ## 获取矩形框的宽，高
    x,y,width,height = rect

    print 'cv2 周长' + str(perimeter)
    print 'cv2 面积' + str(area)
    ## 半径
    r = (height + width) / 4
    ## 自己计算的面积
    tmp_area = pi * r * r
    print '计算面积'+str(tmp_area),'计算半径'+str(r)
    print '计算周长' + str(pi * 2 * r)

    ## 面积差
    area_diff = abs(area - tmp_area) / area * 100

    print '面积差是' + str(area_diff)+'%'
    print '\n'

    ## 目前统计的，最大的面积差5.%
    area_diff_thresh = 5

    ## 进行判断筛选
    if (area_diff < area_diff_thresh and r > minRadius):
        is_circle = True

    return is_circle


image = cv2.imread('images/zhenshiba.jpg')
if image is None:
    print('Failed to load image:', image)
    sys.exit(1)

## 灰度处理
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

## 二值法处理
ret,thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

## 膨胀处理(验证后发现膨胀处理后靶子的一些线条变粗了我之前没发现卧槽)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3),(-1,-1))
dilate = cv2.dilate(thresh, kernel)

## 提取轮廓
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

## 保存符合要求的轮廓的点集合
tmp_contours = []
for i in range(0,len(contours)):
    ## 现在要过滤像素点较少的元素
    less_pixels = 10 * 10
    if(math.fabs(cv2.contourArea(contours[i]))) > less_pixels:
        tmp_contours.append(contours[i])

tmp_arr = []
for i in range(0,len(tmp_contours)):
    if is_circle_contour(tmp_contours[i],minRadius=10) == True:
        tmp_arr.append(tmp_contours[i])


# is_circle_contour(tmp_contours[9],minRadius=30)


## 绘制轮廓
cv2.drawContours(image, tmp_arr, -1, (0, 255, 0), 2)

print len(tmp_arr)

## 过滤轮廓

cv2.imshow("shooting_rings", image)
cv2.waitKey(0)
cv2.destroyAllWindows()