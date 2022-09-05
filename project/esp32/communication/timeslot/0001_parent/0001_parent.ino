#include <SoftwareSerial.h>
#include "RTClib.h"

#define UART_RX 17  // ES920LR 8(TX)
#define UART_TX 16  // ES920LR 9(RX)
#define LoRa_Rst 5 //  ES920LR 24(RESETB)

SoftwareSerial LoRa_ss(UART_TX, UART_RX);

RTC_DS1307 rtc;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
String data0002;
String data0003;

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

void LoRa_read_data(int id) {
  //read message and update the data to send 
  if (id == 2){
    if (LoRa_ss.available())Serial.print("from LoRa >>");
    if (LoRa_ss.available()) {
      data0002 = LoRa_ss.readString();
      Serial.print(data0002);
    }
  }
  else if (id == 3){
    if (LoRa_ss.available())Serial.print("from LoRa >>");
    if (LoRa_ss.available()) {
      data0003 = LoRa_ss.readString();
      Serial.print(data0003);
    }
  }else{
    Serial.print("No such id exists");
  }
}

void LoRa_write_string(String msg) {
  // write message
  char str_array[msg.length()+1];
  msg.toCharArray(str_array, msg.length()+1);
  LoRa_ss.write(str_array);
  Serial.print("to   LoRa >>");
  Serial.println(str_array);
  delay(500);
  LoRa_read();
}

void LoRa_write(char msg[]) {
  // write message
  LoRa_ss.write(msg);
  Serial.print("to   LoRa >>");
  Serial.print(msg);
  delay(500);
  LoRa_read();
}

void setup() {

  // RTC setting up
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1) delay(10);
  }

  if (! rtc.isrunning()) {
    Serial.println("RTC is NOT running, let's set the time!");
    // When time needs to be set on a new device, or after a power loss, the
    // following line sets the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }

  // When time needs to be re-set on a previously configured device, the
  // following line sets the RTC to the date & time this sketch was compiled
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  // This line sets the RTC with an explicit date & time, for example to set
  // January 21, 2014 at 3am you would call:
  // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  
  Serial.begin(9600);
  while(!Serial){
    //wait till Serial
  }
  LoRa_ss.begin(9600);
  
  Serial.println("Start!!");

  LoRa_write("config\r\n");

  // define reset
  pinMode(LoRa_Rst , OUTPUT);
  delay(1000);
  digitalWrite(LoRa_Rst, HIGH);
  delay(1000);

  // reset
  Serial.println("Reset");
  digitalWrite(LoRa_Rst, LOW);
  delay(1000);
  digitalWrite(LoRa_Rst, HIGH);
  delay(3000);

  // read
  LoRa_read();

  // select processor mode
  LoRa_write("processor\r\n");
  delay(1000);

  // default config
  // LoRa_write("load\r\n");
  // delay(100);
  
  // baudrate 9600
  LoRa_write("baudrate 1\r\n");
  delay(100);
  
  // 125kHz
  LoRa_write("bw 4\r\n");
  delay(100);

  // spreading factor 11
  LoRa_write("sf 11\r\n");
  delay(100);

  // channel 5
  LoRa_write("channel 5\r\n");
  delay(100);

  // PAN
  LoRa_write("panid 0001\r\n");
  delay(100);

  // own network id
  LoRa_write("ownid 0001\r\n");
  delay(100);

  // destination network id (raspberry pi)
  LoRa_write("dstid 7068\r\n");
  delay(100);

  // save
  LoRa_write("save\r\n");
  delay(10000);

  // into operation mode
  LoRa_write("start\r\n");
  delay(1000);


}

void loop() {

  DateTime now = rtc.now();

  Serial.print(now.year(), DEC);
  Serial.print('/');
  Serial.print(now.month(), DEC);
  Serial.print('/');
  Serial.print(now.day(), DEC);
  Serial.print(" (");
  Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
  Serial.print(") ");
  Serial.print(now.hour(), DEC);
  Serial.print(':');
  Serial.print(now.minute(), DEC);
  Serial.print(':');
  Serial.print(now.second(), DEC);
  Serial.println();

  if(now.minute()%3==0){
    Serial.println("Receiving data from children");
    LoRa_read_data(2);
    delay(3000);
    
  }
  else if(now.minute()%3==1){
    Serial.println("Receiving data from children");
    LoRa_read_data(3);
    delay(3000);
    
  }else{
    String data = "data:";
    data.concat(data0002);
    data.concat(data0003);
    Serial.println("Sending data to Raspberry pi");
    LoRa_write_string(data);
    delay(3000);
    
  }

}
