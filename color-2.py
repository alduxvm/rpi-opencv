#!/usr/bin/env python

"""color-2.py: Color detection using openCV."""

""" 
Performance @ 640x480 resolution: 

RMBP -> 0.006s each detection or 166hz 

RPI 2 -> 0.21s each detection or 4.76hz 

RPI 3 -> 0.17 each detection or 5.88hz 

"""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2016 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

import sys
import cv
import time 

min_size = (20, 20)
image_scale = 4
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0

def detect_and_draw(img):
    t1 = time.time()

    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
			       cv.Round (img.height / image_scale)), 8, 1)

    # blur the source image to reduce color noise 
    cv.Smooth(img, img, cv.CV_BLUR, 3);
    hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)
    thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
    #cv.InRangeS(hsv_img, (120, 80, 80), (140, 255, 255), thresholded_img)

    # White
    sensitivity = 15
    cv.InRangeS(hsv_img, (0, 0, 255-sensitivity), (255, sensitivity, 255), thresholded_img)

    # Red
    #cv.InRangeS(hsv_img, (0, 150, 0), (5, 255, 255), thresholded_img)

    # Blue
    #cv.InRangeS(hsv_img, (100, 50, 50), (140, 255, 255), thresholded_img)

    # Green
    #cv.InRangeS(hsv_img, (40, 50, 50), (80, 255, 255), thresholded_img)

    mat=cv.GetMat(thresholded_img)
    moments = cv.Moments(mat, 0)
    area = cv.GetCentralMoment(moments, 0, 0)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(area > 5000):
        #determine the x and y coordinates of the center of the object 
        #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
        x = cv.GetSpatialMoment(moments, 1, 0)/area
        y = cv.GetSpatialMoment(moments, 0, 1)/area
        x = int(round(x))
        y = int(round(y))

        #create an overlay to mark the center of the tracked object 
        overlay = cv.CreateImage(cv.GetSize(img), 8, 3)

        cv.Circle(overlay, (x, y), 2, (0, 0, 0), 20)
        cv.Add(img, overlay, img)
        #add the thresholded image back to the img so we can see what was  
        #left after it was applied 
        #cv.Merge(thresholded_img, None, None, None, img)
        t2 = time.time()
        message = "Color tracked!"
        print "detection time = %gs x=%d,y=%d" % ( round(t2-t1,3) , x, y)

    cv.ShowImage("Color detection", img)



if __name__ == '__main__':

    capture = cv.CreateCameraCapture(0)
    #capture = cv.CaptureFromFile('roomba.mp4')
    cv.NamedWindow("Color detection", 1)

    width = 640 #leave None for auto-detection
    height = 480 #leave None for auto-detection


    if width is None:
    	width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
    else:
    	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    

    if height is None:
	height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
    else:
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)
            detect_and_draw(frame_copy)
            if cv.WaitKey(10) >= 0:
                break
    cv.DestroyWindow("Color detection")
