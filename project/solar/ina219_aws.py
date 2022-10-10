#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
import time
import boto3
from botocore.config import Config
import time

SHUNT_OHMS = 0.1

session = boto3.Session()
write_client = session.client('timestream-write', region_name='us-west-2', config=Config(read_timeout=20, max_pool_connections = 5000, retries={'max_attempts': 10}))
DatabaseName='solarpanel_test'
TableName='solarpanel_test'
dimensions = [
        {'Name': 'Location', 'Value': 'Tokyo'},
]

def current_milli_time():
    return round(time.time() * 1000)

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
    
    try:
#        measurevalues = [{
#            'Name': 'bus voltage',
#            'Value': str(ina.voltage()),
#            'Type': 'DOUBLE'
#            },
#            {
#            'Name': 'bus current',
#            'Value': str(ina.current()),
#            'Type': 'DOUBLE'
#            },
#            {
#            'Name': 'power',
#            'Value': str(ina.power()),
#            'Type': 'DOUBLE'
#            }]

        record = [{
            'Dimensions': dimensions,
            'MeasureName': 'battery_voltage',
            'MeasureValueType': 'DOUBLE',
            'MeasureValue': str(ina.voltage()),
            'Time': str(current_milli_time()),
            'TimeUnit': 'MILLISECONDS'
        }]
        result = write_client.write_records(DatabaseName=DatabaseName,
                                            TableName=TableName,
                                            Records=record,
                                            CommonAttributes={})
    except Exception as e:
        print(e)

if __name__ == "__main__":
    while True:
        read()
        time.sleep(60)