from pycom import pulses_get
from time import sleep_ms
import time
from machine import Pin

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

#
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

def extract_bytes(data):
    byte_str = ''
    byte_arr = []

    for i in range(1, 81):
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

def get_humidity(byte_arr):
    return (calc_bytes(byte_arr[0], 'high'), calc_bytes(byte_arr[1], 'low'))

def get_temperature(byte_arr):
    if(byte_arr[0][0] != '1'):
        return (calc_bytes(byte_arr[0], 'high'), calc_bytes(byte_arr[1], 'low'))
    else:
        return (-1*calc_bytes(byte_arr[0], 'high'), calc_bytes(byte_arr[1], 'low'))

def run_sensor():
    pin = Pin('P21', mode=Pin.OPEN_DRAIN)
    print(pin)

    pin(0)
    sleep_ms(20)
    pin(1)
    data = pulses_get(pin, 100)         # Fetches all pulses > 100ms
    time.sleep(0.2)

    if(len(data) == 80):
        byte_arr = extract_bytes(data)      # Extract bytes from fetched pulses.

        humid = get_humidity(byte_arr[:2])
        temp = get_temperature(byte_arr[2:4])
        check_sum = calc_bytes(byte_arr[4])[0]
        hum_temp_sum = (humid[0][1] + humid[1][1] + temp[0][1] + temp[1][1]) % 256

        if(hum_temp_sum == check_sum):
            return ((humid[0][0] + humid[1][0])/10, (temp[0][0] + temp[1][0])/10)
        else:
            raise ValueError('Checksum error.')
    else:
        print('NOT 80 BITS!!!!!!')
        raise ValueError('Wrong sensor output.')
