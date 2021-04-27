"""
 *    Direccion I2C 0x41
 * Comandos Descripcion     Valor1    Valor2
 *    0x01  Mod PWM M1      0-255
 *    0x02  Mod PWM M2      0-255
 *    ...
 *    0x06  Mod PWM M6      0-255
 *
 *    0x11  Mod Dir M1      0-parar, 1-avanzar, 2-retroceder
 *    0x12  Mod Dir M2      0-parar, 1-avanzar, 2-retroceder
 *    ...
 *    0x06  Mod Dir M6      0-parar, 1-avanzar, 2-retroceder
 * 
"""
import Adafruit_GPIO.I2C as I2C 
from time import sleep


class MotorController():
    def __init__(self):
        self.i2c = I2C
        self.device = self.i2c.get_i2c_device(0x41,busnum=1)
        self.ComandoDireccion = ["nada",0x10,0x11,0x12,0x13,0x14,0x15]
        self.ComandoVelocidad = ["nada",0x00,0x01,0x02,0x03,0x04,0x05]

    def SetSpeed(self, motor, speed):
        if speed < 0 :
            self.device.write8(self.ComandoDireccion[motor], 2)
            speed = -1 * speed
        elif speed > 0:
            self.device.write8(self.ComandoDireccion[motor], 1)
        else:
            self.device.write8(self.ComandoDireccion[motor], 0)
        self.device.write8(self.ComandoVelocidad[motor], int(speed*255/100))

if (__name__ == "__main__"):
	quit()