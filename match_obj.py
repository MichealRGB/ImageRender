#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

## 原图
image = cv2.imread('images/ceshi2.jpg',0)
if image is None:
    print('Failed to load image:', image)
    sys.exit(1)

def find_template_obj(tmp_image):
    template_image = cv2.imread(tmp_image,0)
    if template_image is None:
        print('Failed to load tmp_image:', tmp_image)
        sys.exit(1)
    w, h = template_image.shape[::-1]

    ## 匹配
    res = cv2.matchTemplate(image, template_image, cv2.TM_CCOEFF_NORMED)
    ##
    threshold = 0.95
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (50,255,0), 2)

if __name__ == '__main__':
    images_arr = ['images/shuzi6.jpg','images/shuzi7.jpg','images/shuzi8.jpg','images/shuzi9.jpg','images/shuzi10.jpg']
    for single_image in images_arr:
        find_template_obj(tmp_image=single_image)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



