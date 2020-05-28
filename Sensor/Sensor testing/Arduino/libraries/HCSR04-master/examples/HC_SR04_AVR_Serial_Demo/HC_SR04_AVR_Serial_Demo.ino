/***************************************************************************************************/
/*
  This is an Arduino sketch for HC-SR04, HC-SRF05, DYP-ME007, BLJ-ME007Y ultrasonic ranging sensor

  Operating voltage:    5v
  Operating current:    10..20mA
  Working range:        4cm..250cm
  Measuring angle:      15°
  Operating frequency:  40kHz
  Resolution:           0.3cm
  Maximum polling rate: 20Hz

  written by : enjoyneering79
  sourse code: https://github.com/enjoyneering/


  Frameworks & Libraries:
  ATtiny Core           - https://github.com/SpenceKonde/ATTinyCore
  ESP32 Core            - https://github.com/espressif/arduino-esp32
  ESP8266 Core          - https://github.com/esp8266/Arduino
  ESP8266 I2C lib fixed - https://github.com/enjoyneering/ESP8266-I2C-Driver
  STM32 Core            - https://github.com/rogerclarkmelbourne/Arduino_STM32

  GNU GPL license, all text above must be included in any redistribution, see link below for details:
  - https://www.gnu.org/licenses/licenses.html
*/
/***************************************************************************************************/
#include <HCSR04.h>

float distance = 0;

/*
HCSR04(trigger, echo, temperature, distance)

trigger     - trigger pin
echo        - echo pin
temperature - ambient temperature, in C
distance    - maximun measuring distance, in cm
*/
HCSR04 ultrasonicSensor(9, 8, 20, 300);

void setup()
{
  Serial.begin(115200);

  ultrasonicSensor.begin(); //set trigger as output & echo pin as input
}

void loop()
{
  distance = ultrasonicSensor.getDistance();

  if (distance != HCSR04_OUT_OF_RANGE)
  {
    Serial.print(distance, 1);
    Serial.println(F(" cm"));                            //(F()) saves string to flash & keeps dynamic memory free
  }
  else
  {
    Serial.println(F("out of range"));
  }
  delay(50);                                             //wait 50msec or more, until echo from previous measurement disappears


  distance = ultrasonicSensor.getMedianFilterDistance(); //pass 3 measurements through median filter, better result on moving obstacles

  if (distance != HCSR04_OUT_OF_RANGE)
  {
    Serial.print(distance, 1);
    Serial.println(F(" cm, filtered"));
  }
  else
  {
    Serial.println(F("out of range, filtered"));
  }

  ultrasonicSensor.setTemperature(18.5);                 //set air temperature to compensate change in speed of sound

  delay(250);                                            //serial refresh rate
}
