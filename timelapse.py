import numpy as np
import cv2
import time

# time delay between frames
delay = 30

# folder to write to
folder = 'timelapse/c920/'
folder2 = 'timelapse/nir/'

c920 = cv2.VideoCapture(0)
nir = cv2.VideoCapture(1)

c920.set(3, 1920)
c920.set(4, 1080)

nir.set(3, 1600)
nir.set(4, 1200)

ret, frame = c920.read()
ret, frame = nir.read()
count = 1
while(1):
    ret, frame = c920.read()
    ret2, frame2 = nir.read()
    frame_num = "%08d" % (count,)
    cv2.imwrite(folder + frame_num + '.jpg', frame)
    k = cv2.waitKey(1)
    cv2.imwrite(folder2 + frame_num + '.jpg', frame2)
    k = cv2.waitKey(1)
    count = count + 1
    time.sleep(delay)

cv2.destroyAllWindows()
c920.release()
nir.release()