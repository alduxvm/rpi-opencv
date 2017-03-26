#!/usr/bin/env python

"""color-3.py: Color detection using openCV."""

""" 
Performance @ 640x480 resolution: 

RMBP -> 0.03s each detection or 33hz 

RPI 2 -> 0.165s each detection or 6.06hz 

RPI 3 -> 0.129s each detection or 7.75hz 

"""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2016 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import cv2, math
import numpy as np
import time, threading
import multiprocessing

class ColorTracker:
    def __init__(self, targetcolor, show, width, height):
        #self.capture = cv2.VideoCapture(0)
        self.capture = cv2.VideoCapture('slung2.mp4')
        self.tracker = {'color':targetcolor,'found':False,'x':0.0,'y':0.0,'serx':0.0,'sery':0.0,'elapsed':0.0}
        self.targetcolor = targetcolor
        self.show = show
        self.width = width
        self.height = height
        self.capture.set(3,self.width)
        self.capture.set(4,self.height)
        self.scale_down = 4
        if self.show:
            cv2.namedWindow("ColorTrackerWindow", cv2.CV_WINDOW_AUTOSIZE)
    def findColor(self):
        while True:
            t1 = time.time()
            f, orig_img = self.capture.read()
            orig_img = cv2.flip(orig_img, 1)
            img = cv2.GaussianBlur(orig_img, (5,5), 0)
            img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
            img = cv2.resize(img, (len(orig_img[0]) / self.scale_down, len(orig_img) / self.scale_down))
            # Blue
            if self.targetcolor is 'blue':
                color = cv2.inRange(img,np.array([100,50,50]),np.array([140,255,255]))
            # Green
            elif self.targetcolor is 'green':
                color = cv2.inRange(img,np.array([40,50,50]),np.array([80,255,255]))
            # Red
            elif self.targetcolor is 'red':
                color = cv2.inRange(img,np.array([0,150,0]),np.array([5,255,255]))
            # Black
            elif self.targetcolor is 'black':
                color = cv2.inRange(img,np.array([0,0,0]),np.array([100,100,100]))
            # White
            else:
                sensitivity = 10
                color = cv2.inRange(img,np.array([0,0,255-sensitivity]),np.array([255,sensitivity,255]))
            binary = color
            dilation = np.ones((15, 15), "uint8")
            binary = cv2.dilate(binary, dilation)
            contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            max_area = 0
            largest_contour = None
            for idx, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    largest_contour = contour
            if largest_contour is not None:
                moment = cv2.moments(largest_contour)
                if moment["m00"] > 1000 / self.scale_down:
                    rect = cv2.minAreaRect(largest_contour)
                    rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
                    box = cv2.cv.BoxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(orig_img,[box], 0, (0, 0, 255), 2)
                    x = rect[0][0]
                    y = rect[0][1]
                    self.tracker['found']=True
                    self.tracker['elapsed'] = round(time.time() - t1,3)
                    self.tracker['x'] = round(x,3)
                    self.tracker['y'] = round(y,3)
                    #Check correct width with X and height with Y
                    self.tracker['serx'] = round((self.tracker['x']-(self.width/2.0))*(50.0/(self.width/2)),3)
                    self.tracker['sery'] = round((self.tracker['y']-(self.height/2.0))*(50.0/(self.height/2)),3)
                    print self.tracker
                    #print "detection time = %gs x=%d,y=%d" % ( round(t2-t1,3) , x, y)
                    if self.show:
                        cv2.imshow("ColorTrackerWindow", orig_img)   
                    if cv2.waitKey(20) == 27:
                        if self.show:
                            cv2.destroyWindow("ColorTrackerWindow")
                        self.capture.release()
                        break
            else:
                if self.show:
                    cv2.imshow("ColorTrackerWindow", orig_img)
                self.tracker['found']=False
                print self.tracker

color_tracker = ColorTracker('black',True,640,480)
color_tracker.findColor()
jobs = []

"""
try:
    #testThread = threading.Thread(target=color_tracker.findColor)
    #testThread.daemon=True
    #testThread.start()
    #testThread.join()
    p = multiprocessing.Process(target=color_tracker.findColor)
    jobs.append(p)
    p.start()
    #while True:
    #    print color_tracker.tracker
    #    if cv2.waitKey(1) == 27:
    #       break
    #    time.sleep(0.1)
    #    pass
except Exception,error:
    print "Error in main: "+str(error)
"""
