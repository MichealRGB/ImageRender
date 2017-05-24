#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__= "Micheal"

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images/ceshi2.jpg')

## 先进行灰度处理
gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

## 二值法进行处理
ret,thresh = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)

## 腐蚀处理
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
eroded = cv2.erode(thresh, kernel)
#
## 提取轮廓
tmp_image, contours, hierarchy = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

## 绘制轮廓
cv2.drawContours(img, contours, -1, (0, 0, 0), 2)

for singel in contours:
    if cv2.contourArea(singel) < 10.0 or cv2.contourArea(singel) > 200.0 :
        print '-' *100
    else:
        print cv2.contourArea(singel)
        x, y, w, h = cv2.boundingRect(singel)
        img = cv2.rectangle(img, (x - 1, y - 1), (x + w + 1, y + h + 1), (0, 0, 255), 2)

# cv2.imshow('image',img)
# cv2.imshow('lunkuo',tmp_image)
# cv2.imshow("Eroded Image", eroded)
# cv2.imshow('threshold',thresh)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
def draw_circle(event,x,y,flags,param):
  if event==cv2.EVENT_MOUSEMOVE:
    cv2.circle(img,(x,y),100,(255,0,0),-1)

img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
  cv2.imshow('image',img)
  if cv2.waitKey(20)&0xFF==27:
    break
cv2.destroyAllWindows()


def show_threshold(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5), (-1, -1))
    dilate = cv2.dilate(gray_image, kernel)
    ret,thresh1 = cv2.threshold(dilate,255,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    ret,thresh2 = cv2.threshold(dilate,255,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    ret,thresh3 = cv2.threshold(dilate,0,255,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(dilate,0,255,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(dilate,0,255,cv2.THRESH_TOZERO_INV)
    titles = ['Gray Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
    images = [gray_image, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in xrange(6):
       plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
       plt.title(titles[i])
       plt.xticks([]),plt.yticks([])
    plt.show()

# show_threshold("images/zhenshiba.jpg")