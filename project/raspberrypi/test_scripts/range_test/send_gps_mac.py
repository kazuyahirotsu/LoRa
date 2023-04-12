import paramiko
import sys
import serial
import logging

logging.basicConfig(format='%(asctime)s %(message)s',filename='rangetest_results/send6_15.log', encoding='utf-8', level=logging.DEBUG)
# when not sending to file
# logging.getLogger().setLevel(logging.INFO)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# Update the next three lines with your
# server's information

host = "lora-gateway-rpi7067.local"
username = "pi"
password = "nakaolab"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
args = sys.argv
ser = serial.Serial(args[1],9600)

stdin, stdout,stderr = client.exec_command("send_test.py") #setup and test
print(stdout.read().decode())
stdin, stdout,stderr = client.exec_command("echo b")
print(stdout.read().decode())

send_count = 0

while True:
    # command = input("waiting for Enter:")
    # print(command=="")
    # if command != "":
    #     continue
    line = ser.readline()
    splited_line = line.decode().split(",")
    # print(splited_line)
    if splited_line[0] == "$GNGGA":
        hour =int((splited_line[1])[:2]) + 9
        minute = int((splited_line[1])[2:4])
        second = float((splited_line[1])[4:])

        status = splited_line[6]
        if status == "0":
            print("gps not fix")
            stdin, stdout,stderr = client.exec_command("python send_gps.py "+str(send_count)+ ",gpsnotfix") #sending gps info from ssh lora to base lora
            print(stdout.read().decode())
            send_count += 1
        elif status == "1" or status == "2":
            if status == "1":
                print("gps fix")
            else:
                print("dgps fix")
            print(splited_line[7]+"satelites found")
            lat = float((splited_line[2])[:2]) + float((splited_line[2])[2:])/60.0
            lon = float((splited_line[4])[:3]) + float((splited_line[4])[3:])/60.0
            messagetosend = str(send_count) + "," + str(lat) + "," + splited_line[3] + "," + str(lon) + "," + splited_line[5]
            print(messagetosend)
            logging.info(messagetosend)
            command = "python send_gps.py "+messagetosend

            stdin, stdout,stderr = client.exec_command(command) #sending gps info from ssh lora to base lora
            print(stdout.read().decode())
            send_count += 1

        else:
            print("status: "+status)
stdin.close()
stdout.close()
stderr.close()
client.close()

ser.close()