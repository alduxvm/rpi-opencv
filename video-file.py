import cv

vidFile = cv.CaptureFromFile( 'crash-480.mp4' )

nFrames = int(  cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FRAME_COUNT ) )
fps = cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FPS )
waitPerFrameInMillisec = int( 1/fps * 1000/1 )

print 'Num. Frames = ', nFrames
print 'Frame Rate = ', fps, ' frames per sec'

for f in xrange( nFrames ):
  frameImg = cv.QueryFrame( vidFile )
  cv.ShowImage( "My Video Window",  frameImg )
  cv.WaitKey( waitPerFrameInMillisec  )

# When playing is done, delete the window
#  NOTE: this step is not strictly necessary, 
#         when the script terminates it will close all windows it owns anyways
cv.DestroyWindow( "My Video Window" )

# import numpy as np
# import cv2

# cap = cv2.VideoCapture('crash-480.mp4')

# while(cap.isOpened()):
#     ret, frame = cap.read()

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()