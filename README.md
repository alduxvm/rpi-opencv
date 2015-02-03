# rpi-opencv

Test scripts for using openCV with python, all running on a raspberry pi. Also works on Mac running yosemite after installing opencv using brew and resolving all problems and warnings.

![rpi-opencv-python-noir](http://www.aldux.net/images/face-rpi-opencv.JPG "rpi face detection opencv python with noir camera")

## What do you need?

* Raspberry pi (I'm using a rpi B+)
* Camera module (I'm using the NOIR camera)
* USB webcam (I'm using a logitech pro 9000)
* wifi dongle for the rpi or ethernet (duhhh)

## How?

The first thing to do is to find out that everything is working... 

Your rpi must be connected to internet, and updated...

```
sudo apt-get update
sudo apt-get upgrade
```

Install the essentials:
```
sudo apt-get install python-wxgtk2.8 python-matplotlib python-opencv python-pip python-numpy
```

Then, plug the webcam and check is working using this nice app:
```
sudo apt-get guvcview
```

If you can see video, then everything is ok, we can proceed to check the other camera module, go ahead and plug it to the CSI port of your rpi, then make sure the camera module is enabled using the configuration tool of the rpi :
```
sudo raspi-config
```
-- You may have to reboot your rpi if it wasnt enabled.

Test this module using this command:
```
raspivid -t 0
```
If you see video, then we are good!! :)

### Important...

The rpi camera module is accessed via the MMAL and V4L apis... this means that we cannot use it as a webcam, but if we run this command we will able to use this great camera module as a webcam and with this examples.
```
sudo modprobe bcm2835-v4l2
```

Then pick one of the testing scripts and have fun!! 

> Important!! This code is not enterely mine, its copy-pasted from different codes found on the internet, I just made them easier to read and change and becuase I'm lazy and I prefer to code in my mac than in the rpi and github its a great way to put code inside the rpi ;)


## Working on rpi!

![ss-opencv-python](http://www.aldux.net/images/ss-rpi-usb.png "ss face detection opencv python usb")

## Working on mac!!

![mac-opencv-python](http://www.aldux.net/images/face-mac-opencv.JPG "mac face detection opencv python")
