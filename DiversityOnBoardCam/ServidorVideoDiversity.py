# https://pyshine.com/Socket-Programming-with-multiple-clients/

from time import sleep
import socket
import cv2
from os import getloadavg
import base64
import threading
import struct
import logging
from datetime import datetime

logging.basicConfig(
 filename="test.log",
 level=logging.DEBUG,
 format="%(asctime)s:%(levelname)s:%(message)s"
 )

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 4643
server_socket.bind(("0.0.0.0", port))
server_socket.listen()

"""
GST_ARGUS: Available Sensor modes :
GST_ARGUS: 3264 x 2464 FR = 21.000000 fps Duration = 47619048 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 3264 x 1848 FR = 28.000001 fps Duration = 35714284 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 1920 x 1080 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 1640 x 1232 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 1280 x 720 FR = 59.999999 fps Duration = 16666667 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
GST_ARGUS: 1280 x 720 FR = 120.000005 fps Duration = 8333333 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
"""

cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=(string)NV12, framerate=(fraction)10/1 ! nvvidconv flip-method=2 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink' , cv2.CAP_GSTREAMER)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
font = cv2.FONT_HERSHEY_SIMPLEX

current_frame = None
frame_result = None

def accept_client(client_socket, addr):
    connected_client_ip = client_socket.getpeername()[0]
    logging.log(logging.INFO, f"{connected_client_ip} connected")
    global current_frame
    while True:
        try:
            if frame_result != False:
                data = base64.b64encode(current_frame)
                client_socket.sendall(struct.pack("=L", len(data)) + data)

        except socket.error as e: # Handle client disconnect
            if e.errno == socket.errno.ECONNRESET:
                logging.log(logging.INFO, f"{connected_client_ip} disconnected")
                break
            else:
                raise e
    
def process_camera(camera, encode_param):
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    global current_frame
    global frame_result

    while camera.isOpened():
        ret, frame = camera.read()
        if ret != False:
            scale_percent = 50 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            cv2.putText(frame,datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4],(10,30), font, 0.5,(255,255,255),1,cv2.LINE_AA)
            cv2.putText(frame,"Diversity@DiverBOT",(10,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
            frame_result, current_frame = cv2.imencode('.jpg', frame, encode_param)
            


camera_thread = threading.Thread(target=process_camera, args=(cap, encode_param))
camera_thread.start()

while True:
    try:
        client_socket, addr  = server_socket.accept()
        client_thread = threading.Thread(target=accept_client, args=(client_socket, addr))
        client_thread.start()
    except KeyboardInterrupt:
        raise(Exception)
