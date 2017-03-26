![Altax](https://altax.net/images/altax.png "Altax")

# rpi-opencv

Test scripts for using openCV with python, all scripts designed to work on a raspberry pi, but will work on Mac's and Linux. 

![rpi-opencv-python-noir](https://altax.net/images/face-rpi-opencv.jpg "rpi face detection opencv python with noir camera")

## Video demo:

[![Drone Color tracking](http://img.youtube.com/vi/xlQw_mnJtNQ/0.jpg)](http://www.youtube.com/watch?v=xlQw_mnJtNQ)

## Performance:

The performance tests for the color tracking algorithms was performed using a Raspberry Pi NoIR Camera, fixing the resolution at 640x480 pixels and finding the colour white (light emitted using infra-red LEDs).

|        | Color 1 | Color 2 | Color 3 | Color 4 | Color 5 | Color 6 |
| -------|:-------:| -------:| -------:| -------:| -------:| -------:|
| RPI 2  |  0.20s  |  0.21s  |  0.165s |  0.15s  |  0.15s  |  0.15s  |
| RPI 3  |  0.17s  |  0.17s  |  0.129s |  0.124s |  0.12s  |  0.12s  |

![rpi-opencv-tests](https://altax.net/images/rpi-opencv-tests.jpg "Performance tests for colour finding")

## What do you need?

* Raspberry pi (I'm using a RPI 2 and RPI 3)
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
-- You may have to reboot your rpi if it wasn't enabled.

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

> Important!! This code is not enterely mine, its copy-pasted from different codes found on the internet, I just made them easier to read and change and because I'm lazy and I prefer to code in my mac than in the rpi and github its a great way to put code inside the rpi ;)


## Working on rpi!

![ss-opencv-python](https://altax.net/images/ss-rpi-usb.png "ss face detection opencv python usb")

## Working on mac!!

![mac-opencv-python](https://altax.net/images/face-mac-opencv.png "mac face detection opencv python")
