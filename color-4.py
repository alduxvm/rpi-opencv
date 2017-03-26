#!/usr/bin/env python

"""color-4.py: Color detection using openCV."""

"""
Performance @ 640x480 resolution: 

RMBP -> 0.005s each detection or 20hz 

RPI 2 -> 0.15s each detection or 6.6hz 

RPI 3 -> 0.124s each detection or 8.06hz 

"""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2015 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import numpy as np
import cv2
import time


#cam = cv2.VideoCapture(0)
cam = cv2.VideoCapture('slung-load.mp4')
cam.set(3,640)
cam.set(4,480)

while ( True ):
        t1 = time.time()
        ret, frame = cam.read()

        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        # Blue
        #color = cv2.inRange(hsv,np.array([100,50,50]),np.array([140,255,255]))

        # Black
        color = cv2.inRange(hsv,np.array([0,0,0]),np.array([150,150,150]))

        # Green
        #color = cv2.inRange(hsv,np.array([40,50,50]),np.array([80,255,255]))

        # Red
        #color = cv2.inRange(hsv,np.array([0,150,0]),np.array([5,255,255]))

        # White
        #sensitivity = 10
        #color = cv2.inRange(hsv,np.array([0,0,255-sensitivity]),np.array([255,sensitivity,255]))

        # Change to select color
        image_mask=color

        element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        image_mask = cv2.erode(image_mask,element, iterations=2)
        image_mask = cv2.dilate(image_mask,element,iterations=2)
        image_mask = cv2.erode(image_mask,element)

        contours, hierarchy = cv2.findContours(image_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        maximumArea = 10
        bestContour = None
        for contour in contours:
            currentArea = cv2.contourArea(contour)
            if currentArea > maximumArea:
                bestContour = contour
                maximumArea = currentArea
        #Create a bounding box around the biggest color object
        if bestContour is not None:
            x,y,w,h = cv2.boundingRect(bestContour)
            cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
            t2 = time.time()
            print "detection time = %gs x=%d,y=%d" % ( round(t2-t1,3) , x, y)

        #output=cv2.bitwise_and(frame,frame,mask=image_mask)
        cv2.imshow('Original',frame)
        #cv2.imshow('Image Mask',image_mask)
        #cv2.imshow('Output',output)

        if cv2.waitKey(1) == 27:
                break

cv2.destroyAllWindows()
cam.release()
