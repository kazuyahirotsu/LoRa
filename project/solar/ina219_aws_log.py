#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
import time
import boto3
from botocore.config import Config
import time
import logging

# logging.basicConfig(format='%(asctime)s %(message)s',filename='solarpanel_voltage.log', encoding='utf-8', level=logging.DEBUG)

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('test.log',  encoding='utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s')) # or whatever
root_logger.addHandler(handler)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

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
        logging.info("aws success")
    except Exception as e:
        print(e)
        logging.info(e)

    try:
        logging.info("voltage = "+str(ina.voltage()))
    except Exception as e:
        print(e)
        logging.info(e)


if __name__ == "__main__":
    while True:
        read()
        time.sleep(60)