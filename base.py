#!/usr/bin/env python3
import sys
import serial
import time
import logging

logging.basicConfig(format='%(asctime)s %(message)s',filename='rangetest.log', encoding='utf-8', level=logging.DEBUG)
# when not sending to file
# logging.getLogger().setLevel(logging.INFO)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)

def send_req(str):
  print("Send:" + str);  
  ser.write(str.encode('utf-8'))
  

def show_res():
  while(1):
    line=ser.readline()
    if (line):
      try:  
        #print(line.decode())
        return line
      except:
        continue;  
    else:
      break;
def twosComplement_hex(hexval):
    bits = 16
    val = int(hexval, bits)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val

line = ser.readline()
show_res()
send_req("\r\n")
show_res()
send_req("\r\n")
show_res()
time.sleep(1)

# command z go operation
send_req("z\r\n")
show_res()
time.sleep(1)

count = 0
while(True):
    count += 1
    if count%10==0:
        send_req("hello\r\n")
    message = show_res()
    try:
        logging.info("RSSI="+str(twosComplement_hex(message[:4]))+"dBm, message="+message[12:])
    except:
        continue
    time.sleep(1)

ser.close()
