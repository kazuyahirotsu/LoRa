#include <SoftwareSerial.h>
#include "RTClib.h"

#define UART_RX 17  // ES920LR 8(TX)
#define UART_TX 16  // ES920LR 9(RX)
#define LoRa_Rst 5 //  ES920LR 24(RESETB)

SoftwareSerial LoRa_ss(UART_TX, UART_RX);

RTC_DS1307 rtc;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
char* data0003;

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
  //read and rewrites the data to send for each child
  if (id == 3){
    char message[30] = {'\0'};
    if (LoRa_ss.available())Serial.print("from LoRa >>");
    int idx = 0;
    while (LoRa_ss.available()) {
      char c = {LoRa_ss.read()};
      Serial.print(c);
      message[idx] = c;
      idx += 1;
      //strcat(message, c);
      delay(1);
    }
    data0003 = message;
    Serial.print(data0003);
  }else{
    Serial.print("No such id exists");
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

void setup() {

//   // RTC setting up
//   if (! rtc.begin()) {
//     Serial.println("Couldn't find RTC");
//     Serial.flush();
//     while (1) delay(10);
//   }

//   if (! rtc.isrunning()) {
//     Serial.println("RTC is NOT running, let's set the time!");
//     // When time needs to be set on a new device, or after a power loss, the
//     // following line sets the RTC to the date & time this sketch was compiled
//     rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
//     // This line sets the RTC with an explicit date & time, for example to set
//     // January 21, 2014 at 3am you would call:
//     // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
//   }

//   // When time needs to be re-set on a previously configured device, the
//   // following line sets the RTC to the date & time this sketch was compiled
//   rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
//   // This line sets the RTC with an explicit date & time, for example to set
//   // January 21, 2014 at 3am you would call:
//   // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  
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
  LoRa_write("ownid 0003\r\n");
  delay(100);

  // destination network id (parent)
  LoRa_write("dstid 0001\r\n");
  delay(100);

  // save
  LoRa_write("save\r\n");
  delay(10000);

  // into operation mode
  LoRa_write("start\r\n");
  delay(1000);


}

void loop() {

//   DateTime now = rtc.now();

//   Serial.print(now.year(), DEC);
//   Serial.print('/');
//   Serial.print(now.month(), DEC);
//   Serial.print('/');
//   Serial.print(now.day(), DEC);
//   Serial.print(" (");
//   Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
//   Serial.print(") ");
//   Serial.print(now.hour(), DEC);
//   Serial.print(':');
//   Serial.print(now.minute(), DEC);
//   Serial.print(':');
//   Serial.print(now.second(), DEC);
//   Serial.println();

  if (LoRa_ss.available()){
    // get data from LoRa and parse it
    Serial.print("from LoRa >>");
    String data = LoRa_ss.readString();
    Serial.print(data);
    int index = split(data, ',', parsed_data);
    // send data if this edge is requested to send data
    if (parsed_data[0].equals("3")){
      Serial.println("It's my turn!!");
    //   char datetosend[16];
    //   itoa(now.unixtime(), datetosend, 10);
    //   strcat(datetosend, "\r\n");
    //   LoRa_write(datetosend);
      LoRa_write("dummy data\r\n");
    }else{
      Serial.println("Not my turn :(");
    }
  }
  delay(100);

}
