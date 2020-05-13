from network import LoRa
from machine import RTC

import pycom
import socket
import time
import ubinascii
import machine
import palette
import keys

# Set the date for machine.
rtc = RTC()
rtc.init((2020, 3, 2, 15, 34, 10))

counter = 0

# Number of seconds to hold sensor after ack.
HOLD_SENSOR = 5

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, adr=True)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify(keys.APP_EUI)
app_key = ubinascii.unhexlify(keys.APP_KEY)

# Connect to LoRa gateway through OTAA
def connect_lora():
    pycom.rgbled(palette.COLOUR_DARKRED)
    # join a network using OTAA (Over the Air Activation)
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)

    connector = 0
    # wait until the module has joined the network
    while not lora.has_joined():
        time.sleep(3)
        print('Waiting for connection..')
        connector = connector + 1
        if(connector > 5):
            machine.reset()

    print('Connected to gateway.')
    pycom.rgbled(palette.COLOUR_DARKGREEN)

    # create a LoRa socket and make object global for other functions.
    global s
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 1)

# Send a message over LoRa.
def send_msg(byteEncoded):
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    s.send(byteEncoded)
    print('Sent bytes: ', byteEncoded)

# Receive messages from LoRa gateway
def recv_msg():
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print('Ack received, controlling..')
    if(len(data) > 0):
        return data[0]
    else:
        return -1

# Creates a message id.
def idcreator(time):
    idtime = time[:-1]                 # Tuple of time. TZ excluded
    strtime = ''.join(map(str, idtime))     # Concatenated string of tuple.
    return strtime

# Sends message and searches for ack's from server.
def sendrecv(message = ''):
    pycom.rgbled(palette.COLOUR_GREEN)

    # Create message id and send
    # message = idcreator(rtc.now())
    send_msg(message.encode('utf-8'))
    time.sleep(1)

    pycom.rgbled(palette.COLOUR_DARKBLUE)

    # Check for messages received.
    for i in range(10):
        ack = recv_msg()
        check_ack = int(message[-3:])

        # Send ack message to receive downlinks.
        # If ack has been received let server handle itself before new measurements.
        if(ack >= 0 and ack == check_ack):
            pycom.rgbled(palette.COLOUR_WHITE)
            print('Correct ack received from server.')
            send_msg(('ack' + message).encode('utf-8'))
            time.sleep(HOLD_SENSOR)
            print('Ready for sensor..')
            break
        else:
            # If no or wrong ack received, send message again.
            send_msg(message)
            time.sleep(1)
            pycom.rgbled(palette.COLOUR_RED)
        if(i == 10):
            # Loop again.
            return True
        time.sleep(1)

def joined():
    return lora.has_joined()
