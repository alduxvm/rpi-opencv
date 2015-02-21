#!/usr/bin/env python

"""color-tracking.py: Color (blue-purple or red) detection using openCV."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2015 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import cv2, math
import numpy as np

class ColourTracker:
  def __init__(self):
    cv2.namedWindow("ColourTrackerWindow", cv2.CV_WINDOW_AUTOSIZE)
    #self.capture = cv2.VideoCapture(0)
    self.capture = cv2.VideoCapture('crash-480.mp4')
    #self.capture.set(3,320)
    #self.capture.set(4,240)
    self.scale_down = 4
  def run(self):
    while True:
      t = cv2.getTickCount()
      f, orig_img = self.capture.read()
      orig_img = cv2.flip(orig_img, 1)
      img = cv2.GaussianBlur(orig_img, (5,5), 0)
      img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
      img = cv2.resize(img, (len(orig_img[0]) / self.scale_down, len(orig_img) / self.scale_down))
      #red_lower = np.array([0, 150, 0],np.uint8)
      #red_upper = np.array([5, 255, 255],np.uint8)
      #blue_lower = np.array([130, 80, 80],np.uint8)
      #blue_upper = np.array([140, 255, 255],np.uint8)
      sensitivity = 15
      lower_white = np.array([0,0,255-sensitivity])
      upper_white = np.array([255,sensitivity,255])
      red_binary = cv2.inRange(img, lower_white, upper_white)
      dilation = np.ones((15, 15), "uint8")
      red_binary = cv2.dilate(red_binary, dilation)
      contours, hierarchy = cv2.findContours(red_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
      max_area = 0
      largest_contour = None
      for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > max_area:
          max_area = area
          largest_contour = contour
      if not largest_contour == None:
        moment = cv2.moments(largest_contour)
        if moment["m00"] > 1000 / self.scale_down:
          rect = cv2.minAreaRect(largest_contour)
          rect = ((rect[0][0] * self.scale_down, rect[0][1] * self.scale_down), (rect[1][0] * self.scale_down, rect[1][1] * self.scale_down), rect[2])
          box = cv2.cv.BoxPoints(rect)
          box = np.int0(box)
          cv2.drawContours(orig_img,[box], 0, (0, 0, 255), 2)
          t = cv2.getTickCount() - t
          print "detection time = %gms" % (t/(cv2.getTickFrequency()*1000.))
          cv2.imshow("ColourTrackerWindow", orig_img)
          if cv2.waitKey(20) == 27:
            cv2.destroyWindow("ColourTrackerWindow")
            self.capture.release()
            break
if __name__ == "__main__":
  colour_tracker = ColourTracker()
  colour_tracker.run()