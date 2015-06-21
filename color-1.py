#!/usr/bin/env python

"""color-1st.py: Color tracking using openCV. """

""" Performance: on video (mp4 sample) and running in a RMBP -> 0.005s each detection or 200hz """

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2015 Aldux.net"

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
        #self.capture = cv.CaptureFromCAM(0)
        self.capture = cv.CaptureFromFile('crash-480.mp4')

    def run(self):
        while True:
            img = cv.QueryFrame( self.capture )
            #t = cv.GetTickCount()
            t = time.time()
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
            sensitivity = 10
            cv.InRangeS(hsv_img, (0, 0, 255-sensitivity), (255, sensitivity, 255), thresholded_img)

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

                #print 'x: ' + str(x) + ' y: ' + str(y) + ' area: ' + str(area) 

                #create an overlay to mark the center of the tracked object 
                overlay = cv.CreateImage(cv.GetSize(img), 8, 3)

                cv.Circle(overlay, (x, y), 2, (255, 255, 255), 20)
                cv.Add(img, overlay, img)
                #add the thresholded image back to the img so we can see what was  
                #left after it was applied 
                cv.Merge(thresholded_img, None, None, None, img)
                message = "color tracked!"
            else:
                message = ""

            t = time.time() - t
            print "detection time = %gs %s" % ( round(t,3) , message)
            #display the image  
            cv.ShowImage(color_tracker_window, img)

            if cv.WaitKey(10) == 27:
                break

if __name__=="__main__":
    color_tracker = ColorTracker()
    color_tracker.run()