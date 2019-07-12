/*
Testing reading raw analog data from sensor. Pulse sensor of type Joy-It (KY039HS) is used.
Set up:
 - white:  3.3V (better resposne than 5V)
 - gray:   GND
 - black:  SIG (A5)
 
Features: 
 - Sampling rate set to 200Hz.
 - Receive 'R' to reset time
*/

//  INIT VARIABLES
unsigned long time_start;
const unsigned long period = 5000; // 5000us : 200Hz
unsigned long last_read;
char check_status;

//  SET UP LOOP
void setup() {
  Serial.begin(57600);
}

// RUN LOOP
void loop() {
  // CHECK FOR STATUS MESSAGE
  if (Serial.available()>0) {
    check_status = Serial.read();
    // Serial.println(check_status);
    // RESET TIME
    if (check_status == 'R') {
      //Serial.print("Resetting\n");
      time_start = micros();
      last_read = micros();
    }
  }

  if (micros() - last_read >= period) {
    //  may introduce small time errors, but should be within ~100us
    last_read += period;
  
    // read the input on analog pin 0:
    int sensorValue = analogRead(A5);
      
    // print out time and value:
    //Serial.print(micros()-time_start-period);
    //Serial.print(",");
    Serial.print(sensorValue);
    Serial.println("");
  }
}
