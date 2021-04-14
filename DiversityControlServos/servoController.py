from time import sleep
import Adafruit_PCA9685

VelocidadGiro = 0.05
PosicionServoAD = 0
PosicionIr = 180

class ServoController():

	def __init__(self, busnum=1):
		self.pwm = Adafruit_PCA9685.PCA9685(busnum=busnum)
		self.pwm.set_pwm_freq(60)

		self.minValues = [100, 140, 125, 125, 160, 130]
		self.maxValues = [575, 610, 590, 590, 530, 420]


	def setAngle(self, servo, angle):
		if (angle < 0): angle = 0
		if (angle > 180): angle = 180
		minValue = self.minValues[servo]
		maxValue = self.maxValues[servo]

		pulse = (angle - 0) * (maxValue - minValue) / (180 - 0) + minValue
		self.pwm.set_pwm(servo, 0, int(pulse))

if (__name__ == "__main__"):
	sc = ServoController(1)
	sc.setAngle(1, PosicionServoAD)

	sc.setAngle(1, 0)
	sc.setAngle(1, 90)

























