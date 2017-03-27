#!/usr/bin/env python

"""people-detection.py: Detect cars from a web camera."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2017 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

import numpy as np
import cv2
import imutils
from imutils.object_detection import non_max_suppression

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('video.mp4')

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

record = False

if record:
    fps = 15
    capSize = (400,226) # this is the size of my source video
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
    vout = cv2.VideoWriter()
    success = vout.open('output.mov',fourcc,fps,capSize,True) 

while(True):
    ret, image = cap.read()
    
    image = imutils.resize(image, width=min(400, image.shape[1]))
    orig = image.copy()

    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        padding=(8, 8), scale=1.05)

    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    cv2.imshow('frame',image)
    if record:
        vout.write(image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if record:
    vout.release() 
    vout = None
cv2.destroyAllWindows()
