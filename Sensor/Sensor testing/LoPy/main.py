# -*- coding: utf-8 -*-
import pycom
import time
import machine
import lib.lopy as LoPy
import lib.palette as palette
import lib.sensor_measurements as measurements
from machine import Pin
from deepsleep import DeepSleep

# Sensor scripts
import lib.HC_SR04 as HC_SR04
# import lib.VL53L0X as VL53L0X
# import lib.MCP9700A as temp
import lib.RHT03 as RHT03


COLOUR_BLACK = 0x000000
COLOUR_GREEN = 0x00FF00
COLOUR_BLUE  = 0x0000FF
pycom.heartbeat(False)              # disable the blue blinking
ds = DeepSleep()

'''
Sensor names:
VL53L0X - Time of flight sensor (LIDAR)
HC_SR04  - Ultrasonic sensor
'''
sensor = HC_SR04
iter = 30

def humid_temp():
    try:
        return RHT03.run_sensor()
    except Exception as err:
        return ('Checksum error', 'Checksum error')

calibrated_distance = measurements.measure(sensor, humid_temp()[1], iter)
print(calibrated_distance, ': Calibrated')
time.sleep(2)

while(True):
    try:
        humid, temp = humid_temp()
        print('Humidity: ', humid, '%')
        print('Temperature: ', temp, '°C')

        time.sleep(2)

        distance = measurements.measure(sensor, temp, 10)
        print('Distance: ', distance)
        depth = calibrated_distance - distance

        if(depth < 0.3):
            if(depth < - 0.5):
                # Recalibrating if distance is 0.2 below the 3mm buffer.
                print('Recalibrating..')
                calibrated_distance = measurements.measure(sensor, temp, iter)
            depth = 0

        print('Depth: ', depth)

        print('Send humid, temp, depth with LoRa.')

        # Wait to catch data.
        time.sleep(10)
    except Exception as err:
        console.log(err)
