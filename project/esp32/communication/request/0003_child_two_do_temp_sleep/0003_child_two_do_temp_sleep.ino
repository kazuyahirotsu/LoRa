#include <SoftwareSerial.h>
#include "RTClib.h"

#define UART_RX 16  // ES920LR 8(TX)
#define UART_TX 17  // ES920LR 9(RX)
#define LoRa_Rst 5 //  ES920LR 24(RESETB)
#define TEMP 32
#define CLOCK_INTERRUPT_PIN 4

const float ANALOG_MAX = 4096;

SoftwareSerial LoRa_ss(UART_RX, UART_TX);
SoftwareSerial do_ss(19, 18);
SoftwareSerial do_ss2(26, 25);

RTC_DS3231 rtc;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
String data_to_send;

String sensorstring = "";                             //a string to hold the data from the Atlas Scientific product
String sensorstring2 = "";                             //a string to hold the data from the Atlas Scientific product
boolean waiting_for_respond = false;
int received_message_num = 0;

int now_minute=0;
int before_minute=0;

void LoRa_read() {
  // just read message
  if (LoRa_ss.available())Serial.print("from LoRa >>");
  while (LoRa_ss.available()) {
    char c = LoRa_ss.read();
    if (c < 0x80){
      Serial.print(c);
    }
    delay(1);
  }
}

void LoRa_write(char msg[]) {
  // write message
  LoRa_ss.write(msg);
  Serial.print("to   LoRa >>");
  Serial.print(msg);
  delay(500);
  LoRa_read();
}

void LoRa_write_string(String msg) {
  // write message
  char str_array[msg.length()+1];
  msg.toCharArray(str_array, msg.length()+1);
  LoRa_ss.write(str_array);
  Serial.print("to   LoRa >>");
  Serial.println(str_array);
  LoRa_ss.write("\r\n");
}

String parsed_data[3] = {"\0"};

int split(String data, char delimiter, String *dst){
    int index = 0;
    dst[index] = "";
    int arraySize = (sizeof(data)/sizeof((data)[0]));  
    int datalength = data.length();
    for (int i = 0; i < datalength; i++) {
        char tmp = data.charAt(i);
        if ( tmp == delimiter ) {
            index++;
            dst[index] = "";
            if ( index > (arraySize - 1)) return -1;
        }
        else dst[index] += tmp;
    }
    return (index + 1);
}

void do_send(String msg, boolean sensor_data){
      do_ss.print(msg);
      Serial.println("send: "+msg);
      waiting_for_respond = true;
      int t0 = rtc.now().unixtime();
      delay(100);

      while(waiting_for_respond){
          while (do_ss.available()){                              //if the hardware serial port_0 receives a char
          Serial.print("received: ");
          if(sensor_data){
            sensorstring = do_ss.readStringUntil(13);           //read the string until we see a <CR>
            Serial.println(sensorstring);
          }else{
            String received_message = do_ss.readStringUntil(13);           //read the string until we see a <CR>
            Serial.println(received_message);
          }
          received_message_num += 1;
          }
          if(received_message_num >= 1){
              received_message_num = 0;
              waiting_for_respond = false;
          }
          if(rtc.now().unixtime() - t0 >= 5){
            waiting_for_respond = false;
          }
          delay(100);
      }
}

void do_send2(String msg, boolean sensor_data){
      do_ss2.print(msg);
      Serial.println("send: "+msg);
      waiting_for_respond = true;
      int t0 = rtc.now().unixtime();
      delay(100);

      while(waiting_for_respond){
          while (do_ss2.available()){                              //if the hardware serial port_0 receives a char
          Serial.print("received: ");
          if(sensor_data){
            sensorstring2 = do_ss2.readStringUntil(13);           //read the string until we see a <CR>
            Serial.println(sensorstring2);
          }else{
            String received_message = do_ss2.readStringUntil(13);           //read the string until we see a <CR>
            Serial.println(received_message);
          }
          received_message_num += 1;
          }
          if(received_message_num >= 1){
              received_message_num = 0;
              waiting_for_respond = false;
          }
          if(rtc.now().unixtime() - t0 >= 5){
            waiting_for_respond = false;
          }
          delay(100);
      }
}

void print_wakeup_reason(){
  esp_sleep_wakeup_cause_t wakeup_reason;

  wakeup_reason = esp_sleep_get_wakeup_cause();

  switch(wakeup_reason)
  {
    case ESP_SLEEP_WAKEUP_EXT0 : Serial.println("Wakeup caused by external signal using RTC_IO"); break;
    case ESP_SLEEP_WAKEUP_EXT1 : Serial.println("Wakeup caused by external signal using RTC_CNTL"); break;
    case ESP_SLEEP_WAKEUP_TIMER : Serial.println("Wakeup caused by timer"); break;
    case ESP_SLEEP_WAKEUP_TOUCHPAD : Serial.println("Wakeup caused by touchpad"); break;
    case ESP_SLEEP_WAKEUP_ULP : Serial.println("Wakeup caused by ULP program"); break;
    default : Serial.printf("Wakeup was not caused by deep sleep: %d\n",wakeup_reason); break;
  }
}

void onAlarm() {
    Serial.println("Alarm occured!");
}

void setup() {
  pinMode(13,OUTPUT);
  digitalWrite(13,HIGH);

  analogSetAttenuation(ADC_6db);
  pinMode(TEMP,ANALOG);

  Serial.begin(9600);
  while(!Serial){
    //wait till Serial
  }
  delay(1000); // DON'T COMMENT OUT THIS

  //Print the wakeup reason for ESP32
  print_wakeup_reason();

  // RTC setting up
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1) delay(10);
  }

  if (rtc.lostPower()) {
    Serial.println("RTC lost power, let's set the time!");
    // When time needs to be set on a new device, or after a power loss, the
    // following line sets the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }

  // When time needs to be re-set on a previously configured device, the
  // following line sets the RTC to the date & time this sketch was compiled
  // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  // This line sets the RTC with an explicit date & time, for example to set
  // January 21, 2014 at 3am you would call:
  // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  
  // DO setup
  do_ss.begin(9600);                                //set baud rate for software serial port_3 to 9600
  while(!do_ss){
    //wait till Serial
  }

  do_ss2.begin(9600);                                //set baud rate for software serial port_3 to 9600
  while(!do_ss2){
    //wait till Serial
  }
  delay(3000);
  
  sensorstring.reserve(30);                           //set aside some bytes for receiving data from Atlas Scientific product
  do_send("sleep\r", false);

  sensorstring2.reserve(30);                           //set aside some bytes for receiving data from Atlas Scientific product
  do_send2("sleep\r", false);
  
  LoRa_ss.begin(9600);
  while(!LoRa_ss){
    //wait till Serial
  }
  Serial.println("Start!!");

  LoRa_write("config\r\n");

  // define reset
  pinMode(LoRa_Rst , OUTPUT);
  delay(100);
  digitalWrite(LoRa_Rst, HIGH);
  delay(100);

  // reset
  Serial.println("Reset");
  digitalWrite(LoRa_Rst, LOW);
  delay(100);
  digitalWrite(LoRa_Rst, HIGH);

  Serial.println("Start reading temp");
  float temp_volts_sum = 0;
  for(int i=0; i<1000; i++){
    temp_volts_sum += (float)analogReadMilliVolts(TEMP);
  }
  float voltage = temp_volts_sum/(float)1000;
  Serial.println(voltage);
  String temp = String((voltage-1058)/9);
  Serial.println(temp);
  
  // get data while waiting for lora to wakeup
  do_send("wakeup\r", false);
  do_send("rt "+temp+"\r", true);
  do_send("sleep\r", false);

  do_send2("wakeup\r", false);
  do_send2("rt "+temp+"\r", true);
  do_send2("sleep\r", false);
//
//  // get data while waiting for lora to wakeup
//  do_send("wakeup\r", false);
//  do_send("r\r", true);
//  do_send("sleep\r", false);
//
//  do_send2("wakeup\r", false);
//  do_send2("r\r", true);
//  do_send2("sleep\r", false);
//
//  float reading = analogRead(TEMP);
//  Serial.println(reading);
//  float voltage = (reading*3.3)/ANALOG_MAX;
//  Serial.println(voltage);
//  String temp = String((voltage-1.058)/0.009);
//  Serial.println((voltage-1.058)/0.009);
//  Serial.println(temp);

  data_to_send = "d,0003,"+sensorstring+","+sensorstring2+","+temp+","+String(rtc.now().unixtime());
  Serial.println(data_to_send);
  // read
  LoRa_read();

  // select processor mode
  LoRa_write("processor\r\n");
  delay(100);

//  // default config
//  LoRa_write("load\r\n");
//  delay(100);
//  
//  // baudrate 9600
//  LoRa_write("baudrate 1\r\n");
//  delay(100);
//  
//  // 125kHz
//  LoRa_write("bw 4\r\n");
//  delay(100);
//
//  // spreading factor 11
//  LoRa_write("sf 11\r\n");
//  delay(100);
//
//  // channel 5
//  LoRa_write("channel 5\r\n");
//  delay(100);
//
//  // PAN
//  LoRa_write("panid 0001\r\n");
//  delay(100);
//
//  // own network id
//  LoRa_write("ownid 0003\r\n");
//  delay(100);
//
//  // destination network id (parent)
//  LoRa_write("dstid 0001\r\n");
//  delay(100);
//
//  // retry num
//  LoRa_write("retry 3\r\n");
//  delay(100);
//
// // save
// LoRa_write("save\r\n");
// delay(10000);

  // into operation mode
  LoRa_write("start\r\n");
  delay(100);


}

void loop() {    
    if (LoRa_ss.available()){
      // get data from LoRa and parse it
      Serial.print("from LoRa >>");
      String data = LoRa_ss.readString();
      Serial.print(data);
      int index = split(data, ',', parsed_data);
      // send data if this edge is requested to send data
      if (parsed_data[1].equals("3")){
        Serial.println("It's my turn!!");

        Serial.print("setting time to ");
        Serial.println(parsed_data[2].toInt());
        rtc.adjust(DateTime(parsed_data[2].toInt()));
        Serial.print("time is now ");
        Serial.println(String(rtc.now().unixtime()));

        LoRa_write_string(data_to_send);
        delay(3000);
        LoRa_read();
        
        digitalWrite(13,LOW);

        //we don't need the 32K Pin, so disable it
        rtc.disable32K();

        // Making it so, that the alarm will trigger an interrupt
        pinMode(CLOCK_INTERRUPT_PIN, INPUT_PULLUP);
        attachInterrupt(digitalPinToInterrupt(CLOCK_INTERRUPT_PIN), onAlarm, FALLING);

        // set alarm 1, 2 flag to false (so alarm 1, 2 didn't happen so far)
        // if not done, this easily leads to problems, as both register aren't reset on reboot/recompile
        rtc.clearAlarm(1);
        rtc.clearAlarm(2);

        // stop oscillating signals at SQW Pin
        // otherwise setAlarm1 will fail
        rtc.writeSqwPinMode(DS3231_OFF);

        // turn off alarm 2 (in case it isn't off already)
        // again, this isn't done at reboot, so a previously set alarm could easily go overlooked
        rtc.disableAlarm(2);

        char date[10] = "hh:mm:ss";
        rtc.now().toString(date);
        Serial.print("now: ");
        Serial.println(date);
        
        DateTime now = rtc.now();
        int wakeup_minute = now.minute()+(10-now.minute()%10);
        if(wakeup_minute==60){
          wakeup_minute = 0;
        }
        DateTime wakeup_time = DateTime(0, 0, 0, 0, wakeup_minute, 0);
        Serial.print("alarm time: ");
        Serial.print(wakeup_time.minute(), DEC);
        Serial.print("m");
        Serial.print(wakeup_time.second(), DEC);
        Serial.println("s");
        
        // schedule an alarm on *0 minute
        if(!rtc.setAlarm1(
                wakeup_time,
                DS3231_A1_Minute // this mode triggers the alarm when the seconds match. See Doxygen for other options
        )) {
            Serial.println("Error, alarm wasn't set!");
        }else {
            Serial.println("Alarm set");
        }
          esp_sleep_enable_ext0_wakeup(GPIO_NUM_4,0); //1 = High, 0 = Low
        
          //Go to sleep now
          Serial.println("Going to sleep now");
          esp_deep_sleep_start();
          Serial.println("This will never be printed");

      }else{
        Serial.println("Not my turn :(");
      }
    }
  }
