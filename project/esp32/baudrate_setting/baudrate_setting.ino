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
  //Serial.begin(19200);
  //Serial.begin(115200);
  while(!Serial){
    //wait till Serial
  }
  // SoftwareSerialでPrivate LoRa通信モジュールとの通信を定義します
  LoRa_ss.begin(9600);
  //LoRa_ss.begin(19200);
  //LoRa_ss.begin(115200);
  
  Serial.println("Start!!");

  // ES920LRをコンフィグレーションモードに移行します
  LoRa_write("config\r\n");
  delay(1000);
  LoRa_write("config\r\n");
  delay(1000);
  LoRa_write("config\r\n");
  delay(1000);
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
  //delay(100);
  
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
  LoRa_write("ownid 7069\r\n");
  delay(100);

  // 送信先ノードのネットワークアドレスを0000に設定します
  LoRa_write("dstid 7068\r\n");
  delay(100);

  // 設定した内容を内蔵FlashROMに保存します
  LoRa_write("save\r\n");
  delay(10000);

  // ES920LRをオペレーションモードに移行します
  LoRa_write("start\r\n");
  delay(1000);
}

void loop() {
  LoRa_write("test\r\n");
  delay(3000);
}
