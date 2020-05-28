'''
Converts number into string and adds zeroes to make 3 digits long.

@author Lars Petter Ulvatne, Linnaeus University.
'''

def count(counter):
    if(counter > 99):
        return str(counter)
    elif(counter > 9):
        return '0' + str(counter)
    else:
        return '00' + str(counter)
