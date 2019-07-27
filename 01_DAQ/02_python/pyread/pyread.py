#!/home/pi/Software/python3.7/bin/python3

####################################################################################################
#
#	Python script to interface with Arduino running pulseDAQ
#	Assuming 200Hz sampling frequency
#	Running at 57600 baud/s
#	Recording n intervals of 10min (command specified)
#	Arduino reset (i.e. micros() close to 0) for each interval
#
####################################################################################################

#####	Import packages
import serial
import numpy as np
import matplotlib.pyplot as mp
import datetime
import sys, os
import time

#####	Check if call is correct
if len(sys.argv)<2:
	print('Call with: pyread.py <intervals of 10min>')
	exit()

#####	Start setup time
print('5min to set up, starting now')
time.sleep(300)

#####	Define and start serial communication
try:
	#####	57600 baud should be sufficient
	#####	timeout at 0.2s should be enough to capture 200Hz signal while not hanging too long on serial errors.
	ser = serial.Serial('/dev/ttyACM0', 57600, timeout=0.2)
except:
	print('Please check the port.')

#####	Check if serial communcation is open
if ser.isOpen():
	print('Serial communication is up!')
else:
	print('Serial communication error: wrong port/baudrate?')
	exit()

#####	Start loop over user defined number of intervals at call
for tt in range(0,int(sys.argv[1])):

	#####	Initialize empty array (rel. time, value)
	##### 	1200k samples at 200Hz = 10min
	n_len = 120000
	data = np.zeros((n_len,2),dtype=int)

	#####	Initialize file name for saving
	fname = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

	#####	Send start command to UNO
	print('Start recording for '+fname+' for ~'+str(n_len/200)+'s or '+str(n_len)+'samples')

	#####	Reset arduino by DTR pin
	ser.setDTR(False)
	time.sleep(0.022) # <-- supposedly what the UI does, seems to work
	ser.flushInput()
	ser.setDTR(True)

	#####	Skip first 5 (empty) rows
	for i in range(0,5):
		ser.readline()

	#####	Set LED status to recording
	time.sleep(0.2)
	ser.write(bytes('R','utf-8'))

	#####	Start reading/decoding/writing to file
	ir = 0
	n_err = 0
	while ir < n_len:
		#####	Implemented try/except to avoid read/write/measurement issues in serial
		try:
			#####	Grab time stamp from micros() and measured value
			t,value = ser.readline().decode().strip().split(",")
			t = int(t)
			value = int(value)
			data[ir,0] = t
			data[ir,1] = value
			ir = ir+1
			if ir%1000==0:
				print(str(ir)+' samples taken with '+str(n_err)+' errors')

		#####	Cancel loop by keyboard interrupt
		except KeyboardInterrupt:
			print("Stopping due to user abort\n")
			ser.write(bytes('S','utf-8'))
			ser.close()
			np.savetxt('abort.csv',data,fmt='%d',delimiter=',')
			print('Saved abort.csv after '+str(ir)+' steps')
			exit()

		#####	Skip read if issues (may require fillers for further data processing)
		except:
			n_err = n_err+1
			if n_err%20==0:
				print('Significant number of errors:'+str(n_err))

			if n_err>1000:
				print('Aborting due to too many errors')
				ser.write(bytes('S','utf-8'))
				exit()

			pass


	#####	Send terminate command to UNO
	print('Terminate recording for '+fname+' with '+str(n_err)+' errors')
	ser.write(bytes('S','utf-8'))

	#####	Save to file
	np.savetxt(fname+'.csv',data,fmt='%d',delimiter=',')
	print('Saved '+fname+'.csv')

#####	Close serial and exit
ser.write(bytes('S','utf-8'))
ser.close()
exit()

