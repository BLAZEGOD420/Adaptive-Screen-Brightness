"""
Core Concept:
1. Take a picture from camera.
2. Analyze picture to determine the light level.
3. Adjust screen brightness accordingly.
4. Repeat at a set sample rate (probably around once per 5 seconds).
"""
import time
import cv2
import PIL
from PIL import Image
import screen_brightness_control as sbc

cam_port = 0
cam = cv2.VideoCapture(cam_port)

while True:
    result, image = cam.read()

    if result:
        cv2.imwrite("poop.png", image)
        image = Image.open("poop.png")
        width, height = image.size
        avg = 0
        for x in range(0, width, int(width / 100)):
            for y in range(0, height, int(height / 100)):
                avg += sum(image.getpixel((x, y)))/3
        avg /= 10000
        print(avg)

        monitors = sbc.list_monitors()
        for monitor in monitors:
            sbc.set_brightness(int(100 * avg/255) - (int(100 * avg/255) % 20), display=monitor)

        time.sleep(5)
