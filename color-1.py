#!/usr/bin/env python

"""color-1.py: Color tracking using openCV. """

""" 
Performance @ 640x480 resolution: 

RMBP -> 0.005s each detection or 200hz 

RPI 2 -> 0.2s each detection or 5hz 

RPI 3 -> 0.17s each detection or 5.88hz 

"""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2016 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"
import cv, time

color_tracker_window = "Color Tracker"

class ColorTracker:

    def __init__(self):
        cv.NamedWindow( color_tracker_window, 1 )
        self.capture = cv.CaptureFromCAM(0)
        width = 640
        height = 480
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height)
        #self.capture = cv.CaptureFromFile('crash-480.mp4')

    def run(self):
        while True:
            img = cv.QueryFrame( self.capture )
            t1 = time.time()
            #blur the source image to reduce color noise 
            cv.Smooth(img, img, cv.CV_BLUR, 3);

            #convert the image to hsv(Hue, Saturation, Value) so its  
            #easier to determine the color to track(hue) 
            hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3)
            cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)

            #limit all pixels that don't match our criteria, in this case we are  
            #looking for purple but if you want you can adjust the first value in  
            #both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
            #a hue range for the HSV color model 
            thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1)

            # White
            sensitivity = 10
            cv.InRangeS(hsv_img, (0, 0, 255-sensitivity), (255, sensitivity, 255), thresholded_img)

            # Red
            #cv.InRangeS(hsv_img, (0, 150, 0), (5, 255, 255), thresholded_img)

            # Blue
            #cv.InRangeS(hsv_img, (100, 50, 50), (140, 255, 255), thresholded_img)

            # Green
            #cv.InRangeS(hsv_img, (40, 50, 50), (80, 255, 255), thresholded_img)

            #determine the objects moments and check that the area is large  
            #enough to be our object 
            mat=cv.GetMat(thresholded_img)
            moments = cv.Moments(mat, 0)
            area = cv.GetCentralMoment(moments, 0, 0)

            #there can be noise in the video so ignore objects with small areas 
            if(area > 10000):
                #determine the x and y coordinates of the center of the object 
                #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
                x = cv.GetSpatialMoment(moments, 1, 0)/area
                y = cv.GetSpatialMoment(moments, 0, 1)/area
                x = int(round(x))
                y = int(round(y))

                #create an overlay to mark the center of the tracked object 
                overlay = cv.CreateImage(cv.GetSize(img), 8, 3)
                cv.Circle(overlay, (x, y), 2, (255, 255, 255), 20)
                cv.Add(img, overlay, img)
                #add the thresholded image back to the img so we can see what was  
                #left after it was applied 
                t2 = time.time()
                cv.Merge(thresholded_img, None, None, None, img)
                print "detection time = %gs x=%d,y=%d" % ( round(t2-t1,3) , x, y)
            
            #display the image  
            cv.ShowImage(color_tracker_window, img)

            if cv.WaitKey(10) == 27:
                break

if __name__=="__main__":
    color_tracker = ColorTracker()
    color_tracker.run()