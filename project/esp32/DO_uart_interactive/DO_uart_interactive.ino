// disable continuous reading and ok response with this script
// C,0
// *OK,0
// R
#include <SoftwareSerial.h> 
//SoftwareSerial do_ss(19, 18);
SoftwareSerial do_ss(26, 25);

String inputstring = "";                              //a string to hold incoming data from the PC
String sensorstring = "";                             //a string to hold the data from the Atlas Scientific product
boolean input_string_complete = false;                //have we received all the data from the PC
boolean sensor_string_complete = false;               //have we received all the data from the Atlas Scientific product
float DO;                                             //used to hold a floating point number that is the DO


void setup() {
  pinMode(13,OUTPUT);
  digitalWrite(13,HIGH);
  delay(1000);

  //set up the hardware
  Serial.begin(9600);                                 //set baud rate for the hardware serial port_0 to 9600
  do_ss.begin(9600);                                //set baud rate for software serial port_3 to 9600
  inputstring.reserve(10);                            //set aside some bytes for receiving data from the PC
  sensorstring.reserve(30);                           //set aside some bytes for receiving data from Atlas Scientific product
}

void loop() {                                         //here we go...
  if (Serial.available()){                              //if the hardware serial port_0 receives a char
    Serial.print("typed: ");
    inputstring = Serial.readStringUntil(13);           //read the string until we see a <CR>
    Serial.println(inputstring);
    input_string_complete = true;                       //set the flag used to tell if we have received a completed string from the PC
  }
  
    if (do_ss.available()){                              //if the hardware serial port_0 receives a char
    Serial.print("received: ");
    sensorstring = do_ss.readStringUntil(13);           //read the string until we see a <CR>
    Serial.println(sensorstring);
    sensor_string_complete = true;                       //set the flag used to tell if we have received a completed string from the PC
  }


  if (input_string_complete == true) {                //if a string from the PC has been received in its entirety
    do_ss.print(inputstring);                       //send that string to the Atlas Scientific product
    do_ss.print('\r');                              //add a <CR> to the end of the string
    inputstring = "";                                 //clear the string
    input_string_complete = false;                    //reset the flag used to tell if we have received a completed string from the PC
  }


  if (sensor_string_complete == true) {               //if a string from the Atlas Scientific product has been received in its entirety
    Serial.println(sensorstring);                     //send that string to the PC's serial monitor
   /*                                                 //uncomment this section to see how to convert the D.O. reading from a string to a float 
    if (isdigit(sensorstring[0])) {                   //if the first character in the string is a digit
      DO = sensorstring.toFloat();                    //convert the string to a floating point number so it can be evaluated by the Arduino
      if (DO >= 6.0) {                                //if the DO is greater than or equal to 6.0
        Serial.println("high");                       //print "high" this is demonstrating that the Arduino is evaluating the DO as a number and not as a string
      }
      if (DO <= 5.99) {                               //if the DO is less than or equal to 5.99
        Serial.println("low");                        //print "low" this is demonstrating that the Arduino is evaluating the DO as a number and not as a string
      }
    }
  */
  }
  sensorstring = "";                                  //clear the string:
  sensor_string_complete = false;                     //reset the flag used to tell if we have received a completed string from the Atlas Scientific product
}
