// Función cambiar colores
// Función aplique colores

#include <Adafruit_NeoPixel.h>


#define LED_PIN 8
#define LED_COUNT 16
#define LED_COUNT_LITTLE 8



Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);


void bar(int endPoint, uint32_t color) {
  strip.clear();
  for (int i = 0; i < endPoint; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
}

void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}


void measureSensor(int analog_pin, int sensor_bar_pin){
  Adafruit_NeoPixel sensor_bar(LED_COUNT_LITTLE, sensor_bar_pin, NEO_GRB + NEO_KHZ800);
  int r = map(analogRead(A7), 511, 1023, 0, LED_COUNT_LITTLE);
  uint32_t color;
  
  if (r < 6) {
    color = strip.Color(255, 0, 0);
    
  }
  else if (r < 12) {
    color = strip.Color(100, 100, 0);
  }
  else {
    color =(r, strip.Color(0, 100, 0);
  }

  strip.clear();
  for (int i = 0; i < endPoint; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
  
}

/*
 Analog   Input
  1023 ->  25
    x  ->  tutension

 Max: 
 */
void batterySensor(){
  int r = map(analogRead(A7), 441, 500, 0, LED_COUNT);
  if (r < 6) {
    bar(r, strip.Color(255, 0, 0));
    
  }
  else if (r < 12) {
    bar(r, strip.Color(100, 100, 0));
  }
  else {
    bar(r, strip.Color(0, 100, 0));
  }
}

/*
 A7 -> Tensión batería
 A6 -> Tensión servos
 A3 -> Corriente motores DC
 A2 -> Corriente general/batería
 A1 -> Consumo servos
 A0 -> Jetson Nano
*/

void loop() {
  batterySensor();
  measureSensor(A0, 9);

}
