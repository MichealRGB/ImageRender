#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

image = cv2.imread('images/ceshi2.jpg')
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(gray_image,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=1,maxRadius=30)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of circle
    cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

# cv2.imwrite('images/circle.jpg',image)
cv2.imshow('Cicle',image)
cv2.waitKey()
cv2.destroyAllWindows()