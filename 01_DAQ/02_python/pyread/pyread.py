#!/home/pi/Software/python3.7/bin/python3

####################################################################################################
#
#	Python script to interface with Arduino running pulseDAQ
#
####################################################################################################

#####	Import packages

import serial
import numpy as np
import matplotlib.pyplot as mp
import datetime

#####	Define and start serial communication
ser = serial.Serial('/dev/ttyACM0', 9600)

#####	Main loop start
while True:
	#####	Implemented try/except to avoid read/write/measurement issues in serial
	try:
		#####	Grab time stamp from micros() and measured value
		time,value = ser.readline().decode().strip().split(",")
		time = int(time)
		value = int(value)
		print(time,value)

	#####	Cancel loop by keyboard interrupt
	except KeyboardInterrupt:
		print("Stopping\n")
		exit()

	#####	Skip read if issues (may require fillers for further data processing)
	except:
		pass
