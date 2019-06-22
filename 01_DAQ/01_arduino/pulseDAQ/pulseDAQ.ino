/*
Testing reading raw analog data from sensor. Pulse sensor of type Joy-It (KY039HS) is used.
Set up:
 - white:   5V
 - gray:   GND
 - black:  SIG (A5)
 
Features: 
 - Sampling rate set to 100Hz.
*/

//  INIT VARIABLES
unsigned long time;
const unsigned long PERIOD = 5000; // 5000us : 200Hz
static unsigned long lastRead;

//  SET UP LOOP
void setup() {
  Serial.begin(56600);
}

// RUN LOOP
void loop() {
  
  if (micros() - lastRead >= PERIOD) {
    //  may introduce small time errors, but should be within ~100us
    lastRead += PERIOD;

    // read the input on analog pin 0:
    int sensorValue = analogRead(A5);
    
    // print out time and value:
    time = micros();
    Serial.print(time);
    Serial.print(",");
    Serial.print(sensorValue);
    Serial.print("\n");
  }
  
}
