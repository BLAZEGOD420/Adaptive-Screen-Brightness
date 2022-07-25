"""
Core Concept:
1. Take a picture from camera.
2. Analyze picture to determine the light level.
3. Adjust screen brightness accordingly.
4. Repeat at a set sample rate.

Problem:
How to account for auto adjustment of webcam to maintain a certain brightness level within image?

Solution:
The webcam, when exposed to new conditions, will for a brief moment have a brighter/darker image before adjusting itself. Therefore,
we update the brightness with that initial exposure value, and then stop sampling for x amount of time after which we keep track of the
adjusted brightness level. We continue sampling until the brightness changes by some amount, at which point we repeat the process.

Future Work:
Tack the auto adjustment problem in a more head-on way.

"""

import time
import cv2
from PIL import Image
import screen_brightness_control as sbc
import numpy


def getCurrentBrightness(cam):

    result, image = cam.read()

    if result:
        width, height = len(image[0]), len(image)
        avg = numpy.sum(image) / (width * height * 3)
        return avg

    return -1

def setBrightness(brightness):
    monitors = sbc.list_monitors()
    for monitor in monitors:
        sbc.set_brightness(int(100 * brightness/255) - (int(100 * brightness/255) % 20), display=monitor)


def activateAutoBrightness():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    previous = 0

    while True:
        avg = getCurrentBrightness(cam)

        if avg != -1 and abs(avg - previous) > 25:
            setBrightness(avg)
            time.sleep(2)
            avg = getCurrentBrightness(cam)
            previous = avg            

        time.sleep(1)

def main():
    activateAutoBrightness()

if __name__ == '__main__':
    main()
