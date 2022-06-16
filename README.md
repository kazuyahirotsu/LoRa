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
ssh to this machine and run  
```
$ python setup_7068.py  
$ python base.py
```  

## pi@lora-gateway-rpi7067.local
ssh to this machine and run  
```
$ python setup_7067.py  
```  

## mac
connect gps module and run  
```
$ python gps_ssh_setup.py
$ python send_gps_mac.py /dev/cu.usbserial-0001
```
