# https://stackoverflow.com/questions/36503536/send-video-over-tcp-using-opencv-and-sockets-in-raspberry-pi
# ejecutar en PC
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import logging
from datetime import datetime

logging.basicConfig(
 filename="test.log",
 level=logging.DEBUG,
 format="%(asctime)s:%(levelname)s:%(message)s"
 )

"""
GST_ARGUS: Available Sensor modes :
GST_ARGUS: 3264 x 2464 FR = 21.000000 fps Duration = 47619048 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 3264 x 1848 FR = 28.000001 fps Duration = 35714284 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 1920 x 1080 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 1640 x 1232 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 1280 x 720 FR = 59.999999 fps Duration = 16666667 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 1280 x 720 FR = 120.000005 fps Duration = 8333333 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
"""
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=(string)NV12, framerate=(fraction)10/1 ! nvvidconv flip-method=2 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink' , cv2.CAP_GSTREAMER)
#cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv flip-method=2 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink' , cv2.CAP_GSTREAMER)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Esperando conexion")
clientsocket.connect(('192.168.1.138', 5201))
print("Conexion establecida")
logging.debug("Conectado con el servidor")

payload_size = struct.calcsize("=L")
data = b''
while True:
    while len(data) < payload_size:
        data += clientsocket.recv(4096)
        print(str(data))
    packed_msg_size = data[:payload_size]
    print("packed_msg_size: ", str(packed_msg_size))
    data = data[payload_size:]
    msg_size = struct.unpack("=L", packed_msg_size)[0]

    print(msg_size)

    while len(data) < msg_size :
        data += clientsocket.recv(4096)
    print("Datos recibidos")
    frame_data = data[:msg_size]
    data = data[msg_size:]

    print(len(data), len(frame_data))
    
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('Diversity real time video',frame)
    cv2.waitKey(10)
