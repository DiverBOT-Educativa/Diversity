"""
def calc_angle(AB, BC):
    from math import atan2, degrees

    return round(degrees(atan2(AB, BC)),1)


DAncho=3
DVertical=5
RadioGiro = int(input("Radio de giro deseado: "))
RuedaInterior = 90 + calc_angle(5, RadioGiro - DAncho)
RuedaExterior = 90 + calc_angle(5, RadioGiro + DAncho*2)
print("Angulo rueda interior: {}º , Angulo rueda exterior: {}º".format(RuedaInterior,RuedaExterior))
"""


class AngleCalculator:

    def __init__(self, DAncho, DVertical):
        self.DAncho = DAncho        #ancho separacion de ruedas en metros
        self.DVertical = DVertical  #separacion entre ruedas delanteras y traseras en metros

    def calc_angle(self, AB, BC):
        from math import atan2, degrees
        return round(degrees(atan2(AB, BC)),1)

    def IntCalc(self, RadioGiro):
        return 90 + self.calc_angle(self.DVertical,RadioGiro - self.DAncho)

    def ExtCalc(self, RadioGiro):
        return 90 + self.calc_angle(self.DVertical,RadioGiro + 2 * self.DAncho)

    def map(self, value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def CalcularServosGiro(self,giro):
        """
        Calcula la posicion de los servos para hacer un giro

        :param giro: el giro que queremos realizar, de -30(izquierda) a 30(derecha)
        :return: lista [servo1, servo2, servo3, servo4, radioDeGiro]
        """
        izquierda = False
        if (giro == 0): return [90,90,90,90,10000000]
        if (giro > 30): giro = 30
        if (giro < -30): giro = -30
        if (giro < 0):
            giro = giro * (-1)
            izquierda = True
        radioSeleccionado = self.map(giro, 1,30,4,0.4)
        if izquierda == False :
            servo1 = self.ExtCalc(radioSeleccionado)
            servo2 = self.IntCalc(radioSeleccionado)
            servo3 = 90 -(servo1 - 90)
            servo4 = 90 -(servo2 - 90)
        else :
            servo1 = 180 - self.IntCalc(radioSeleccionado)
            servo2 = 180 - self.ExtCalc(radioSeleccionado)
            servo3 = 180 - servo1
            servo4 = 180 - servo2          
        return [servo1, servo2, servo3, servo4, radioSeleccionado]
        

if __name__ == "__main__" :

    A = AngleCalculator(0.19,0.23)
    while True:
        print(A.CalcularServosGiro(int(input("Radio de giro: "))))
    

