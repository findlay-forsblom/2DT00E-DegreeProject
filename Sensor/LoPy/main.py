# -*- coding: utf-8 -*-
import pycom
import time
import machine
import lib.lopy as LoPy
import lib.palette as palette
import lib.sensor_measurements as measurements
from machine import Pin

# Sensor scripts
import lib.HC_SR04 as HC_SR04
import lib.VL53L0X as VL53L0X
# import lib.MCP9700A as temp
import lib.RHT03 as RHT03


COLOUR_BLACK = 0x000000
COLOUR_GREEN = 0x00FF00
COLOUR_BLUE  = 0x0000FF
pycom.heartbeat(False)              # disable the blue blinking

'''
Sensor names:
VL53L0X - Time of flight sensor (LIDAR)
HCSR04  - Ultrasonic sensor
'''
sensor = VL53L0X
iter = 50

def humid_temp():
    try:
        return RHT03.run_sensor()
    except Exception as err:
        print('Error:', err)

calibrated_distance = measurements.measure(sensor, humid_temp()[1], iter)
print(calibrated_distance, ': Calibrated')

while(True):
    humid, temp = humid_temp()
    print('Humidity: ', humid, '%')
    print('Temperature: ', temp, '°C')

    time.sleep(2)

    distance = measurements.measure(sensor, temp, 10)
    print('Distance: ', distance)
    depth = calibrated_distance - distance
    print('Depth: ', depth)

    print('Send humid, temp, depth with LoRa.')


# # Set pin input/output for ultrasonic sensor.
# trigger = Pin('P19', mode=Pin.OUT)
# echo = Pin('P20', mode=Pin.IN )
#
# # Set pin input for temperature sensor.
# adc = machine.ADC(0, bits=10)                 # create an ADC object

# '''
# Here's what needed for running the RHT03 sensor.
# '''
# import RHT03
# pin = Pin('P21', mode=Pin.OPEN_DRAIN)
# data = RHT03.run_sensor(pin)
# print('humidiy: ', data[0], '%')
# print('temperature: ', data[1], '°C')


#
# distance = sensor.calibrate(trigger, echo, analog_pin)

# try:
    # while(True):
    #     time.sleep(0.25)
    #
    #     # print(apin())
    #     arr = []
    #     for i in range(50):
    #         time.sleep(0.01)
    #         arr.append(analog_pin.value())
    #     print(arr)
    #     arr.sort()
    #     print(arr)
        # v = (voltz*5)/1063
        # dist = 16.2537 * v**4 - 129.893 * v**3 + 382.268 * v**2 - 512.611 * v + 301.439
        # print(dist, ' cm', v)
        # Run program until interruption
        # if(LoPy.joined()):
        #     pycom.rgbled(palette.COLOUR_DARKGREEN)
        #

            # LoPy.sendrecv('14.3,22.2,2.1')

            # # print('Sensor value: ', value, distance)
            # if(value < distance - 10):
            #     print('Found motion. Sensor value: ', value)
            #     while(LoPy.sendrecv()):
            #         print('No ack recevied.. Resending.')
            # else:
            #     time.sleep(0.1)
        # else:
        #     print('Connecting to gateway..')
        #     LoPy.connect_lora()
# except Exception as e:
#     print(e)
# finally:
#     print('STOPPED.')

# import socket
# import ubinascii
# import sys
# import machine
# import utime
# import lib.palette as palette
# from network import LoRa

# Led colors
# COLOUR_DARKYELLOW = 0x0F0F00    # Calibrating
# COLOUR_DARKRED = 0x0F0000       # No connection
# COLOUR_DARKGREEN = 0x000F00     # Connected & Reading sensor values
# COLOUR_DARKBLUE = 0x000F0F      # Checking for ack's
# COLOUR_WHITE = 0xF0F0F0         # Ack received.
# COLOUR_RED   = 0xFF0000         # No ack received.


# # Initialise LoRa in LORAWAN mode.
# # Please pick the region that matches where you are using the device:
# # Asia = LoRa.AS923
# # Australia = LoRa.AU915
# # Europe = LoRa.EU868
# # United States = LoRa.US915
# lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, adr=True)
# pycom.heartbeat(False) # disable the blue blinking
#
# # create an OTAA authentication parameters
# app_eui = ubinascii.unhexlify('70B3D57ED002AC52')
# app_key = ubinascii.unhexlify('F8D72FFC421E7FD0ABEAC11DC2AD69B0')
#
# # Sensor input pin
# # pin = Pin('P23', mode=Pin.IN)
#
# # adc = machine.ADC()             # create an ADC object
# # apin = adc.channel(pin='P16')   # create an analog pin on P16
# # p_in = Pin('P17', mode=Pin.IN)
# # val = apin()                    # read an analog value

# # Connect to LoRa gateway through OTAA
# def connect_lora():
#     pycom.rgbled(palette.COLOUR_DARKRED)
#     # join a network using OTAA (Over the Air Activation)
#     lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)
#
#     connector = 0
#     # wait until the module has joined the network
#     while not lora.has_joined():
#         time.sleep(2)
#         print('Waiting for connection..')
#         connector = connector + 1
#         if(connector > 10):
#             machine.reset()
#
#     print('Connected to gateway.')
#     pycom.rgbled(palette.COLOUR_DARKGREEN)
#
#     # create a LoRa socket and make object global for other functions.
#     global s
#     s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
#
#     # set the LoRaWAN data rate
#     s.setsockopt(socket.SOL_LORA, socket.SO_DR, 1)

# # Send a message over LoRa.
# def send_msg(byteEncoded):
#     # make the socket blocking
#     # (waits for the data to be sent and for the 2 receive windows to expire)
#     s.setblocking(True)
#     s.send(byteEncoded)
#     print('Sent bytes: ', byteEncoded)

# # Receive messages from LoRa gateway
# def recv_msg():
#     # make the socket non-blocking
#     # (because if there's no data received it will block forever...)
#     s.setblocking(False)
#
#     # get any data received (if any...)
#     data = s.recv(64)
#     print(data, len(data))
#     if(len(data) > 0):
#         print(data[0])
#         if(data[0] == 0):
#             print('Restarting machine..')
#             machine.reset()
#         return data[0]
#     else:
#         return 0

# Fetches sensor value.
# def run_sensor():
#     # Make sure output is low
#     trigger.value(0)
#     utime.sleep_us(10)
#
#     # Trigger 8 cycle sonic burst by setting trigger to high for 10us
#     trigger.value(1)
#     utime.sleep_us(10)
#     trigger.value(0)
#
#     # Wait for pulse to start on input pin.
#     while echo() == 0:
#         pass
#     start = utime.ticks_us()
#
#     # Run until input pin changes to low.
#     while echo() == 1:
#         pass
#     finish = utime.ticks_us()
#
#     utime.sleep_ms(10)
#
#     # Calculate and print out distance measured.
#     return ((utime.ticks_diff(finish, start)) * .03426)/2

# # Calibrate initial sensor distance to target.
# def sensor_calibration():
#     pycom.rgbled(COLOUR_DARKYELLOW)
#     print('Starting calibration..')
#     median_list = []
#     counter = 0
#     for i in range(200):
#         counter = counter + 1
#         median_list.append(sensor.run_sensor(trigger, echo))
#
#     median_list.sort()
#
#     global distance
#     distance = median_list[int(counter/2)]
#     median_list.clear()
#
#     print('Distance calibrated: ', distance)
#     print('Calibration done.. ')
#     time.sleep(0.1)

# # Sends message and searches for ack's from server.
# def messageHandler(message):
#     pycom.rgbled(palette.COLOUR_DARKGREEN)
#
#     LoPy.send_msg(message)
#     time.sleep(1)
#
#     pycom.rgbled(palette.COLOUR_DARKBLUE)
#
#     # Check for messages received.
#     for i in range(5):
#         # Send ack message to receive downlinks.
#         LoPy.send_msg('ack'.encode('utf-8'))
#         ack = LoPy.recv_msg()
#         # If ack has been received let server handle itself before new measurements.
#         if(ack > 0):
#             pycom.rgbled(palette.COLOUR_WHITE)
#             time.sleep(HOLD_SENSOR)
#             break
#         if(i == 4):
#             pycom.rgbled(palette.COLOUR_RED)
#             # print('No ack received. Listening for sensor values.')
#             return True
#         time.sleep(1)
#
# # Creates a message id.
# def idcreator():
#     return ''.join(map(str, rtc.now()[:-1]))
