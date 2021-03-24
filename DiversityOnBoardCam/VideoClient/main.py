import socket
import struct
import pickle
import cv2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 9843))

payload_size = struct.calcsize("Q")
data = b""

while True:
    while len(data) < payload_size:
        packet = s.recv(4096)
        if packet == None:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += s.recv(4096)

    packed_img = data[:msg_size] # Limita data a el tamaño del mensaje
    img = pickle.loads(packed_img, encoding="bytes")
    frame = cv2.imdecode(img, cv2.IMREAD_COLOR)
    cv2.imshow("Image window", frame)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
