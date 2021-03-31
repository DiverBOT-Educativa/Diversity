# https://pyshine.com/Socket-Programming-with-multiple-clients/

import socket
import cv2
#import imutils
import pickle
import threading
import struct
import numpy as np
import sys
import logging
from datetime import datetime

logging.basicConfig(
 filename="test.log",
 level=logging.DEBUG,
 format="%(asctime)s:%(levelname)s:%(message)s"
 )

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5201
server_socket.bind(("0.0.0.0", port))
server_socket.listen()

cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=(string)NV12, framerate=(fraction)10/1 ! nvvidconv flip-method=2 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink' , cv2.CAP_GSTREAMER)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
font = cv2.FONT_HERSHEY_SIMPLEX

def accept_client(client_socket, addr):
    print("Client accepted!")
    while cap.isOpened():
        ret, frame = cap.read()
        if ret != False:
            scale_percent = 50 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            cv2.putText(frame,datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4],(10,30), font, 0.5,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(frame,"Diversity@DiverBOT",(10,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = pickle.dumps(frame,0)
            print("img sent")
            client_socket.sendall(struct.pack("=L", len(data)) + data)
    

while True:
    try:
        client_socket, addr  = server_socket.accept()
        client_thread = threading.Thread(target=accept_client, args=(client_socket, addr))
        client_thread.start()
    except KeyboardInterrupt:
        raise(Exception)