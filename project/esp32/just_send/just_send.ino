#include <SoftwareSerial.h> // SoftwareSerialライブラリ

#define UART_RX 17  // ES920LRの8ピン(TX)に接続します
#define UART_TX 16  // ES920LRの9ピン(RX)に接続します
#define LoRa_Rst 5 //  ES920LRの24ピン(RESETB)に接続します

SoftwareSerial LoRa_ss(UART_TX, UART_RX); // Private LoRa通信モジュールとのSoftwareSerialを定義します

char message;

// Private LoRa通信モジュールからのメッセージを受信します
void LoRa_read() {
  //if (LoRa_ss.available())Serial.print("from LoRa >>");
  LoRa_ss.listen();
  
  while (LoRa_ss.available() > 0) {
    message = (char)LoRa_ss.read();
    //if (message < 0x80)Serial.write(message);
    //Serial.write(message);
    Serial.print(message);
  }
  Serial.println(message);
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

  while(!Serial){
    //wait till Serial
  }
  // SoftwareSerialでPrivate LoRa通信モジュールとの通信を定義します
  LoRa_ss.begin(9600);
  
  Serial.println("Start!!");

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
  delay(1000);

  // Private LoRa通信モジュールからのメッセージを受信します
  LoRa_read();

  // ES920LRのプロセッサーモードを選択します
  LoRa_write("processor\r\n");
  delay(1000);

}

void loop() {
  LoRa_write("test\r\n");
  delay(3000);
}
