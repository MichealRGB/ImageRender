#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import cv2
import sys
from Image_sub import get_point

def is_circle_contour(contour):
    ## 返回值
    is_circle = False
    ## 面积
    area = cv2.arcLength(contour,True)
    pi = 3.1415926
    ## 外接矩形
    rect = cv2.boundingRect(contour)
    ## 获取矩形框的宽，高
    x,y,width,height = rect
    # print 'cv2 周长' + str(area)
    ## 半径
    r = (height + width) / 4
    ## 自己计算的面积
    tmp_area = pi * r * 2
    # print '计算周长'+str(tmp_area),'计算半径'+str(r)
    ## 面积差
    area_diff = abs(area - tmp_area) / area * 100

    # print '周长差是' + str(area_diff)+'%'
    # print '\n'

    ## 目前统计的，最大的面积差5.%
    area_diff_thresh = 5

    ## 进行判断筛选
    if (area_diff < area_diff_thresh):
        is_circle = True

    return is_circle


image = cv2.imread('images/777.jpg')
if image is None:
    print('Failed to load image:', image)
    sys.exit(1)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4),(-1,-1))

eroded_image = cv2.erode(image,kernel)

gray_image = cv2.cvtColor(eroded_image,cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

outermost_contours = []
tmp_contours = []
less_pixels = 25 * 25
for i in range(0,len(contours)):
    if cv2.contourArea(contours[i]) > less_pixels:
        if is_circle_contour(contours[i]) == True:
            tmp_contours.append(contours[i])
        else:
            outermost_contours.append(contours[i])

cv2.drawContours(image, outermost_contours, -1, (0, 255, 0), 2)

cv2.imshow("find_center", image)
cv2.waitKey(0)
cv2.destroyAllWindows()