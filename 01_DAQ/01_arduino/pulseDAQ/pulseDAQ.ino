/*
Testing reading raw analog data from sensor. Pulse sensor of type Joy-It (KY039HS) is used.
Set up:
 - white:  3.3V (better resposne than 5V)
 - gray:   GND
 - black:  SIG (A5)
 
Features: 
 - Sampling rate set to 200Hz.
 - Receive 'S' to start recording
 - Receive 'T' to stop recording
*/

//  INIT VARIABLES
unsigned long time_start;
const unsigned long period = 5000; // 5000us : 200Hz
static unsigned long last_read;
int keep_going = 0;
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
    // START RECORDING STATUS
    if (check_status == 'S') {
      //Serial.print("Starting\n");
      keep_going = 1;
      time_start = micros();
      last_read = micros();
    }
    // STOP RECORDING STATUS
    else if (check_status == 'T') {
      //Serial.print("Terminating\n");
      keep_going = 0;
    }
  }
    
  if (keep_going == 1) {
    if (micros() - last_read >= period) {
      //  may introduce small time errors, but should be within ~100us
      last_read += period;
  
      // read the input on analog pin 0:
      int sensorValue = analogRead(A5);
      
      // print out time and value:
      Serial.print(micros()-time_start-period);
      Serial.print(",");
      Serial.print(sensorValue);
      Serial.println("");
    }
  }
}
