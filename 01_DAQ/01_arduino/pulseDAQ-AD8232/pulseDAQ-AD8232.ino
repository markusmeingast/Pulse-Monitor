//####################################################################################################
//
//  Issues:
//    * no time stamp reset
//    * micros() rolls over at ~71min, millis() may not be accurate enough?
//    * implemented rollover check with switching to next_read, micros() should be fine for sample rate, and time stamp to be writen out as is, rollover possible.
//
//####################################################################################################

//  INCLUDE SPI AND DISPLAY DRIVER
#include <Adafruit_ST7735.h>
#include <SPI.h>

//  DEFINE PINS FOR HARDWARE SPI (11 AND 13 FOR MOSI AND SCLK)
#define RESET  8
#define DC     9
#define CS    10
Adafruit_ST7735 TFTscreen = Adafruit_ST7735(CS, DC, RESET);

//  DEFINE VARIABLES
unsigned long period = 5000;        // 5000us : 200Hz <-- for micros()
unsigned long next_read;            // next interval to read
unsigned long start;                // micros at start recording
unsigned long inc;
unsigned long micros_;              // micros value as variable
int signal_;                        // signal pulled from analogRead
int xpos = 2;                       // plotting position in x-value
int yold;                           // previous assigned y-value
char ser_read = 'S';                // serial read character for status LED

//  RUN SETUP
void setup() {
  //  INIT SCREEN
  TFTscreen.initR(INITR_BLACKTAB);
  TFTscreen.setRotation(3);
  TFTscreen.invertDisplay(1);
  TFTscreen.fillScreen(ST77XX_BLACK);
  TFTscreen.drawRect(1, 26 , 159, 80, ST77XX_WHITE);
  
  //  INIT LED FOR STATUS
  pinMode(7, OUTPUT);

  //  ADJUST NEXT READ AND START AFTER INIT
  next_read = micros();
  start = next_read;

  //  START SERIAL
  Serial.begin(57600);
}

//  RUN LOOP
void loop() {
  //  CHECK FOR SERIAL READ
  if (Serial.available()) {
    ser_read = Serial.read();
  }
  //  SET STATUS LED ACCORDING TO SERIAL READ
  if (ser_read == 'R') {
    digitalWrite(7, HIGH);
  }
  else if (ser_read == 'S') {
    digitalWrite(7, LOW);
  }

  //  GRAB CURRENT TIME
  micros_ = micros();
  
  //  CHECK IF NEXT READ IS SATISFIED (ROLLOVER POSSIBLE)
  if ((micros_ >= next_read) && (micros_-next_read < 2*period)) {
    //  CHECK IF LEAD-OFF DETECTED (UNUSED FOR NOW)
    //if((digitalRead(1) == 1)||(digitalRead(2) == 1)){
    //  Serial.println('!');
    //}

    //  GRAB ANALOG VALUE  
    signal_ = analogRead(A0);

    //  PRINT TIME AND SIGNAL TO SERIAL
    Serial.print(micros_-start);
    Serial.print(",");
    Serial.println(signal_);

    //  ASSIGN NEXT READ TIME
    next_read += period;

    //  PLOTTING TO TFT
    //  INTERPOLATE SIGNAL TO SCREEN
    int ypos = map(signal_,0,700,27,104);

    inc++;
    if (inc%2 == 0) {
      // ITERATE OVER SCREEN WIDTH
      if (xpos >= 158) {
        xpos = 2;
        TFTscreen.drawLine(xpos, 27, xpos, 104, ST77XX_BLACK);
      }
      else {
        TFTscreen.drawLine(xpos-1, ypos, xpos, yold, ST77XX_WHITE);
        TFTscreen.drawLine(xpos+1, 27, xpos+1, 104, ST77XX_BLACK);
        xpos++;
      }

      //  SET SIGNAL VALUE TO OLD FOR NEXT READ
      yold = ypos; 
    }
  }
}
