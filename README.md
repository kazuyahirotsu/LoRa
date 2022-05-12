# LoRa
## make the environment  
```
$ git clone git@github.com:kazuyahirotsu/LoRa.git
$ cd LoRa
$ virtualenv -p 3.10 lora
$ source lora/bin/activate
$ pip install -r requirements.txt
$ pip list
```  

## pi@lora-gateway-rpi7068.local
power on  
select z on ```$ screen /dev/ttyUSB0 9600```  
run ```base.py```  

## pi@lora-gateway-rpi7067.local
power on  
connect to the same network as mac  

## mac
run ```gps_ssh_setup.py```, then ```send_gps_mac.py```
