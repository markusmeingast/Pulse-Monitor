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
import sys, os

#####	Define and start serial communication
ser = serial.Serial('/dev/ttyACM0', 57600)


n_len = 4000
data = np.zeros((n_len,2),dtype=int)

ir = 0

ser.write(bytes('S', "utf8"))

#####	Main loop start
while True:
	#####	Implemented try/except to avoid read/write/measurement issues in serial
	try:
		#####	Grab time stamp from micros() and measured value
		time,value = ser.readline().decode().strip().split(",")
		time = int(time)
		value = int(value)
		data = np.roll(data,-1,axis=0)
		data[-1,0] = time
		data[-1,1] = value
		ir = ir+1
		if ir == n_len:
			ser.write(bytes('T',"utf8"))
			print('Saving')	
			np.savetxt('test.dat',data,fmt='%d',delimiter=',')
			print('Saved')
			sys.exit()
		#print(time,value)
		#print(data)
		#if ir%n_len == 0:
		#	mp.plot(data)
		#	mp.show()


	#####	Cancel loop by keyboard interrupt
	except KeyboardInterrupt:
		print("Stopping\n")
		exit()

	#####	Skip read if issues (may require fillers for further data processing)
	except:
		pass
