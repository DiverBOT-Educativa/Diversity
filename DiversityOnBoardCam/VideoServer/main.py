import socket, struct, pickle, threading, cv2

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("127.0.0.1", 9843))
server_socket.listen()

image = cv2.imread("tux.webp")

def accept_client(client_socket, addr):
    result, frame = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    packed_image = pickle.dumps(frame)
    img_size = struct.pack("Q", len(packed_image))
    packet = img_size + packed_image
    client_socket.send(packet)

while True:
    try:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=accept_client, args=(client_socket, addr))
        client_thread.start()
    except KeyboardInterrupt:
        break
