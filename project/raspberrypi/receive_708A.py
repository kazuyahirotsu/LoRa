#!/usr/bin/env python3
import sys
import serial
import time
# import boto3
# from botocore.config import Config
import logging
import random
import os
os.popen('sh /root/lora-gateway/reset-lora.sh')
import ambient
import datetime

ambi = ambient.Ambient(60089, "45bda2767374dfd8")
# logging.basicConfig(format='%(asctime)s %(message)s',filename='solarpanel_voltage.log', encoding='utf-8', level=logging.DEBUG)
# setup logger
root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO) # or whatever
handler = logging.FileHandler('test.log',  encoding='utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(message)s')) # or whatever
root_logger.addHandler(handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# setup aws
# session = boto3.Session()
# write_client = session.client('timestream-write', region_name='ap-northeast-1', config=Config(read_timeout=20, max_pool_connections = 5000, retries={'max_attempts': 10}))
# DatabaseName='izunuma'
# TableName='izunuma'
# dimensions = [
#         {'Name': 'Location', 'Value': 'Tokyo'},
# ]

# setup serial
ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)
#ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)

def send_req(str):
  print("Send:" + str) 
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
  send_req("c 7\r\n")
  show_res()
  time.sleep(1)

  # command u power
  send_req("u -4\r\n")
  show_res()
  time.sleep(1)

  # command f srcID 
  send_req("f 708A\r\n")
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
   
  # command retry
  send_req("m 0\r\n")
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

  # # command y confirm 
  # send_req("y\r\n")
  # show_res()
  # time.sleep(5)

  # command z go operation
  send_req("z\r\n")
  show_res()
  time.sleep(1)

  # send_req("hello\r\n")
  # show_res()
  # time.sleep(1)

  # while(True):
  #     show_res()
  #     time.sleep(1)

  # ser.close()


def current_milli_time():
  return int(time.time() * 1000)

# def send(values):

#   # dummy_value1 = 12+random.random()
#   # dummy_value2 = 12+random.random()
#   # dummy_value3 = 12+random.random()
  
#   try:
#     try:
#       float1 = float(str(values[1]))
#       value1_valid = True
#     except:
#       value1_valid = False
#     try:
#       float2 = float(str(values[2]))
#       value2_valid = True
#     except:
#       value2_valid = False
#     try:
#       float3 = float(str(values[3]))
#       value3_valid = True
#     except:
#       value3_valid = False
#     try:
#       float5 = float(str(values[5]))
#       value5_valid = True
#     except:
#       value5_valid = False

#     record = []
#     if (values[1] != "") and value1_valid:
#       record.append({
#         'Dimensions': dimensions,
#         'MeasureName': str(values[0])+'DO_1',
#         'MeasureValueType': 'DOUBLE',
#         'MeasureValue': str(values[1]),
#         'Time': str(values[4]),
#         'TimeUnit': 'SECONDS'
#       })
#     if (values[2] != "") and value2_valid:
#       record.append({
#         'Dimensions': dimensions,
#         'MeasureName': str(values[0])+'DO_2',
#         'MeasureValueType': 'DOUBLE',
#         'MeasureValue': str(values[2]),
#         'Time': str(values[4]),
#         'TimeUnit': 'SECONDS'
#     })
#     if (values[3] != "") and value3_valid:
#       record.append({
#         'Dimensions': dimensions,
#         'MeasureName': str(values[0])+'TEMP',
#         'MeasureValueType': 'DOUBLE',
#         'MeasureValue': str(values[3]),
#         'Time': str(values[4]),
#         'TimeUnit': 'SECONDS'
#     })
#     if (values[5] != "") and value5_valid:
#       record.append({
#         'Dimensions': dimensions,
#         'MeasureName': str(values[0])+'RSSI',
#         'MeasureValueType': 'DOUBLE',
#         'MeasureValue': str(values[5]),
#         'Time': str(values[4]),
#         'TimeUnit': 'SECONDS'
#     })
#     result = write_client.write_records(DatabaseName=DatabaseName,
#                                         TableName=TableName,
#                                         Records=record,
#                                         CommonAttributes={})
#     print(result)
#     logging.info("aws success")
#   except Exception as e:
#     print(e)
#     logging.info(e)

#   try:
#     logging.info("values = "+str(values))
#   except Exception as e:
#     print(e)
#     logging.info(e)


if __name__ == "__main__":
  setup()
#   time_to_send = False
#   send_minute = int(time.strftime("%M")) + (10-int(time.strftime("%M"))%10)
#   send_minute_now = send_minute
# #  send_minute = int(time.strftime("%M")) + 1

#   if send_minute == 60:
#     send_minute = 0
#   logging.info("send time at "+str(send_minute)+"m")

  while True:
    # if int(time.strftime("%M")) == send_minute:
    #   time_to_send = True
    #   send_minute_now = send_minute
    #   send_minute += 10
    #   # send_minute += 1
    #   if send_minute == 60:
    #     send_minute = 0
    #   logging.info("next send time at "+str(send_minute)+"m")

    # while time_to_send:
    # time_message = "r,7068,"+str(int(time.time())) + "\r\n"

    # send_req(time_message)
    # time.sleep(3)
    # logging.info("getting ok")

    # message = show_res()
    # if ok is not None:
    #   ok = ok.replace('\n', '').replace('\r', '')
    # if ok == "OK":
    #   print("it was ok")
    # elif ok == "NG 103":
    #   print("it was not ok")
    # else:
    #   print("it was something else")
      # logging.info("getting ack")
      # ack_0001 = show_res()
      # if ok is not None:
      #   ok = ok.replace('\n', '').replace('\r', '')
      # if ack_0001 is not None:
      #   ack_0001 = ack_0001[12:].replace('\n', '').replace('\r', '')
      # if ok == "OK" and ack_0001 == "0001":
      #   time_to_send = False
      #   logging.info("waiting for the data")
      # if int(time.strftime("%M")) >= send_minute_now+5:
      #   time_to_send = False
      #   logging.info("0001 not receiving time for 5 min")

    message = show_res()
    if message is not None:
      message = message.replace('\n', '').replace('\r', '')
      try:
        # logging.info("raw message = "+str(message))
        logging.info((message[4:]+","+str(twosComplement_hex(message[:4]))))

      except Exception as e:
        print(e)

      try:
        time_ambi = str(datetime.datetime.fromtimestamp(int(message[4:])).strftime('%Y-%m-%d %H:%M:%S'))
        ambi.send({
          'created': time_ambi, 
          'd2': twosComplement_hex(message[:4])})
      except Exception as e:
        print(e)

    time.sleep(1)

  ser.close()