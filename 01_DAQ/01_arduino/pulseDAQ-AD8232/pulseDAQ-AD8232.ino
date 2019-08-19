//####################################################################################################
//
//  Issues:
//    * no time stamp reset
//    * micros() rolls over at ~71min, millis() may not be accurate enough?
//    * implemented rollover check with switching to next_read, micros() should be fine for sample rate, and time stamp to be writen out as is, rollover possible.
//
//####################################################################################################

#include <Adafruit_ST7735.h>
#include <SPI.h>

#define CS     10
#define DC      9
#define RESET   8 
Adafruit_ST7735 TFTscreen = Adafruit_ST7735(CS, DC, RESET);

unsigned long period = 5000; // 5000us : 200Hz <-- for micros()
//const unsigned long period = 5; // 5ms : 200Hz <-- for millis()
unsigned long next_read;
unsigned long start;
unsigned long micros_;
int signal_;
int xpos = 2;
int yold;
char ser_read = 'S';

void setup() {
  Serial.begin(57600);
//  TFTscreen.begin();
  TFTscreen.initR(INITR_BLACKTAB);
  TFTscreen.setRotation(3);
  TFTscreen.invertDisplay(1);
  TFTscreen.fillScreen(ST77XX_BLACK);
  TFTscreen.drawRect(1, 26 , 159, 80, ST77XX_WHITE);
  pinMode(7, OUTPUT);
  next_read = micros();
  start = next_read;
}

void loop() {
  if (Serial.available()) {
    ser_read = Serial.read();
  }
  if (ser_read == 'R') {
    digitalWrite(7, HIGH);
  }
  else if (ser_read == 'S') {
    digitalWrite(7, LOW);
  }

  micros_ = micros();
  if ((micros_ >= next_read) && (micros_-next_read < 2*period)) {
    //if((digitalRead(1) == 1)||(digitalRead(2) == 1)){
    //  Serial.println('!');
    //}
    signal_ = analogRead(A0);
    Serial.print(micros_-start);
    Serial.print(",");
    Serial.println(signal_);
    next_read += period;
    
    int ypos = map(signal_,100,700,27,104);
    if (xpos >= 158) {
      xpos = 2;
      TFTscreen.drawLine(xpos, 27, xpos, 104, ST77XX_BLACK);
    }
    else {
      TFTscreen.drawLine(xpos-1, ypos, xpos, yold, ST77XX_WHITE);
      TFTscreen.drawLine(xpos+1, 27, xpos+1, 104, ST77XX_BLACK);
      xpos++;
    }
    yold = ypos; 
  }
}

///******************************************************************************
//Heart_Rate_Display.ino
//Demo Program for AD8232 Heart Rate sensor.
//Casey Kuhns @ SparkFun Electronics
//6/27/2014
//https://github.com/sparkfun/AD8232_Heart_Rate_Monitor
//
//The AD8232 Heart Rate sensor is a low cost EKG/ECG sensor.  This example shows
//how to create an ECG with real time display.  The display is using Processing.
//This sketch is based heavily on the Graphing Tutorial provided in the Arduino
//IDE. http://www.arduino.cc/en/Tutorial/Graph
//
//Resources:
//This program requires a Processing sketch to view the data in real time.
//
//Development environment specifics:
//  IDE: Arduino 1.0.5
//  Hardware Platform: Arduino Pro 3.3V/8MHz
//  AD8232 Heart Monitor Version: 1.0
//
//This code is beerware. If you see me (or any other SparkFun employee) at the
//local pub, and you've found our code helpful, please buy us a round!
//
//Distributed as-is; no warranty is given.
//******************************************************************************/
//
////  INIT VARIABLES
//unsigned long time_start;
//const unsigned long period = 5000; // 5000us : 200Hz
//unsigned long last_read;
//char check_status;
//unsigned int go = 0;
//
//void setup() {
//  // initialize the serial communication:
//  Serial.begin(57600);
//  pinMode(10, INPUT); // Setup for leads off detection LO +
//  pinMode(11, INPUT); // Setup for leads off detection LO -
//}
//
//void loop() {
//
////  // CHECK FOR STATUS MESSAGE
////  if (Serial.available()>0) {
////    check_status = Serial.read();
////    // Serial.println(check_status);
////    // RESET TIME
////    if (check_status == 'R') {
////      //Serial.print("Resetting and clearing serial buffer\n");
////      delay(1000);
////      Serial.flush();
////      go = 1;
////      Serial.println("R");
////      time_start = micros();
////      last_read = micros();
////    }
////  }
//
////  if (go==1){
//    //if((digitalRead(10) == 1)||(digitalRead(11) == 1)){
//    //  Serial.println('!');
//    //}
//    //else{
//    if (micros() - last_read >= period) {
//      last_read += period;
//      // send the value of analog input 0:
//      // Serial.println(analogRead(A0));
//      // print out time and value:
////      Serial.print(micros()-time_start-period);
////      Serial.print(",");
//      Serial.print(analogRead(A0));
//      Serial.println("");
//    }
//    //}
//    //Wait for a bit to keep serial data from saturating
//    //delay(1);
////  }
//}
