#!/usr/bin/env python3
import sys
import serial
import time

#place this file where you get in first when you ssh to this machine

ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)
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
        continue
    else:
      break

args = sys.argv
line = ser.readline()
#show_res()
#send_req("\r\n")
#show_res()
#send_req("\r\n")
#show_res()
#time.sleep(1)

## command z go operation
#send_req("z\r\n")
#show_res()
#time.sleep(1)

message = args[1]+"\r\n"
send_req(message)
show_res()
time.sleep(1)

ser.close()
