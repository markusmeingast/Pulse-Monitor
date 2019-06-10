/*
Testing reading raw analog data from sensor. Due to lack of pulse sensor at this time, accelerometer data MMA7361 is used.
 - Sampling rate set to 50Hz.
*/

//  INIT VARIABLES
unsigned long time;
const unsigned long PERIOD = 20000; // 20000us : 50Hz
static unsigned long lastRead;

//  SET UP LOOP
void setup() {
  Serial.begin(9600);
}

// RUN LOOP
void loop() {
  
  if (micros() - lastRead >= PERIOD) {
    //  may introduce small time errors, but should be within ~100us
    lastRead += PERIOD;

    // read the input on analog pin 0:
    int sensorValue = analogRead(A2);
    
    // print out time and value:
    time = micros();
    Serial.print(time);
    Serial.print(",");
    Serial.print(sensorValue);
    Serial.print("\n");
  }
  
}
