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

i2c = I2C
device = i2c.get_i2c_device(0x41,busnum=1)

device.write8(0x01,100)
device.write8(0x11,1)
sleep(0.5)
device.write8(0x11,0)
sleep(0.5)
device.write8(0x11,2)
sleep(0.5)
device.write8(0x11,0)
