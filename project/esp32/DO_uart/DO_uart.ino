#include <SoftwareSerial.h> 
SoftwareSerial do_ss(18, 19);
String sensorstring = "";                             //a string to hold the data from the Atlas Scientific product
boolean waiting_for_respond = false;
int received_message_num = 0;


void setup() {                                        //set up the hardware
  Serial.begin(9600);                                 //set baud rate for the hardware serial port_0 to 9600
  do_ss.begin(9600);                                //set baud rate for software serial port_3 to 9600
  sensorstring.reserve(30);                           //set aside some bytes for receiving data from Atlas Scientific product
}

void loop() {                                        //here we go...
    while(do_ss.available())do_ss.read();             // clear the buffer

    do_ss.print("r\r");
    Serial.println("send: r");
    waiting_for_respond = true;

    while(waiting_for_respond){
        while (do_ss.available()){                              //if the hardware serial port_0 receives a char
        Serial.print("received: ");
        sensorstring = do_ss.readStringUntil(13);           //read the string until we see a <CR>
        Serial.println(sensorstring);
        received_message_num += 1;
        }
        if(received_message_num == 2){
            received_message_num = 0;
            waiting_for_respond = false;
        }
        delay(100);
    }

}
