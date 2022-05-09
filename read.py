#!/usr/bin/env python3
import sys
import serial
import time



ser = serial.Serial('/dev/ttyUSB0',115200,timeout=None)
#ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)

def send_req(str):
  print("Send:" + str);  
  ser.write(str.encode('utf-8'))
  

def show_res():
  while(1):
    line=ser.readline()
    if (line):
      try:  
        print(line.decode())
      except:
        continue;  
    else:
      break;

#line = ser.readline()

while(True):
    show_res()
    time.sleep(1)


ser.close()