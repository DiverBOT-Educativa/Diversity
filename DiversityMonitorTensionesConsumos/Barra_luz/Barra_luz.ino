/*
 * Diversity.
 * 
 * https://github.com/DiverBOT-Educativa/Diversity
 * 
 * Placa monitorización consumos y tensiones.
 * Esta placa también será la encargada de activar y desactivar
 * los servos entre otros dispositivos.
 * 
 * La comunicación con la Jetson Nano se realizara mediante
 * el bus I2C. 
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

#include <arduino.h>
#include <Adafruit_NeoPixel.h>

#define VBatPin         A7
#define LedVBatPin      8

#define VServosPin      A6
#define LedVServosPin   9

#define IDcMotorsPin    A3
#define LedIDcMotorsPin 10

#define IDcBatPin       A2
#define LedIDcBatPin    11

#define IServosPin      A1
#define LedIServosPin   12

#define IJetsonNanoPin  A0
#define LedIJetsonNanoPin 13



class DisplayBar {
  public:
    DisplayBar(byte pinDin, byte pinAn, int valorMin, int valorMax, byte nPixel, unsigned int tPeakPersist);
    void Begin();
    void Dibujar();

  private:
    Adafruit_NeoPixel strip;
    byte _pinDin;
    byte _pinAn;
    int _valorMin;
    int _valorMax;
    byte _nPixel;
    unsigned int _tPeakPersist;
    unsigned long tiempoPico;
    int valorAnalogico;
    int valorPico;
    int valor;
    void DibujarPico();
    int MapValue(int value);
};

DisplayBar::DisplayBar(byte pinDin, byte pinAn, int valorMin, int valorMax, byte nPixel, unsigned int tPeakPersist) {
  _pinDin = pinDin;
  _pinAn = pinAn;
  _valorMin = valorMin;
  _valorMax = valorMax;
  _nPixel = nPixel;
  _tPeakPersist = tPeakPersist;
  tiempoPico = 0;
  valorPico = 0;
}
void DisplayBar::Begin() {
  strip = Adafruit_NeoPixel(_nPixel, _pinDin, NEO_GRB + NEO_KHZ800);
  strip.begin();
  strip.clear();
}
int DisplayBar::MapValue(int value) {
  return map(value, _valorMin, _valorMax, 0, _nPixel);
}
void DisplayBar::Dibujar() {
  valorAnalogico = analogRead(_pinAn);
  valor = MapValue(valorAnalogico);
  strip.clear();
  for (int i = 0; i < valor; i++) {
    strip.setPixelColor(i, strip.Color(100, 0, 0));
  }
  DibujarPico();
  strip.show();
}
void DisplayBar::DibujarPico() {
  if (tiempoPico < millis()) {
    valorPico --;
    tiempoPico = tiempoPico + 250;
  }
  if (valor > valorPico) {
    valorPico = valor;
    tiempoPico = millis() + _tPeakPersist;
  }
  valorPico = constrain(valorPico, 0, _nPixel - 1);
  strip.setPixelColor(valorPico, strip.Color(0, 100, 0));
}

/*Aqui empieza nuestro programa*/

DisplayBar displayVBat(LedVBatPin, VBatPin, 441, 515, 16, 1000);
DisplayBar displayVServos(LedVServosPin, VServosPin, 920, 1023, 8, 1000);
DisplayBar displayIdcMotors(LedIDcMotorsPin, IDcMotorsPin,512,600,8,500);
DisplayBar displayIDcBat(LedIDcBatPin, IDcBatPin,512,600,8,500);
DisplayBar displayIServos(LedIServosPin, IServosPin,512,600,8,500);
DisplayBar displayIJetsonNano(LedIJetsonNanoPin, IJetsonNanoPin,512,600,8,500);

void setup() {
  Serial.begin(9600);
  Serial.println("Programa iniciado");

  displayVBat.Begin();
  displayVServos.Begin();
  displayIdcMotors.Begin();
  displayIDcBat.Begin();
  displayIServos.Begin();
  displayIJetsonNano.Begin();
  
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  for(int i = 0; i < 4; i++){
    digitalWrite(6, LOW);
    delay(500);
    digitalWrite(6,HIGH);
    delay(500);
  }
  
}

void loop() {
  displayVBat.Dibujar();
  displayVServos.Dibujar();
  displayIdcMotors.Dibujar();
  displayIDcBat.Dibujar();
  displayIServos.Dibujar();
  displayIJetsonNano.Dibujar();
  Serial.println(analogRead(IDcMotorsPin));
}

/* Como guardar un color en un uint32

  uint32_t Adafruit_NeoPixel::Color(uint8_t r, uint8_t g, uint8_t b) {
  return ((uint32_t)r << 16) | ((uint32_t)g <<  8) | b;
  }

*/
