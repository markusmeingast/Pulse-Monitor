# PULSE-MONITOR
Concept work for a heart beat monitor to determine intermittent arrhythmia. 

# Basic concept:
The idea of this project is to measure heart rythm by means of a IR based pulse sensor and determine arrythmia by comparison of prediction and true sinus rythm based on last few heart beats. 

A prediction model will be built using tensorflow RNN, e.g. LSTM cells, based on various length signal input to accurately capture varying bpms. The trained model should then be capable of using live measurement data to accurately predict a following heart beat.

The main challenges are the following:

 - [X] Data acquisition concept
 - [ ] Automatic data splitting into single or multiple beats
 - [ ] Model training in tensorflow
 - [ ] Model translation for live interpretation (e.g. tflite)

Currently three scenarios are envisioned.

 1. DAQ runs through a Arduino Nano, routing data by serial to Raspberry Pi for splitting, processing and storing.
 1. ~~DAQ runs directly through the Raspberry Pi by means of GPIO, effectively removing the Nano fromt he~~ chain.
 1. ~~DAQ and processing run through the Nano, with dedicated SD storage extension shield.~~

## Latest results

![Signal Example](signal_example.png "Signal Example")

## 01.06.2019
Starting basic setup work for Arduino **Nano** (C-Control compatible board) and Raspberry **Pi** 3 B+.
 - Added "blink" example as placeholder to Nano
 - Set up python 3.7.3 on Pi

## 10.06.2019
Set up basic serial communication between Arduino **Uno** (for testing/prototyping purposes) and Pi.
 - Restructured project folder
 - Using EZ1-Range Finder sensor for testing
 - Implemented try/catch on Pi side to limit communcation issues... further testing and development needed
 - Set sampling frequnecy to 50Hz

## 22.06.2019
Added KY039HS pulse sensor to replace EZ1. Additional code development.
 - Ramped sampling rate up tp 200Hz
 - Ramped up serial baud rate to 56.6k
 - Added initial plotting tool for saved test data
 - Added sensor documentation

## 02.07.2019
Added start/stop commands to UNO ("S" Start, "T" Terminate).
 - Switched to 3.3V supply on sensor. resolution seems far better.
 - Switched to Arduino IDE 1.8.9 for serial plotting support.

## 04.07.2019
Facing some issues getting the serial communication synced and without mistransmissions.
 - Play around with ser.flush(), time.sleep() and timeout settings.
 - Added shell script for removing old *.csv files
 - Saving files according to start date and time

## 08.07.2019
First 60min recording failed.
 - Added monitoring print out, and abort saving.

## 09.07.2019
Second attempt at reading 60min. Failed at around 2150s (from 3600s). Needs further debugging/file splitting.
 - Started development notebook.
 - Rolling mean (5-window) reduces noise significantly.
 - Peak finding can be tested on data set.

## 12.07.2019
Attached AD8232 ECG sensor as an alternative to KY039. 
 - Basic setup based on [Sparkfun guide](https://learn.sparkfun.com/tutorials/ad8232-heart-rate-monitor-hookup-guide/all)
 - Switched to 57600baud for consistency.
 - Reduced to 200Hz DAQ

## Open Topics / Concept issues
 - ~~Serial read frequency (DAQ and transfer should be min ~50Hz)~~
 - Unstable/nonrobust serial communication between Pi and Uno
 - Tensorflow lite model transfer (CPU/GPU --> ARM)
 - Sensor setup on PI/Nano
 - Beat splitting method
 - Buffering

## Software build versioning

### Raspberry Pi:
**system**
```
Raspberry Pi Model 3 B+
Raspbian GNU/Linux 9.9
Kernel 4.19.42-v7+
```

**python**
```
absl-py==0.7.1
astor==0.8.0
cycler==0.10.0
Cython==0.29.9
future==0.17.1
gast==0.2.2
grpcio==1.21.1
h5py==2.9.0
iso8601==0.1.12
joblib==0.13.2
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.0
kiwisolver==1.1.0
Markdown==3.1.1
matplotlib==3.1.0
mock==3.0.5
numpy==1.16.4
pandas==0.24.2
protobuf==3.8.0
pyparsing==2.4.0
pyserial==3.4
python-dateutil==2.8.0
pytz==2019.1
PyYAML==5.1.1
scikit-learn==0.21.2
scipy==1.3.0
serial==0.0.97
six==1.12.0
sklearn==0.0
tensorboard==1.13.1
tensorflow==1.13.1
tensorflow-estimator==1.13.0
termcolor==1.1.0
Werkzeug==0.15.4
```

### Arduino:
**system**
```
Arduino Uno R2
ATMega328P-PU
```

**system**
```
C-Control Nano
ATMega328
```

**Arduino  IDE**
```
2:1.0.5+dfsg2-4.1
1.8.9 local
```
