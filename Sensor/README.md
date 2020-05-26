# IoT device implementations
The task provided for using the IoT devices, was to measure snow depth and send the data over LoRa to the application server. The sensors used in this project was the HC-SR04 ultrasonic sensor, VL53L0X micro LIDAR sensor, GP2Y0A21YK0F IR sensor and RHT03 relative humidity and temperature sensor. All sensors were used with an Arduino Uno and all, but the IR sensor, were also used with a Pycom LoPy4, mounted onto an expansion shield. 

## LoRaWAN
The data transfer method was LoRa and was only setup to the LoPy4 device, to send data to the application server. This was done through [The Things Network](https://www.thethingsnetwork.org/). The decoding function for parsing data before pushing to the server, can be found in the [The Things Network folder](/The%20Things%20Network).

## HC-SR04
The pin connections to both microcontrollers can be viewed in the image below.

![Pin connections to the LoPy4 and Arduino Uno. Fritzing images are under CC-BY-SA license.](/Sensor/img/hc_sr04.jpg)