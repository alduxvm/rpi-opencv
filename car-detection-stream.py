#!/usr/bin/env python

"""car-detection-stream.py: Detect cars from a CCTV camera."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2017 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

import numpy as np
import cv2
from urllib2 import urlopen
import imutils

# Stream from public cameras (http://www.webcamxp.com/publicipcams.aspx) - test first using VLC
stream = urlopen('http://96.10.1.168/mjpg/video.mjpg') # mjpg stream camera from an Axis network camera in a random place
bytes = bytes()

#vehicle_classifier = cv2.CascadeClassifier('haars/cascade.xml') # from http://mark-kay.net/2014/06/24/detecting-vehicles-cctv-image/
vehicle_classifier = cv2.CascadeClassifier('haars/cars.xml') # from https://github.com/andrewssobral/vehicle_detection_haarcascades -> works the best
#vehicle_classifier = cv2.CascadeClassifier('haars/cas1.xml') # from 
#vehicle_classifier = cv2.CascadeClassifier('haars/cas2.xml') # from 
#vehicle_classifier = cv2.CascadeClassifier('haars/cas3.xml') # from 
#vehicle_classifier = cv2.CascadeClassifier('haars/cas4.xml') # from 
#vehicle_classifier = cv2.CascadeClassifier('haars/cars2.xml') # from https://github.com/andrewssobral/vehicle_detection_haarcascades

record = True
if record:
    fps = 10
    capSize = (1200,675) # Size of video when is resized (original stream 1080x1920)
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
    vout = cv2.VideoWriter()
    success = vout.open('output.mov',fourcc,fps,capSize,True) 

while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR) # decode image
        image = imutils.resize(i, width=min(1200, i.shape[1])) # resize image (optional)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        #vehicles = vehicle_classifier.detectMultiScale(gray, 1.1, 2, maxSize=(200,200))
        vehicles = vehicle_classifier.detectMultiScale(gray, 1.1, 5)
        print len(vehicles), 'vehicles found...' 
        for (x,y,w,h) in vehicles:
            cv2.rectangle(image, (x,y), (x+w, y+h),(255,0,0),2)

        cv2.imshow('frame', image)
        if record:
            vout.write(image)
        if cv2.waitKey(1) == 27:
            exit(0)

if record:
    vout.release() 
    vout = None
cv2.destroyAllWindows()