SAMPLES = 25
pycom.heartbeat(False) # disable the blue blinking

# # Set pin input/output for ultrasonic sensor.
# trigger = Pin('P19', mode=Pin.OUT)
# echo = Pin('P20', mode=Pin.IN )
#
# # Set pin input for temperature sensor.
adc = machine.ADC(0, bits=10)                 # create an ADC object

#
# distance = sensor.calibrate(trigger, echo, analog_pin)

   # 1) Output Vref of P22
# adc_cal = adc.vref_to_pin('P22')
# print("P22 (mV):",adc_cal) # this will really print a value?
# # 2) Now measure the value of P22 with a multimeter
# # 3) replace the value of 1100 with the measured value
# adc.vref(1023)

# 4) Now connect your sensor on pin 13 and print the value returned by your sensor
wm_1 = adc.channel(pin='P14', attn = machine.ADC.ATTN_11DB)
print("Sensor 1 (mV): ", wm_1());

def volt_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

distances = []
for x in range(10):
    time.sleep(0.5)
    arr=[]
    tester = 0
    for i in range(SAMPLES):
        time.sleep(0.01)
        sample = wm_1()
        arr.append(sample)
        tester = tester + sample
    arr.sort()
    print(arr)
    ir_val = arr[int(SAMPLES/2)]
    v = (ir_val/1023.0)*5
    dist = 16.2537 * v**4 - 129.893 * v**3 + 382.268 * v**2 - 512.611 * v + 301.439
    # print(dist, ' cm')
    distanceCM = 27.728 * pow(volt_map(ir_val, 0, 1023, 0, 5000)/1000.0, -1.2045)
    print(distanceCM, ' cm')
    distances.append(volt_map(ir_val, 0, 1023, 0, 5000)/1000)
    # distanceCM = 27.728 * pow(v, -1.2045)
    # print(distanceCM, ' cm')
print(sum(distances), len(distances))
distances.sort()
print(distances[int(len(distances)/2)], ' 25cm')
