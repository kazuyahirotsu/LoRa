#include <SoftwareSerial.h> // SoftwareSerialライブラリ
#include "RTClib.h"

#define UART_RX 17  // ES920LRの8ピン(TX)に接続します
#define UART_TX 16  // ES920LRの9ピン(RX)に接続します
#define LoRa_Rst 5 //  ES920LRの24ピン(RESETB)に接続します

SoftwareSerial LoRa_ss(UART_TX, UART_RX); // Private LoRa通信モジュールとのSoftwareSerialを定義します

RTC_DS1307 rtc;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
char* data0002;

// Private LoRa通信モジュールからのメッセージを受信します
void LoRa_read() {
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
  if (id == 2){
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
    data0002 = message;
  }else{
    Serial.print("No such id exists");
  }
}

// Private LoRa通信モジュールへメッセージを送信します
void LoRa_write(char msg[]) {
  LoRa_ss.write(msg);
  Serial.print("to   LoRa >>");
  Serial.print(msg);
  delay(500);
  LoRa_read();
}

void setup() {

  
  
  // コンピュータとの通信速度を定義します
  Serial.begin(9600);
  //Serial.begin(115200);
  while(!Serial){
    //wait till Serial
  }
  // SoftwareSerialでPrivate LoRa通信モジュールとの通信を定義します
  LoRa_ss.begin(9600);
  //LoRa_ss.begin(115200);
  
  Serial.println("Start!!");

  // ES920LRをコンフィグレーションモードに移行します
  LoRa_write("config\r\n");

  // Private LoRa通信モジュールをリセットするピンを定義します
  pinMode(LoRa_Rst , OUTPUT);
  delay(1000);
  digitalWrite(LoRa_Rst, HIGH);
  delay(1000);

  // Private LoRa通信モジュールを一度リセットします
  Serial.println("Reset");
  digitalWrite(LoRa_Rst, LOW);
  delay(1000);
  digitalWrite(LoRa_Rst, HIGH);
  delay(3000);

  // Private LoRa通信モジュールからのメッセージを受信します
  LoRa_read();

  // ES920LRのプロセッサーモードを選択します
  LoRa_write("processor\r\n");
  delay(1000);

  // ES920LRの設定を全て初期設定に戻す
  //LoRa_write("load\r\n");
//  delay(100);
  
  // 帯域幅を125kHzに設定します
  LoRa_write("baudrate 1\r\n");
  delay(100);
  
  // 帯域幅を125kHzに設定します
  LoRa_write("bw 4\r\n");
  delay(100);

  // 拡散率を7に設定します
  LoRa_write("sf 11\r\n");
  delay(100);

  // 無線チャンネル番号を1に設定します
  LoRa_write("channel 5\r\n");
  delay(100);

  // PANネットワークアドレスをABCDに設定します
  LoRa_write("panid 0001\r\n");
  delay(100);

  // 自ノードのネットワークアドレスを1000に設定します
  LoRa_write("ownid 0001\r\n");
  delay(100);

  // 送信先ノードのネットワークアドレスを0000に設定します
  LoRa_write("dstid FFFF\r\n");
  delay(100);

  // 設定した内容を内蔵FlashROMに保存します
  LoRa_write("save\r\n");
  delay(10000);

  // ES920LRをオペレーションモードに移行します
  LoRa_write("start\r\n");
  delay(1000);

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
  // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  // This line sets the RTC with an explicit date & time, for example to set
  // January 21, 2014 at 3am you would call:
  // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
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

  if(now.minute()%4==0){
    Serial.println("Receiving data from children");
    data0002 = {'\0'};
    LoRa_read_data(2);
    delay(3000);
    
  }else if(now.minute()%4==1){
    Serial.println("Buffer Time");
    delay(3000);
    
  }else if(now.minute()%4==2){
    Serial.println("Sending data to Raspberry pi");
    LoRa_write(data0002);
    delay(3000); 
    
  }else{
    Serial.println("Buffer Time");
    delay(3000);
    
  }
  if(now.minute()==2){
    Serial.println("Sending time to calibrate");
    char datetosend[16];
    itoa(now.unixtime(), datetosend, 10);
    strcat(datetosend, "\r\n");
    LoRa_write(datetosend);
    delay(3000);
  }

}
