#!/usr/bin/env python3
import sys
import serial
import time
import boto3
from botocore.config import Config
import logging
import random

# logging.basicConfig(format='%(asctime)s %(message)s',filename='solarpanel_voltage.log', encoding='utf-8', level=logging.DEBUG)
# setup logger
root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('test.log',  encoding='utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s')) # or whatever
root_logger.addHandler(handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# setup aws
session = boto3.Session()
write_client = session.client('timestream-write', region_name='us-west-2', config=Config(read_timeout=20, max_pool_connections = 5000, retries={'max_attempts': 10}))
DatabaseName='solarpanel_test'
TableName='solarpanel_test'
dimensions = [
        {'Name': 'Location', 'Value': 'Tokyo'},
]

# setup serial
#ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)
ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)

def send_req(str):
  print("Send:" + str);  
  ser.write(str.encode('utf-8'))
  
def twosComplement_hex(hexval):
    bits = 16
    val = int(hexval, bits)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val

def show_res():
  while(1):
    line=ser.readline()
    if (line):
      try:  
        print(line.decode())
        return line.decode()
      except:
        continue
    else:
      break

def setup():
  line = ser.readline()
  show_res()
  send_req("\r\n")
  show_res()
  send_req("\r\n")
  show_res()
  time.sleep(1)

  # command 1 terminal
  send_req("2\r\n")
  show_res()
  time.sleep(1)

  # command d (channel=5) 
  send_req("d 5\r\n")
  show_res()
  time.sleep(1)

  # command c  spreading factor 11
  send_req("c 11\r\n")
  show_res()
  time.sleep(1)

  # command f srcID 
  send_req("f 7068\r\n")
  show_res()
  time.sleep(1)


  # command g dstID
  send_req("g 7067\r\n")
  show_res()
  time.sleep(1)

  # command l ack off (2) 
  # command l ack on (1) 
  send_req("l 1\r\n")
  show_res()
  time.sleep(1)

  # command p RSSI  on
  send_req("p 1\r\n")
  show_res()
  time.sleep(1)

  # command q operation mode 
  send_req("q 1\r\n")
  show_res()
  time.sleep(1)
  
  # command w write 
  send_req("w\r\n")
  show_res()
  time.sleep(1)

  # command y confirm 
  send_req("y\r\n")
  show_res()
  time.sleep(1)

  # command z go operation
  send_req("z\r\n")
  show_res()
  time.sleep(1)

  send_req("hello\r\n")
  show_res()
  time.sleep(1)

  # while(True):
  #     show_res()
  #     time.sleep(1)

  # ser.close()


def current_milli_time():
  return int(time.time() * 1000)

def send(values):

  # dummy_value1 = 12+random.random()
  # dummy_value2 = 12+random.random()
  # dummy_value3 = 12+random.random()
  
  try:
    record = [{
        'Dimensions': dimensions,
        'MeasureName': str(values[0])+'DO_1',
        'MeasureValueType': 'DOUBLE',
        'MeasureValue': str(values[1]),
        'Time': str(current_milli_time()),
        'TimeUnit': 'MILLISECONDS'
    },
    {
        'Dimensions': dimensions,
        'MeasureName': str(values[0])+'DO_2',
        'MeasureValueType': 'DOUBLE',
        'MeasureValue': str(values[2]),
        'Time': str(current_milli_time()),
        'TimeUnit': 'MILLISECONDS'
    },
    {
        'Dimensions': dimensions,
        'MeasureName': str(values[0])+'TEMP',
        'MeasureValueType': 'DOUBLE',
        'MeasureValue': str(values[3]),
        'Time': str(current_milli_time()),
        'TimeUnit': 'MILLISECONDS'
    },
    {
        'Dimensions': dimensions,
        'MeasureName': str(values[0])+'RSSI',
        'MeasureValueType': 'DOUBLE',
        'MeasureValue': str(values[4]),
        'Time': str(current_milli_time()),
        'TimeUnit': 'MILLISECONDS'
    }]
    result = write_client.write_records(DatabaseName=DatabaseName,
                                        TableName=TableName,
                                        Records=record,
                                        CommonAttributes={})
    print(result)
    logging.info("aws success")
  except Exception as e:
    print(e)
    logging.info(e)

  try:
    logging.info("values = "+str(values))
  except Exception as e:
    print(e)
    logging.info(e)


if __name__ == "__main__":
  # setup()
  while True:
    message = show_res()
    if message is not None:
      message = message.replace('\n', ' ').replace('\r', '')
      try:
        print("raw message = "+str(message))
        print(("RSSI= "+str(twosComplement_hex(message[:4]))+"dBm, message= "+message[12:]))
        values = message[12:].split(',')
        values.append(str(twosComplement_hex(message[:4])))
        send(values)
      except Exception as e:
        print(e)
        continue
    time.sleep(1)

  ser.close()