# How to use
# pip install pyserial
#
# シリアルポートの番号を引数に追加して実行する
# py GPS_recieve.py COM1
#
# GPSはNMEAフォーマットで送出される．
#  GPRMC（データタイプ），UTC（hhmmss.ss），V（警告）A（有効），緯度(lat)(ddmm.mmmm)，北緯or南緯，経度(lon)(dddmm.mmmm)，東経or西経，移動速度(kt)，真方位，UTCでの日付(ddmmyy)，磁北と真方位の差，差の方向，モード（N：データなし，A：自立方向，D干渉測位方式，E：推定），チェックサム
# https://www.hiramine.com/physicalcomputing/general/gps_nmeaformat.html

import sys
import serial

args = sys.argv

ser = serial.Serial(args[1],9600);      # Serial(PORT, ボーレート) ボーレートは9600 or 57600

while True:
    line = ser.readline()           # binaryデータでlineに格納される
    splited_line = line.decode().split(",")
    if splited_line[0] == "$GNGGA":
        hour =int((splited_line[1])[:2]) + 9    # 時（UTCに+9時間足すことで，JSTに変換している）
        minute = int((splited_line[1])[2:4])    # 分
        second = float((splited_line[1])[4:])   # 秒

        status = splited_line[6]        # Aなら受信している．Nなら受信していない
        if status == "0":
            print("gps not fix")
        elif status == "1":
            print("gps fix")
        elif status == "2":
            print("dgps fix")
            print(splited_line[7]+"satelites found")
            lat = float((splited_line[2])[:2]) + float((splited_line[2])[2:])/60.0
            lon = float((splited_line[4])[:3]) + float((splited_line[4])[3:])/60.0
            print(str(lat) + "," + splited_line[3] + "," + str(lon) + "," + splited_line[5])
        else:
            print("status: "+status)

ser.close()
