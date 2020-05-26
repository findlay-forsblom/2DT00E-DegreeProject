'''
Configures and measures distance with the Adafruid VL53L0X ToF sensor.
config() function will configure the measurement initiations and timings.
run_sensor() function will start measuring the distance to target.

LoPy4 pins:
SCL => Pin 10
SDA => Pin 9
'''
from machine import UART
from time import sleep_ms
from machine import I2C
import pycom
import binascii
import ubinascii
from machine import Pin
import ustruct
import time
import lib.palette as palette

VL53L0X_REG_IDENTIFICATION_MODEL_ID = 0xc0
VL53L0X_REG_IDENTIFICATION_REVISION_ID = 0xc2
VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD = 0x50
VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD = 0x70
VL53L0X_REG_SYSRANGE_START = 0x00
VL53L0X_REG_RESULT_INTERRUPT_STATUS = 0x13
VL53L0X_REG_RESULT_RANGE_STATUS = 0x14
sensor = 0x29       #I2C Address

pycom.heartbeat(False)
##RGB Colors
red = 0xff0000
yellow = 0xffff00
green = 0x00ff00
blue = 0x0000ff
cyan = 0x00feff
purple = 0xc442a1
orange = 0xff8b55
dark = 0x000000

def name():
    return 'VL53L0X'

def ledtoggle(color):
    pycom.rgbled(color)
    sleep_ms(50)
    pycom.rgbled(dark)
    sleep_ms(50)

def i2c_w(reg, val):
    i2c.writeto_mem(sensor, reg, bytes([val])) #Put device on standby mode
    sleep_ms(1)

## address 0x1D
i2c = I2C(0)                          # Create on bus 0
i2c = I2C(0, I2C.MASTER)                # Create on bus 0 and init as master
i2c.init(I2C.MASTER, baudrate=400000)   # Init at baudrate 400k
sleep_ms(30)

print("I2C Scan for devices")
print(i2c.scan())
print("Revision ID ")
print(i2c.readfrom_mem(sensor, VL53L0X_REG_IDENTIFICATION_REVISION_ID, 1))
print("")
print("Device ID ")
print(i2c.readfrom_mem(sensor, VL53L0X_REG_IDENTIFICATION_MODEL_ID, 1))
print("")
print("Pre Range config Period")
print(i2c.readfrom_mem(sensor, VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD, 1))
print("")
print("Final  Period")
print(i2c.readfrom_mem(sensor, VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD, 1))
sleep_ms(30)
print("")

def run_sensor():
    counter = 0
    value = 0

    i2c_w(VL53L0X_REG_SYSRANGE_START, 0x02)

    while (counter < 100):
        # 1 second waiting time max
        value = i2c.readfrom_mem(sensor, VL53L0X_REG_RESULT_RANGE_STATUS, 1)

        if value == 64:
            counter = 200
        counter = counter + 1

    sleep_ms(30)

    datasensor = i2c.readfrom_mem(sensor, 0x14, 12)         # Read sensor data
    distance = (datasensor[10]*256 + datasensor[11])/10     # Convert to cm
    ledtoggle(palette.COLOUR_DARKGREEN)
    return distance
