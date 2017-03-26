#!/usr/bin/env python

"""haar-detection-several.py: Detect cars from a CCTV camera."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2017 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

import cv2
import imutils

cap = cv2.VideoCapture(0) # Web camera attached to the rpi or computer

# Change to the haar as desired from what you want to test or use
classifier = cv2.CascadeClassifier('haars/eye.xml')
#classifier = cv2.CascadeClassifier('haars/smile.xml')
#classifier = cv2.CascadeClassifier('haars/fullbody.xml')
#classifier = cv2.CascadeClassifier('haars/lowerbody.xml')
#classifier = cv2.CascadeClassifier('haars/upperbody.xml')

while True:
    ret, image = cap.read()
    image = imutils.resize(image, width=min(600, image.shape[1])) # resize

    detection = classifier.detectMultiScale(image, 1.1, 2)

    for (x,y,w,h) in detection:
        cv2.rectangle(image, (x,y), (x+w, y+h),(255,0,0),2)

    cv2.imshow('frame', image)
    if cv2.waitKey(1) == 27:
        exit(0)
