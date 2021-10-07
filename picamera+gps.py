from picamera.array import PiRGBArray  # lib. for
from picamera import PiCamera
import time
import cv2
import os

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# writing file
datetime = time.strftime('time%H:%M:%Sdate %d%m')
# print(datetime)
path = ("/home/pi/" + datetime + "/")
os.mkdir(path)
file = open(path + "speed.csv", "w")

#  liberary for gps
import board
import busio
import adafruit_gps

import serial

uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")


def speed():
    last_print = time.monotonic()
    while True:
        gps.update()
        current = time.monotonic()
        if current - last_print >= 0.031:
            last_print = current
            if not gps.has_fix:
                continue
            if gps.speed_knots is not None:
                # print("Speed: {} knots".format(gps.speed_knots))
                gspeed = gps.speed_knots
                return gspeed


# capture frames from the camera
counter = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    # show the frame
    # cv2.imshow("Frame", image)
    # key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    file = open(path + "/" + "speed.csv", "a")
    path2 = path
    get_speed = speed()
    file.write(str(get_speed) + "\n")

    counter += 1
    cv2.imwrite(path2 + str(counter) + ".jpg", image)

    file.close()



