# https://stackoverflow.com/questions/36503536/send-video-over-tcp-using-opencv-and-sockets-in-raspberry-pi
# ejecutar en PC
import cv2
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

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Esperando conexion")
clientsocket.connect(('192.168.1.138', 4643))
print("Conexion establecida")
logging.debug("Conectado con el servidor")

payload_size = struct.calcsize("=L")
data = b''
while True:
    while len(data) < payload_size:
        data += clientsocket.recv(4096)
        logging.log(logging.DEBUG, str(data))
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
