/* Example implementation of an alarm using DS3231
 *
 * VCC and GND of RTC should be connected to some power source
 * SDA, SCL of RTC should be connected to SDA, SCL of arduino
 * SQW should be connected to CLOCK_INTERRUPT_PIN
 * CLOCK_INTERRUPT_PIN needs to work with interrupts
 */

#include <RTClib.h>
// #include <Wire.h>

RTC_DS3231 rtc;

// the pin that is connected to SQW
#define CLOCK_INTERRUPT_PIN 4

RTC_DATA_ATTR int bootCount = 0;


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

void setup() {
    Serial.begin(9600);
    
    delay(1000); //Take some time to open up the Serial Monitor

    pinMode(13,OUTPUT);
    
    Serial.println("LOW");
    digitalWrite(13,LOW);
    delay(2500);
    
    Serial.println("HIGH");
    digitalWrite(13,HIGH);
    delay(2500);
    
    Serial.println("LOW");
    digitalWrite(13,LOW);
    delay(2500);
    
    
    //Increment boot number and print it every reboot
    ++bootCount;
    Serial.println("Boot number: " + String(bootCount));
  
    //Print the wakeup reason for ESP32
    print_wakeup_reason();

    // initializing the rtc
    if(!rtc.begin()) {
        Serial.println("Couldn't find RTC!");
        Serial.flush();
        while (1) delay(10);
    }

    if(rtc.lostPower()) {
        // this will adjust to the date and time at compilation
        rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    }

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
    DateTime wakeup_time = DateTime(now.year(), now.month(), now.day(), now.hour()+1, now.minute()+1, 0);
    Serial.print("alarm time: ");
    Serial.print(wakeup_time.year(), DEC);
    Serial.print('/');
    Serial.print(wakeup_time.month(), DEC);
    Serial.print('/');
    Serial.print(wakeup_time.day(), DEC);
    Serial.print(" ");
    Serial.print(wakeup_time.hour(), DEC);
    Serial.print(':');
    Serial.print(wakeup_time.minute(), DEC);
    Serial.print(':');
    Serial.print(wakeup_time.second(), DEC);
    Serial.println();
    
//    // schedule an alarm on *0 minute
//    if(!rtc.setAlarm1(
//            wakeup_time,
//            DS3231_A1_Minute // this mode triggers the alarm when the seconds match. See Doxygen for other options
//    )) {
//        Serial.println("Error, alarm wasn't set!");
//    }else {
//        Serial.println("Alarm set");
//    }
    
    // schedule an alarm 10 seconds in the future
    if(!rtc.setAlarm1(
            rtc.now() + TimeSpan(10),
            DS3231_A1_Second // this mode triggers the alarm when the seconds match. See Doxygen for other options
    )) {
        Serial.println("Error, alarm wasn't set!");
    }else {
        Serial.println("Alarm will happen in 10 seconds!");
    }

          /*
      First we configure the wake up source
      We set our ESP32 to wake up for an external trigger.
      There are two types for ESP32, ext0 and ext1 .
      ext0 uses RTC_IO to wakeup thus requires RTC peripherals
      to be on while ext1 uses RTC Controller so doesnt need
      peripherals to be powered on.
      Note that using internal pullups/pulldowns also requires
      RTC peripherals to be turned on.
      */
      esp_sleep_enable_ext0_wakeup(GPIO_NUM_4,0); //1 = High, 0 = Low
    
      //If you were to use ext1, you would use it like
      //esp_sleep_enable_ext1_wakeup(BUTTON_PIN_BITMASK,ESP_EXT1_WAKEUP_ANY_HIGH);
    
      //Go to sleep now
      Serial.println("Going to sleep now");
      esp_deep_sleep_start();
      // esp_light_sleep_start();
      Serial.println("This will never be printed");
}

void loop() {
//    // print current time
//    char date[10] = "hh:mm:ss";
//    rtc.now().toString(date);
//    Serial.print(date);
//
//    // the stored alarm value + mode
//    DateTime alarm1 = rtc.getAlarm1();
//    Ds3231Alarm1Mode alarm1mode = rtc.getAlarm1Mode();
//    char alarm1Date[12] = "DD hh:mm:ss";
//    alarm1.toString(alarm1Date);
//    Serial.print(" [Alarm1: ");
//    Serial.print(alarm1Date);
//    Serial.print(", Mode: ");
//    switch (alarm1mode) {
//      case DS3231_A1_PerSecond: Serial.print("PerSecond"); break;
//      case DS3231_A1_Second: Serial.print("Second"); break;
//      case DS3231_A1_Minute: Serial.print("Minute"); break;
//      case DS3231_A1_Hour: Serial.print("Hour"); break;
//      case DS3231_A1_Date: Serial.print("Date"); break;
//      case DS3231_A1_Day: Serial.print("Day"); break;
//    }
//
//    // the value at SQW-Pin (because of pullup 1 means no alarm)
//    Serial.print("] SQW: ");
//    Serial.print(digitalRead(CLOCK_INTERRUPT_PIN));
//
//    // whether a alarm fired
//    Serial.print(" Fired: ");
//    Serial.print(rtc.alarmFired(1));
//
//    // Serial.print(" Alarm2: ");
//    // Serial.println(rtc.alarmFired(2));
//    // control register values (see https://datasheets.maximintegrated.com/en/ds/DS3231.pdf page 13)
//    // Serial.print(" Control: 0b");
//    // Serial.println(read_i2c_register(DS3231_ADDRESS, DS3231_CONTROL), BIN);
//
//    // resetting SQW and alarm 1 flag
//    // using setAlarm1, the next alarm could now be configurated
//    if (rtc.alarmFired(1)) {
//        rtc.clearAlarm(1);
//        Serial.print(" - Alarm cleared");
//    }
//    Serial.println();
//
//    delay(2000);
}

void onAlarm() {
    Serial.println("Alarm occured!");
}
