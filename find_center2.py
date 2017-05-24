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

##
image = cv2.imread('images/113.jpg')
if image is None:
    print('Failed to load image:', image)
    sys.exit(1)

## 膨胀处理(验证后发现膨胀处理后靶子的一些线条变粗了我之前没发现卧槽)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4),(-1,-1))
eroded_image = cv2.erode(image,kernel)

## 灰度处理
gray_image = cv2.cvtColor(eroded_image,cv2.COLOR_BGR2GRAY)

## 二值法处理
ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

## 提取轮廓
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

## 过滤小面积的元素，现在要找到中心圆环的轮廓
tmp_contours = []
less_pixels = 25 * 25
for i in range(0,len(contours)):
    if cv2.contourArea(contours[i]) > less_pixels:
        if is_circle_contour(contours[i]) == True:
            tmp_contours.append(contours[i])

# print '过滤后的tmp_contours数组 ->' + str(len(tmp_contours))

## 取出质心坐标
cnt = tmp_contours[0]
moment = cv2.moments(cnt)
cx = int(moment['m10'] / moment['m00'])
cy = int(moment['m01'] / moment['m00'])
# print '10环质心坐标：' + str(cx) +',' + str(cy)
# print  '#' * 100

## 绘制质心
cv2.circle(image, (cx, cy), 2, (0, 0, 255), 2)

(x,y),radius = cv2.minEnclosingCircle(cnt)

for i in range(1,7):
    cv2.circle(image,(int(x),int(y)),int(radius * i),(0,0,255),2)


# 质心坐标为375,496
# 质心坐标为226,484
# 质心坐标为471,423
# 质心坐标为324,423
# 质心坐标为279,386
# 质心坐标为362,380
# 质心坐标为346,364
# 检测所有中靶点的质心坐标：346,364

## 绘制轮廓
# cv2.drawContours(image, tmp_contours, -1, (0, 255, 0), 2)

ph1 = "images/251.png"
ph2 = "images/250.png"
## 取到所有中靶子点的数组
point_arr = get_point(original=sys.argv[1],modified=sys.argv[2])
# point_arr = get_point(original='image1/200.jpg',modified='image1/220.jpg')

for i in range(0,len(point_arr)):
    dict = point_arr[i]
    px = int(dict['cx'])
    py = int(dict['cy'])
    ## 判断点在哪个里
    tmp_r = ((px - x) * (px - x) + (py - y) * (py - y)) ** 0.5
    ring = tmp_r / radius
    # print '系统计算10环半径：' + str(int(radius))
    # print '计算中靶点的半径：' + str(tmp_r)
    print '计算环数：'  + str(10 - int(ring)) + ';'
    # print '*' * 100


# cv2.imshow("find_center", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
