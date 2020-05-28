'''
Measures distance by running the run_sensor() function, which takes trigger,
echo and analog_pin as input parameters. calibrate() function can be run upon
distance difference measurements. This will run for several iterations, picking
the median value as the calibrated value. A temperature sensor has to be
installed for more precise measurements in different temperatures, as the speed
of sound changes with temperature. To make code run on other devices than pycom,
remove the LED coding.

@author Lars Petter Ulvatne, Student at Linnaeus University.
'''
import utime
import time
import pycom
import palette
# import lib.MCP9700A as temp   # Temperature sensor
# import lib.RHT03 as RHT         # Humidity and temperature sensor
from machine import Pin
from machine import ADC

SENSOR_NAME = 'HC_SR04'

# Trigger and echo pin configurations.
trigger = Pin('P19', mode=Pin.OUT)
echo = Pin('P20', mode=Pin.IN)

def name():
    return 'HC_SR04'

def run_sensor(temp):
    # Make sure output is low
    trigger.value(0)
    utime.sleep_us(10)

    # Trigger 8 cycle sonic burst by setting trigger to high for 10us
    trigger.value(1)
    utime.sleep_us(10)
    trigger.value(0)

    # Wait for pulse to start on input pin.
    while echo() == 0:
        pass
    start = utime.ticks_us()

    # Run until input pin changes to low.
    while echo() == 1:
        pass
    finish = utime.ticks_us()

    utime.sleep_ms(10)

    # MCP9700A temperature sensor
    # T_A = temp.readTemp(analog_pin)

    if(isinstance(temp, str) == False):
        speed_sound = (331.4 + 0.6 * temp) * 0.0001        # cm/us
    else:
        speed_sound = (331.4 + 0.6 * 14.5) * 0.0001        # cm/us
    # Calculate and print out distance measured.
    return ((utime.ticks_diff(finish, start)) * speed_sound)/2
