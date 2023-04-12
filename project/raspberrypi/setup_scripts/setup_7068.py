#!/usr/bin/env python3
import sys
import serial
import time



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

ser.close()
