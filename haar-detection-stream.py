#!/usr/bin/env python

"""haar-detection-stream.py: Detect haar body from a CCTV camera."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2017 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

import cv2
import imutils
from urllib2 import urlopen
import numpy as np

# Source from http://212.170.22.153:8080/view/viewer_index.shtml?id=412 - test first in VLC
stream = urlopen('http://212.170.22.153:8080/mjpg/video.mjpg') # mjpg stream camera from an Axis network camera in Spain
#stream = urlopen('http://10.0.0.1:60152/liveview.JPG?%211234%21http%2dget%3a%2a%3aimage%2fjpeg%3a%2a%21%21%21%21%21') # qx10 
bytes = bytes()

# Change to the haar as desired from what you want to test or use
#classifier = cv2.CascadeClassifier('haars/face.xml')
classifier = cv2.CascadeClassifier('haars/fullbody.xml')
#classifier = cv2.CascadeClassifier('haars/lowerbody.xml')
#classifier = cv2.CascadeClassifier('haars/upperbody.xml')

while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR) # decode image
        image = imutils.resize(i, width=min(600, i.shape[1])) # resize image (optional)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    	image = imutils.resize(image, width=min(600, image.shape[1])) # resize

    	detection = classifier.detectMultiScale(image, 1.1, 2)

    	for (x,y,w,h) in detection:
	        cv2.rectangle(image, (x,y), (x+w, y+h),(255,0,0),2)

		cv2.imshow('frame', image)
		if cv2.waitKey(1) == 27:
			exit(0)
