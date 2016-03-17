#!/usr/bin/env python

"""color-7.py: Find the brightest spot on a image (find the white color around a radius)."""

"""
Performance @ 640x480 resolution: 

RMBP -> 

RPI 2 -> 

RPI 3 ->

"""

__author__ = "Harald Kirkerod"
__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2016 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import cv2
import time, threading


class vision:
	"""
	1st argumet:
	- True -> if you want to see camera output
	- False -> if you dont want to see camera output
	"""
	def __init__(self, show):
		self.cam = cv2.VideoCapture(0)
		self.position = {'found':False,'x':0,'y':0,'rate':0.0}
		self.cam.set(3,640)
		self.cam.set(4,480)
		self.show = show
		self.radius = 31
		self.threshold = 200

	def findBright(self):
		try:
			while True:
				t1 = time.time()
				ret, frame = self.cam.read()

				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				gray = cv2.GaussianBlur(gray, (self.radius, self.radius), 0)
				(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

				t2 = time.time()
				if maxVal > self.threshold:
					cv2.circle(frame, maxLoc, self.radius, (255, 0, 0), 2)
					#t2 = time.time()
					self.position['found']=True
					self.position['x']=maxLoc[0]
					self.position['y']=maxLoc[1]
					self.position['rate']=round(1.0/(t2-t1),1)
					print self.position

				if self.show:
					cv2.imshow('vision', frame)

				if cv2.waitKey(1) == 27:
					break
		except Exception,error:
			print "Error in findcolor: "+str(error)

def bright():
	test = vision(True)
	test.findBright()

if __name__ == "__main__":
	try:
		#test = vision(True)
		#test.findBright()
		bright()
		#testThread = threading.Thread(target=bright)
		#testThread.daemon=True
		#testThread.start()
	except Exception,error:
		print "Error in main: "+str(error)
	except KeyboardInterrupt:
		print "Keyboard Interrupt, exiting."
		exit()
