#!/home/pi/Software/python3.7/bin/python3

####################################################################################################
#
#	Python script to interface with Arduino running pulseDAQ
#	Assuming 200Hz sampling frequency
#
####################################################################################################

#####	Import packages

import serial
import numpy as np
import matplotlib.pyplot as mp
import datetime
import sys, os
import time

#####	Define and start serial communication
try:
	ser = serial.Serial('/dev/ttyACM0', 57600, timeout=0.2)
	time.sleep(0.1)
except:
	print('Please check the port.')

#####	Check if serial communcation is open
if ser.isOpen():
	print('Serial communication is up!')
else:
	print('Serial communication error: wrong port/baudrate?')
	exit()

#####	SETUP TIME
print('5min to set up, staring now')
time.sleep(300)

#####	START LOOP OVER MULTIPLE INTERVALS
for tt in range(0,6):

	#####	Initialize empty array (rel. time, value)
	n_len = 120000
	data = np.zeros((n_len,2),dtype=int)

	#####	Initialize file name for saving
	fname = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

	#####	Send start command to UNO
	print('Start recording for '+fname+' for ~'+str(n_len/200)+'s or '+str(n_len)+'samples')
	ser.flushOutput()
	ser.write(bytes('R','utf-8'))
	ser.flushInput()

	#####	Main loop start
	#####	Skip first 20 reads
	ir = 0
	while ir < 20:
		ser.readline()
		ir = ir+1

	#####	Start reading/decoding/writing to file
	ir = 0
	n_err = 0
	while ir < n_len:
		#print(ir,n_err)
		#####	Implemented try/except to avoid read/write/measurement issues in serial
		try:
			#####	Grab time stamp from micros() and measured value
			t,value = ser.readline().decode().strip().split(",")
			t = int(t)
			value = int(value)
			#data = np.roll(data,-1,axis=0)   <-- way too slow
			data[ir,0] = t
			data[ir,1] = value
			ir = ir+1
			if ir%1000==0:
				print(str(ir)+' samples taken with '+str(n_err)+' errors')

		#####	Cancel loop by keyboard interrupt
		except KeyboardInterrupt:
			print("Stopping due to user abort\n")
			ser.close()
			np.savetxt('abort.csv',data,fmt='%d',delimiter=',')
			print('Saved abort.csv after '+str(ir)+' steps')
			exit()

		#####	Skip read if issues (may require fillers for further data processing)
		except:
			n_err = n_err+1
			if n_err%20==0:
				print('Significant number of errors:'+str(n_err))
			pass


	#####	Send terminate command to UNO
	print('Terminate recording for '+fname+' with '+str(n_err)+' errors')

	#####	Save to file
	np.savetxt(fname+'.csv',data,fmt='%d',delimiter=',')
	print('Saved '+fname+'.csv')

ser.close()
exit()

