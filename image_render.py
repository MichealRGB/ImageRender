#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import cv2
import numpy as np
from matplotlib import pyplot as plt

def contour_area_and_arcLength(list):
    for i in range(0, len(list)):
        print '面积:' + str(cv2.contourArea(list[i]))
        print '周长:' + str(cv2.arcLength(list[i], True))
        print '<' * 100


def get_ring_count(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

    _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        if cv2.arcLength(contours[i],True) > 135.0:
            cv2.drawContours(image, contours[i], -1, (0, 0, 255), 2)
        else:
            cv2.drawContours(image, contours[i], -1, (0, 255, 0), 2)
            print hierarchy[0][i]


    # contour_area_and_arcLength(contours)



    # tmp_arr = hierarchy[0]
    # for i in range(0,len(tmp_arr)):
    #     print
    #     if tmp_arr[i][0] != -1 & tmp_arr[i][1] == -1:
    #         print '>>>识别标靶完成\t'
    #         print '>>>上靶环数为:' + str(tmp_arr[i][0])+'环'
    #         print '#' * 100 + '\n'

    cv2.imshow("image_render", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_threshold(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(gray_image,127,255,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(gray_image,127,255,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(gray_image,127,255,cv2.THRESH_TOZERO_INV)
    titles = ['Gray Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
    images = [gray_image, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in xrange(6):
       plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
       plt.title(titles[i])
       plt.xticks([]),plt.yticks([])
    plt.show()



if __name__ == '__main__':
    # image_array = ['images/2ring.jpg','images/4ring.jpg','images/6ring.jpg','images/8ring.jpg']
    # for single in image_array:
    #     get_ring_count(single)
    get_ring_count('images/ceshi2.jpg')
    # show_threshold('images/ceshi2.jpg')