'''
Calibrates sensor distance by running multiple measurements and choosing the
median of sorted values.

@author Lars Petter Ulvatne, Student at Linnaeus University.
'''
import pycom
import palette
import utime
import time

# Calibrate initial sensor distance to target.
def measure(sensor, temp, iter = 200):
    pycom.rgbled(palette.COLOUR_DARKYELLOW)
    sensor_name = sensor.name()
    print('Starting measurements on', sensor_name, '..')

    median_list = []
    counter = 0
    for i in range(iter):
        counter = counter + 1
        if sensor_name == 'HC_SR04':
            median_list.append(sensor.run_sensor(temp))
        elif sensor_name == 'VL53L0X':
            median_list.append(sensor.run_sensor())

    median_list.sort()

    distance = median_list[int(counter/2)]
    median_list.clear()

    return distance
