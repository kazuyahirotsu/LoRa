#include <SoftwareSerial.h>
#include "RTClib.h"

#define UART_RX 16  // ES920LR 8(TX)
#define UART_TX 17  // ES920LR 9(RX)
#define LoRa_Rst 5 //  ES920LR 24(RESETB)
#define TEMP 32

const float ANALOG_MAX = 4096;

SoftwareSerial LoRa_ss(UART_RX, UART_TX);
SoftwareSerial do_ss(19, 18);
SoftwareSerial do_ss2(26, 25);

RTC_DS1307 rtc;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
String data0001;
String data0002;
String data0003;

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

void LoRa_read_data(int id) {
  // if there is another broadcast, this need to change since serial buffer will contain data that this edge didn't request
  // for example if there is unexpected data between (reading after sending to raspberry pi) and (sending to 0002), the first readStringUntil('\n') will be the unexpected data
  // it might be a good idea to clean it every loop
  // read message and update the data to send 
  if (id == 2){
    if (LoRa_ss.available())Serial.print("from LoRa >>");
    if (LoRa_ss.available()) {
      String ok = LoRa_ss.readStringUntil('\n');
      Serial.print(ok);
      data0002 = LoRa_ss.readStringUntil('\n');
      Serial.print(data0002);
    }
  }
  else if (id == 3){
    if (LoRa_ss.available())Serial.print("from LoRa >>");
    if (LoRa_ss.available()) {
      String ok = LoRa_ss.readStringUntil('\n');
      Serial.print(ok);
      data0003 = LoRa_ss.readStringUntil('\n');
      Serial.print(data0003);
    }
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
          if(received_message_num == 1){
              received_message_num = 0;
              waiting_for_respond = false;
          }
          delay(100);
      }
}

void do_send2(String msg, boolean sensor_data){
      do_ss2.print(msg);
      Serial.println("send: "+msg);
      waiting_for_respond = true;

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
          if(received_message_num == 1){
              received_message_num = 0;
              waiting_for_respond = false;
          }
          delay(100);
      }
}

void change_config(String dstid) {
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
  delay(100);

  // // default config
  // LoRa_write("load\r\n");
  // delay(100);
  
  // // baudrate 9600
  // LoRa_write("baudrate 1\r\n");
  // delay(100);
  
  // // 125kHz
  // LoRa_write("bw 4\r\n");
  // delay(100);

  // // spreading factor 11
  // LoRa_write("sf 11\r\n");
  // delay(100);

  // // channel 5
  // LoRa_write("channel 5\r\n");
  // delay(100);

  // // PAN
  // LoRa_write("panid 0001\r\n");
  // delay(100);

  // // own network id
  // LoRa_write("ownid 0001\r\n");
  // delay(100);

  // destination network id (broadcast)
  LoRa_write_string("dstid "+ dstid);
  delay(500);
  LoRa_read();
  delay(100);

  // save
  LoRa_write("save\r\n");
  delay(100);

  // into operation mode
  LoRa_write("start\r\n");
  delay(100);

}

void setup() {
  // DO setup
  do_ss.begin(9600);                                //set baud rate for software serial port_3 to 9600
  while(!do_ss){
    //wait till Serial
  }
  sensorstring.reserve(30);                           //set aside some bytes for receiving data from Atlas Scientific product
  do_send("sleep\r", false);

  do_ss2.begin(9600);                                //set baud rate for software serial port_3 to 9600
  while(!do_ss2){
    //wait till Serial
  }
  sensorstring2.reserve(30);                           //set aside some bytes for receiving data from Atlas Scientific product
  do_send2("sleep\r", false);

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
  while(!LoRa_ss){
    //wait till Serial
  }
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

  // destination network id (parent)
  LoRa_write("dstid FFFF\r\n");
  delay(100);

  // retry num
  LoRa_write("retry 0\r\n");
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

    // get my data
    Serial.println(now.minute(), DEC);
    Serial.println("It's my turn!!");

    do_send("wakeup\r", false);
    do_send("r\r", true);
    do_send("sleep\r", false);

    do_send2("wakeup\r", false);
    do_send2("r\r", true);
    do_send2("sleep\r", false);

    float reading = analogRead(TEMP);
    Serial.println(reading);
    float voltage = (reading*3.3)/ANALOG_MAX;
    Serial.println(voltage);
    String temp = String((voltage-1.058)/0.009);
    Serial.println((voltage-1.058)/0.009);
    Serial.println(temp);

    // LoRa_write_string(sensorstring+", "+sensorstring2+", "+temp);
    data0001 = "0001,"+sensorstring+","+sensorstring2+","+temp;
    // delay(500);
    // LoRa_read();

    // clear the buffer
    while(LoRa_ss.available())LoRa_ss.read();

    for(int i=2;i<4;i++){
        // change destination id
        change_config("000"+String(i));
        // using delayed date
        // send calibration date and the edge id to request data to
        String i_string = String(i);

        char datetosend[16];
        itoa(rtc.now().unixtime(), datetosend, 10);

        String custom_data = i_string + "," + datetosend;
        LoRa_write_string(custom_data);
        delay(10000);

        // read data from edge i
        LoRa_read_data(i);
        delay(5000);
    }
  
//    String data = "";
//    data.concat(data0001);
//    data.concat(",");
//    data.concat(data0002);
//    data.concat(",");
//    data.concat(data0003);
//    change_config("7068");
//    Serial.println("Sending data to Raspberry pi");
//    LoRa_write_string(data);
//    delay(1000);
//    LoRa_read();
//    delay(3000);
    
    change_config("7068");
    Serial.println("Sending data to Raspberry pi");
    if(!data0001.equals("")){
      LoRa_write_string(data0001);
      delay(3000);
      LoRa_read();
    }
    if(!data0002.equals("")){
      LoRa_write_string(data0002);
      delay(3000);
      LoRa_read();
    }
    if(!data0003.equals("")){
      LoRa_write_string(data0003);
      delay(3000);
      LoRa_read();
    }

    data0001 = "";
    data0002 = "";
    data0003 = "";

    // now_minute = now.minute();

    // if(now_minute!=before_minute){
    //     Serial.println(now.minute(), DEC);
    //     Serial.println("It's my turn!!");

    //     do_send("wakeup\r", false);
    //     do_send("r\r", true);
    //     do_send("sleep\r", false);

    //     do_send2("wakeup\r", false);
    //     do_send2("r\r", true);
    //     do_send2("sleep\r", false);

    //     LoRa_write_string(sensorstring+", "+sensorstring2);
    //     delay(500);
    //     LoRa_read();
    // }

    // before_minute = now.minute();

//   if (LoRa_ss.available()){
//     DateTime now = rtc.now();
//     // Serial.print(now.year(), DEC);
//     // Serial.print('/');
//     // Serial.print(now.month(), DEC);
//     // Serial.print('/');
//     // Serial.print(now.day(), DEC);
//     // Serial.print(" (");
//     // Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
//     // Serial.print(") ");
//     // Serial.print(now.hour(), DEC);
//     // Serial.print(':');
//     // Serial.print(now.minute(), DEC);
//     // Serial.print(':');
//     // Serial.print(now.second(), DEC);
//     // Serial.println();
    
    
//     // get data from LoRa and parse it
//     Serial.print("from LoRa >>");
//     String data = LoRa_ss.readString();
//     Serial.print(data);
//     int index = split(data, ',', parsed_data);
//     // send data if this edge is requested to send data
//     if (parsed_data[0].equals("2")){
//       Serial.println("It's my turn!!");

//       do_send("wakeup\r", false);
//       do_send("r\r", true);
//       do_send("sleep\r", false);

//       LoRa_write_string(sensorstring);
//     }else{
//       Serial.println("Not my turn :(");
//     }
//     // if (parsed_data[0].equals("2")){
//     //   Serial.println("It's my turn!!");
//     //   char datetosend[16];
//     //   itoa(now.unixtime(), datetosend, 10);
//     //   strcat(datetosend, "\r\n");
//     //   LoRa_write(datetosend);
//     // }else{
//     //   Serial.println("Not my turn :(");
//     // }
//   }
  delay(100);

}
