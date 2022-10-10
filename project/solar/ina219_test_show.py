#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
import ambient
import time

ambi = ambient.Ambient(53835, "b68eaa4a9767851b")

SHUNT_OHMS = 0.1


def read():
    ina = INA219(SHUNT_OHMS)
    ina.configure()

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)
    
#    try:
#        ambi.send({
#            "d1": ina.voltage(),
#            "d2": ina.current(),
#            "d3": ina.power(),
#            "d4": ina.shunt_voltage()
#            })
#    except Exception as e:
#        print(e)

if __name__ == "__main__":
    while True:
        read()
        time.sleep(1)