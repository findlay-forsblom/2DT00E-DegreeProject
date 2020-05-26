# IoT device implementations
The task provided for using the IoT devices, was to measure snow depth and send data over LoRa to the application server. The sensors used in this project was the HC-SR04 ultrasonic sensor, VL53L0X micro LIDAR sensor, GP2Y0A21YK0F IR sensor and RHT03 relative humidity and temperature sensor. All sensors were used with an Arduino Uno and all, but the IR sensor, were also used with a Pycom LoPy4, mounted onto an expansion shield. 

## LoRaWAN
The data transfer method was LoRa and was only setup to the LoPy4 device, to send data to the application server. This was done through [The Things Network](https://www.thethingsnetwork.org/). The decoding function for parsing data before pushing to the server, can be found in the [The Things Network folder](/Sensor/The%20Things%20Network).

## HC-SR04 ultrasonic sensor
The [Arduino Uno code](/Sensor/Sensor%20testing/Arduino) and [LoPy4 code](/Sensor/Sensor%20testing/LoPy/lib) can be found in the separate maps in Sensor testing. Link to [HC-SR04 datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf). The Arduino library for this sensor was provided by the Github account of [enjoyengineering79](https://github.com/enjoyneering/). The pin connections to both microcontrollers can be viewed in the image below.

![Pin connections to the LoPy4 and Arduino Uno. Fritzing images are under CC-BY-SA license.](/img/hc_sr04.jpg)
<br>
Pin connections to the LoPy4 and Arduino Uno. Fritzing images are under CC-BY-SA license.

## VL53L0X micro LIDAR sensor
The [Arduino Uno code](/Sensor/Sensor%20testing/Arduino) and [LoPy4 code](/Sensor/Sensor%20testing/LoPy/lib) can be found in the separate maps in Sensor testing. Link to [VL53L0X datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout.pdf). The Arduino library for this sensor was provided by [Limor Fried and Ladyaya](https://github.com/adafruit/Adafruit_VL53L0X). The LoPy4 library was inspired by a forum thread at pycom.io, from the user [IoTMaker](https://forum.pycom.io/topic/1453/i2c-sensor-with-wipy2/20). The pin connections to both microcontrollers can be viewed in the image below.

![Pin connections to the LoPy4 and Arduino Uno. Fritzing images are under CC-BY-SA license.](/img/vl53l0x.jpg)
<br>
Pin connections to the LoPy4 and Arduino Uno. Fritzing images are under CC-BY-SA license.

## GP2Y0A21YK0F IR sensor
The [Arduino Uno code](/Sensor/Sensor%20testing/Arduino) and [LoPy4 code](/Sensor/Sensor%20testing/LoPy/lib) can be found in the separate maps in Sensor testing. Link to [GP2Y0A21YK0F datasheet](https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y0a21yk_e.pdf). The Arduino library for this sensor was provided by [Benne de Bakker](https://www.makerguides.com/sharp-gp2y0a21yk0f-ir-distance-sensor-arduino-tutorial/) in the step-by-step tutorial for this sensor. This sensor was not used with the LoPy4 device. The pin connections for the Arduino can be viewed in the image below. A 10 µF capacitor was connected between 5V and GND for stabilization. 

![Pin connections to the Arduino Uno. Fritzing images are under CC-BY-SA license.](/img/GP2Y0A21YK0F.jpg)
<br>
Pin connections to the Arduino Uno. Fritzing images are under CC-BY-SA license.

## RHT03 relative humidity and temperature sensor
The [Arduino Uno code](/Sensor/Sensor%20testing/Arduino) and [LoPy4 code](/Sensor/Sensor%20testing/LoPy/lib) can be found in the separate maps in Sensor testing. Link to [RHT03 datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Weather/RHT03.pdf). The Arduino library for this sensor was provided by Sparkfun Electronics at the Github repository [SparkFun_RHT03_Arduino_Library](https://github.com/sparkfun/SparkFun_RHT03_Arduino_Library/). The LoPy4 library was written by the information provided in the datasheet. The pin connections to both microcontrollers can be viewed in the image below.

![Pin connections to the LoPy4 and Arduino Uno. Fritzing images are under CC-BY-SA license.](/img/RHT03.jpg)
<br>
Pin connections to the LoPy4 and Arduino Uno. Fritzing images are under CC-BY-SA license.

## Microcontrollers
The microcontrollers used in this project was Pycom LoPy4, mounted onto a Expansion Shield 3.0, and an Arduino Uno. The LoRa antenna was used when sending data through LoRaWAN, using the LoPy4 device. The microcontrollers can be viewed in the image below.

![From the left: LoRa antenna, Pycom LoPy4 and Arduino Uno.](/img/microcontrollers.jpg)
<br>
From the left: LoRa antenna, Pycom LoPy4 and Arduino Uno.