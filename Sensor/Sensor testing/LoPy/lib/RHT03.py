'''
Reads relative humidity and temperature with the RHT03 sensor.

@author Lars Petter Ulvatne, Linnaeus University.
'''

from pycom import pulses_get
from time import sleep_ms
import time
from machine import Pin

# For fast conversion of half byte decimal values.
half_byte = {
    "0000": 0,
    "0001": 1,
    "0010": 2,
    "0011": 3,
    "0100": 4,
    "0101": 5,
    "0110": 6,
    "0111": 7,
    "1000": 8,
    "1001": 9,
    "1010": 10,
    "1011": 11,
    "1100": 12,
    "1101": 13,
    "1110": 14,
    "1111": 15
}

# For fast conversion of half byte into order of half byte.
byte_value = [4096,256,16,1]

'''
Calculates the value of a byte based on if its the high or low byte of the
16 bit values used by RHT03. In low order bytes, the byte value is the same as
the low order value. Startswith MSB as leftmost bit.
Returns tuple of decimal values, with byte order value and byte value without
order (high/low order value, byte value).
'''
def calc_bytes(byte_str, order = 'low'):
    values = divide_bytes(byte_str)
    byte_val = values[0]*byte_value[2] + values[1]*byte_value[3]

    if(order == 'high'):
        high_order = values[0]*byte_value[0] + values[1]*byte_value[1]
        return (high_order, byte_val)
    else:
        return (byte_val, byte_val)


'''
Divides a byte in half, to retrieve the decimal value from dictionary. Starts
with MSB as leftmost bit.
Returns tuple of values retrieved from higher and lower 4-bits (high, low).
'''
def divide_bytes(byte_str):
    high = half_byte[byte_str[:4]]
    low = half_byte[byte_str[4:]]
    return (high, low)

'''
Checks pulsewidth of each high pulse, which will describe each state of bit:
    0: 18 <= pulsewidth <= 28
    1: 65 <= pulsewidth <= 75
Adds to a string, and appends string to array each 8 bits.
'''
def extract_bytes(data):
    byte_str = ''
    byte_arr = []

    for i in range(1, len(data) + 1):
        bit = data[i - 1]
        if(bit[0] == 1):
            if(18 <= bit[1] <= 28):
                byte_str = byte_str + "0"
            elif(65 <= bit[1] <= 75):
                byte_str = byte_str + "1"
        if(i % 16 == 0 and i != 0):
            byte_arr.append(byte_str)
            byte_str = ''

    return byte_arr

'''
Fetches the pulses from pin in open-drain mode.
'''
def get_pulses():
    data = [(0,0)]
    cnt = 0
    tester = True
    pulses = 100

    while(tester):
        pin = Pin('P21', mode=Pin.OPEN_DRAIN)
        pin(0)
        sleep_ms(20)
        pin(1)

        data = pulses_get(pin, pulses)         # Fetches all pulses > 100ms
        tester = not (data[0][0] == 1 and len(data) == 80)
    return data

'''
Fetch relative humidity and temperature with the RHT03 sensor.
'''
def run_sensor():
    negative = False

    data = get_pulses()
    time.sleep(0.2)

    # 40 bits data (1) and 40 bit pause (0)
    if(len(data) == 80):
        byte_arr = extract_bytes(data)      # Extract bytes from fetched pulses.

        humid = (calc_bytes(byte_arr[0], 'high'), calc_bytes(byte_arr[1], 'low'))
        temp = (calc_bytes(byte_arr[2], 'high'), calc_bytes(byte_arr[3], 'low'))
        check_sum = calc_bytes(byte_arr[4])[0]

        # Fix decimal value if below 0 degrees.
        if(temp[0][0] >= 32768):
            temp = ((temp[0][0] - 32768, temp[0][1]), temp[1])
            negative = True

        hum_temp_sum = (humid[0][1] + humid[1][1] + temp[0][1] + temp[1][1]) % 256

        if(hum_temp_sum == check_sum):
            humidity = (humid[0][0] + humid[1][0])/10
            temperature = (temp[0][0] + temp[1][0])/10

            if(negative):
                temperature = -1*temperature

            return (humidity, temperature)
        else:
            raise ValueError('Checksum error.')
    else:
        raise ValueError('Wrong sensor output.')
