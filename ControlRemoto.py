# https://pyshine.com/Socket-Programming-with-multiple-clients/

from time import sleep
import socket
import threading
import logging
from datetime import datetime
import queue
from DiversityControlServos.servoController import ServoController
from DiversityControlMotores.MotorController import MotorController
from kineDiversity import AngleCalculator


Comandos=queue.Queue()

logging.basicConfig(
 filename="ControlRemoto.log",
 level=logging.DEBUG,
 format="%(asctime)s:%(levelname)s:%(message)s"
 )

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 5005
server_socket.bind(("0.0.0.0", port))





def listeningThread():
    global sc, CamaraTilt, CamaraAz, mt, angulos
    while True:
        data, addr = server_socket.recvfrom(1024)
        print("Datos recividos de {}: {}".format(addr, data))
        print("Comando: {} ".format(str(data[:3])))
        print("Dato: {}".format(int(data[3:])))
        comando = data[:3].decode('utf-8')
        valor = int(data[3:])
        if comando == "CaT":
            print("Moviendo ServoTilt")
            sc.setAngle(CamaraTilt, valor+90)
        if comando == "CaA":
            print("Moviendo ServoAz")
            sc.setAngle(CamaraAz, valor+90)
        if comando == "Mo1":
            print("Poniendo en marcha motor")
            mt.SetSpeed(1,valor)
        if comando == "Mo2":
            print("Poniendo en marcha motor")
            mt.SetSpeed(2,valor)
        if comando == "Mo3":
            print("Poniendo en marcha motor")
            mt.SetSpeed(3,valor)
        if comando == "Mo4":
            print("Poniendo en marcha motor")
            mt.SetSpeed(4,valor)
        if comando == "Mo5":
            print("Poniendo en marcha motor")
            mt.SetSpeed(5,valor)
        if comando == "Mo6":
            print("Poniendo en marcha motor")
            mt.SetSpeed(6,valor)
        if comando == "MoA":
            print("Poniendo en marcha todos los motores")
            for i in range(1,7):
                mt.SetSpeed(i,valor)
        if comando == "Tur":
            print("Reciviendo orden de giro")
            angS1, angS2, angS3, angS4, radGrio = angulos.CalcularServosGiro(valor)
            sc.setAngle(1, angS3)
            sleep(0.20)
            sc.setAngle(2, angS4)
            sleep(0.20)
            sc.setAngle(3, angS2)
            sleep(0.20)
            sc.setAngle(0, angS1)
            sleep(0.20)

        

        

        
try:
    listening_thread = threading.Thread(target=listeningThread, args=())
    listening_thread.start()
except KeyboardInterrupt:
    raise(Exception)
sc = ServoController(1)
mt = MotorController()
angulos = AngleCalculator(0.19,0.23)
CamaraTilt = 5
CamaraAz = 4
Servo1 = 1
Servo2 = 2
Servo3 = 3
Servo4 = 4
AAServos = [90,90,90,90] #Angulo Actual Servos

while True: sleep(0.5)
