# pulse-monitor
Concept work for a heart beat monitor to determine intermittent arrhythmia. 

# Basic concept:
The idea of this project is to measure heart rythm by means of a IR based pulse sensor and determine arrythmia by comparison of prediction and true sinus rythm based on last few heart beats. 

A prediction model will be built using tensorflow RNN, e.g. LSTM cells, based on various length signal input to accurately capture varying bpms. The trained model should then be capable of using live measurement data to accurately predict a following heart beat.

The main challenges are the following:

 - [ ] Data acquisition concept
 - [ ] Automatic data splitting into single or multiple beats
 - [ ] Model training in tensorflow
 - [ ] Model translation for live interpretation (e.g. tflite)

Currently three scenarios are envisioned.

 1. DAQ runs through a Arduino Nano, routing data by serial to Raspberry Pi for splitting, processing and storing.
 1. DAQ runs directly through the Raspberry Pi by means of GPIO, effectively removing the Nano fromt he chain.
 1. DAQ and processing run through the Nano, with dedicated SD storage extension shield.

## 01.06.2019
Starting basic setup work for Arduino **Nano** (C-Control compatible board) and Raspberry **Pi** 3 B+.
 - Added "blink" example as placeholder to Nano
 - Set up python 3.7.3 on Pi

## Open Topics / Concept issues
 - Serial read frequency (DAQ and transfer should be min ~50Hz)
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
Cython==0.29.9
gast==0.2.2
grpcio==1.21.1
h5py==2.9.0
joblib==0.13.2
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.0
Markdown==3.1.1
mock==3.0.5
numpy==1.16.4
protobuf==3.8.0
scikit-learn==0.21.2
scipy==1.3.0
six==1.12.0
sklearn==0.0
tensorboard==1.13.1
tensorflow==1.13.1
tensorflow-estimator==1.13.0
termcolor==1.1.0
Werkzeug==0.15.4
```

### Arduino Nano:
**system**
```
C-Control Nano
ATMega328
```

**Arduino  IDE**
```
2:1.0.5+dfsg2-4.1
```
