# -*- coding: utf-8 -*-
'''
This main script will measure temperature and relative humdity with RHT03 sensor
while not in demo mode. To measure depth from calibrated distance either HC_SR04
or VL53L0X will be used. Uncomment the right library to use the sensor, and
change to the wanted sensor name further down.

The data will then be sent through LoRaWAN, when reaching depths over threshold
value.

@author Lars Petter Ulvatne, Linnaeus University.
'''
import pycom
import time
import machine
import lib.lopy as LoPy
import lib.palette as palette
import lib.sensor_measurements as measurements
import lib.keys as keys
import lib.counter as cnt
from machine import Pin
from deepsleep import DeepSleep

# Sensor scripts
import lib.HC_SR04 as HC_SR04
# import lib.VL53L0X as VL53L0X
import lib.RHT03 as RHT03

pitch_id = 38                       # ID for Fagrabaeckkonstgraesplan
COLOUR_BLACK = 0x000000
COLOUR_GREEN = 0x00FF00
COLOUR_BLUE  = 0x0000FF
pycom.heartbeat(False)              # disable the blue blinking

'''
Sensor names:
VL53L0X - Time of flight sensor (LIDAR)
HC_SR04  - Ultrasonic sensor
'''
sensor = HC_SR04
iter = 20
counter = 1

# Predefined values for testing
temp = -0.1
humid = 80.1
snow_depth = 3.2
demo = True

def humid_temp():
    try:
        return RHT03.run_sensor()
    except Exception as err:
        return ('Checksum error', 'Checksum error')

# Calibrate sensor
humid, temp = humid_temp()
calibrated_distance = measurements.measure(sensor, temp, iter)
print(calibrated_distance, ': Calibrated')
time.sleep(2)

while(True):
    try:
        time.sleep(0.25)

        if(LoPy.joined()):
            # Measure humidity and temperature with RHT03
            if(not demo):
                humid, temp = humid_temp()
                print('Humidity: ', humid, '%')
                print('Temperature: ', temp, '°C')

            print('Reading depth...')
            pycom.rgbled(palette.COLOUR_DARKGREEN)

            distance = measurements.measure(sensor, temp, iter)
            snow_depth = calibrated_distance - distance

            ack_id = cnt.count(counter)

            if(snow_depth > 2):
                message = '{0},{1},{2},{3},{4}'.format(temp, humid, snow_depth, pitch_id, ack_id)
                LoPy.sendrecv(message)
                counter = counter + 1
                if(counter == 100):
                    counter = 1
                time.sleep(60)

            print('Going into deep sleep..')
            machine.deepsleep(10000)
        else:
            print('Connecting to gateway..')
            LoPy.connect_lora()
    except Exception as err:
        print(err)
