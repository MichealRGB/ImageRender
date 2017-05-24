#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import cv2
import numpy as np

# ph1 = "images/300.jpg"
# ph2 = "images/310.jpg"

threshod = 20

# s1 = cv2.imread(ph1,0)
# s2 = cv2.imread(ph2,0)

def pic_sub(dest,s1,s2):
    for x in range(dest.shape[0]):
        for y in range(dest.shape[1]):
            if(s2[x,y] > s1[x,y]):
                dest[x,y] = s2[x,y] - s1[x,y]
            else:
                dest[x,y] = s1[x,y] - s2[x,y]

            if(dest[x,y] < threshod):
                dest[x,y] = 0
            else:
                dest[x,y] = 255

def get_point(original,modified):
    # print '开始检测中靶点'
    s1 = cv2.imread(original, 0)
    s2 = cv2.imread(modified, 0)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4), (-1, -1))
    # eroded_image1 = cv2.erode(s1, kernel)
    # eroded_image2 = cv2.erode(s2, kernel)

    emptyimg = np.zeros(s1.shape, np.uint8)
    pic_sub(emptyimg, s1, s2)
    ## 提取轮廓
    _, contours, hierarchy = cv2.findContours(emptyimg, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    ## 过滤掉面积较小的杂点
    tmp_contours = []
    less_pixels = 3 * 3
    for i in range(0,len(contours)):
        if cv2.contourArea(contours[i]) > less_pixels:
            tmp_contours.append(contours[i])

    ## 绘制轮廓
    cv2.drawContours(s1, tmp_contours, -1, (0, 255, 0), 2)

    point_arr = []
    ## 取出各个点的中心
    for i in range(0,len(tmp_contours)):
        cnt = tmp_contours[i]
        moment = cv2.moments(cnt)
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
        # print '检测所有中靶点的质心坐标：' + str(cx) + ',' + str(cy)
        point = {'cx':cx,'cy':cy}
        point_arr.append(point)
    # print '#' * 100
    # print '检测完成'

    return point_arr

# get_point()
#
# cv2.imshow("image_sub",s1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()