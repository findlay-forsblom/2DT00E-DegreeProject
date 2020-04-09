'''
Measures temperature in celcius by measuring the output voltage. See datasheet
for equations and constants.

@author Lars Petter Ulvatne, Student at Linnaeus University.
'''

V_0 = 500.0                       # mV at 0 degree celsius
T_C = 10.0                        # mV/degree (Temperature coefficient)

def readTemp(pin):
    V_OUT = pin.voltage()
    return (V_OUT-V_0)/T_C
