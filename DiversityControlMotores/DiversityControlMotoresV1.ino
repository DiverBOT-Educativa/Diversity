/*
 * Diversity.
 * 
 * https://github.com/DiverBOT-Educativa/Diversity
 * 
 * Placa de control motores traccion ruedas.
 * 
 *    Dirección I2C 0x01
 * Comandos Descripcion     Valor1    Valor2
 *    0x00  Mod PWM M1      0-255
 *    0x01  Mod PWM M2      0-255
 *    ...
 *    0x05  Mod PWM M6      0-255
 *
 *    0x10  Mod Dir M1      0-parar, 1-avanzar, 2-retroceder
 *    0x11  Mod Dir M2      0-parar, 1-avanzar, 2-retroceder
 *    ...
 *    0x05  Mod Dir M6      0-parar, 1-avanzar, 2-retroceder
 * 
 * 
 * 
 * Introducción:
 *    Diversity es nuestro Curiosity particular. Básicamente
 *    es un robot con capacidad para transportarse, gracias
 *    a sus seis ruedas con tracción. Cuatro de ellas, además,
 *    tiene la capacidad de rotar sobre su eje vertical, lo que
 *    le permite no solo realizar trayectorias curvas, sino que 
 *    Diversity es capaz de rotar sobre si mismo, sin necesidad
 *    de desplazarse.
 *    
 *    El proyecto es original de:
 *    https://bricolabs.cc/wiki/proyectos/curiosity_btl 
 *    
 *    Nuestra dirección en github:
 *    https://github.com/DiverBOT-Educativa/Diversity
 *    
 *    
 *    Aquí unos repositorios que se citaban en el proyecto
 *    original de bricolabs.cc :
 *    https://github.com/felixstdp/curiosity_btl
 *    https://www.thingiverse.com/thing:2414954
 *    https://www.thingiverse.com/thing:3556381
 *    https://github.com/javacasm/curiosity_btl
 *    
 * 
 *    
 */

#include <Wire.h>
#define M1PWM 11    //Delantero izquierdo          
#define M1DIR1 13
#define M1DIR2 12
#define M2PWM 10    //Delantero derecho
#define M2DIR1 7
#define M2DIR2 8
#define M3PWM 9     //Central izquierdo
#define M3DIR1 2
#define M3DIR2 4
#define M4PWM 6     //Central derecho
#define M4DIR1 0
#define M4DIR2 1
#define M5PWM 5     //Trasero izquierdo
#define M5DIR1 14
#define M5DIR2 15
#define M6PWM 3     //Trasero derecho
#define M6DIR1 17
#define M6DIR2 16
//PWM contiene los pines del EN de los motores
byte PWM[] = {M1PWM, M2PWM, M3PWM, M4PWM, M5PWM, M6PWM};

//Dir contiene los pines de dirección y si hay que invertir el sentido de giro.
byte Dir[6][3] = {        // (MxDIR1,MxDIR2,inversionMotor)
  {M1DIR1, M1DIR2, 0},    //Delantero izquierdo
  {M2DIR1, M2DIR2, 0},    //Delantero derecho
  {M3DIR1, M3DIR2, 0},    //Central izquierdo
  {M4DIR1, M4DIR2, 0},    //Central derecho
  {M5DIR1, M5DIR2, 0},    //Trasero izquierdo
  {M6DIR1, M6DIR2, 0}     //Trasero derecho
};

unsigned long UltimoUsoI2C = millis();

//JetsonNanoOff se usará para saber si ha habido algún tipo de comunicación
//  por I2C, indicando si está resente la JetsonNano.
bool JetsonNanoOff = true;

void setup() {
  //Inicializamos los pines como salidas
  for (int i = 0; i<6; i++){
    pinMode(PWM[i], OUTPUT);
    for (int j = 0; j<=1; j++){
      pinMode(Dir[i][j],OUTPUT);
    }
  }  
  InicioVisualMotores();
  delay(500);
  //Inicializamos el I2C
  Wire.begin(0x41);
  Wire.onReceive(receiveEvent);
}

void loop() {
  if (millis() - UltimoUsoI2C > 60000){
    UltimoUsoI2C = millis();
    if (JetsonNanoOff) InicioVisualMotores();
  }
  delay(1000);
}

void receiveEvent (int howMany) {
  byte comando = Wire.read();
  byte comandoOpcion = comando >> 4;
  byte Motor = comando & 0x0F;
  byte valor = Wire.read();

  if (comandoOpcion == 0) {         //Comando para ajustar PWM
    PotenciaMotor(Motor, valor);
  } else if (comandoOpcion == 1) {  //Comando para ajustar Sentido Giro
    DireccionMotor(Motor, valor);
  }
  JetsonNanoOff = false;            //I2C funcionando, lo indicamos en JetsonNanoOff
}

void DireccionMotor(byte motor, byte opcion) {
  switch (opcion) {
    case 0:   //PARAR MOTORES
      digitalWrite(Dir[motor][0], 1);
      digitalWrite(Dir[motor][1], 1);
      break;
    case 1:   //AVANZAR
      digitalWrite(Dir[motor][0], 0 ^ Dir[motor][2]);
      digitalWrite(Dir[motor][1], 1 ^ Dir[motor][2]);
      break;
    case 2:   //RETROCEDER
      digitalWrite(Dir[motor][0], 1 ^ Dir[motor][2]);
      digitalWrite(Dir[motor][1], 0 ^ Dir[motor][2]);
      break;
  }
}
void PotenciaMotor(byte motor, byte potencia){
  analogWrite(PWM[motor], potencia);
}

void InicioVisualMotores(){
  for (byte i = 0; i < 6; i++){
    DireccionMotor(i,1);
    PotenciaMotor(i,100);
    delay(500);
    PotenciaMotor(i,0);
    delay(200);
    DireccionMotor(i,2);
    PotenciaMotor(i,100);
    delay(500);
    PotenciaMotor(i,0);
    DireccionMotor(i,0);
    delay(200);    
  }
}
