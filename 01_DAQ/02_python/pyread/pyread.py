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
ser = serial.Serial('/dev/ttyACM0', 57600, timeout=0.2)

#####	Check if serial communcation is open
if ser.isOpen():
	print('Serial communication is up!')
else:
	print('Serial communication error: wrong port/baudrate?')

#####	Initialize empty array (rel. time, value)
n_len = 1000
data = np.zeros((n_len,2),dtype=int)

#####	Initialize file name for saving
fname = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

#####	Send start command to UNO
print('Start recording for '+fname+' for '+str(n_len/200)+'s or ~'+str(n_len)+'samples')
ser.write(bytes('S', "utf8"))
ser.flush()

#####	Main loop start
ir = 0
n_err = 0
while ir < n_len:
	#print(ir,n_err)
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

	#####	Cancel loop by keyboard interrupt
	except KeyboardInterrupt:
		print("Stopping due to user abort\n")
		ser.write(bytes('T',"utf8"))
		ser.close()
		exit()

	#####	Skip read if issues (may require fillers for further data processing)
	except:
		n_err = n_err+1
		pass


#####	Send terminate command to UNO
print('Terminate recording for '+fname+' with '+str(n_err)+' errors')
ser.write(bytes('T',"utf8"))
ser.close()

#####	Save to file
np.savetxt(fname+'.csv',data,fmt='%d',delimiter=',')
print('Saved '+fname+'.csv')
exit()



