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
import datetime

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
  send_req("f 708C\r\n")
  show_res()
  time.sleep(1)

   # command g dstID
  send_req("g FFFF\r\n")
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


if __name__ == "__main__":
  setup()

  while True:

    send_req("hello\r\n")
    show_res()

    time.sleep(1)

  ser.close()