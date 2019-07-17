#!/home/pi/Software/python3.7/bin/python3

####################################################################################################
#
#	Python script to plot single data files acquired by pulseDAQ
#
####################################################################################################

#####	Import packages

import serial
import numpy as np
import matplotlib.pyplot as mp
import datetime
import sys, os
import pandas as pd

#####	Read data

data = pd.read_csv(sys.argv[1],header=None,names=['time','value'])

#data = np.loadtxt(sys.argv[1])

mp.plot(data['time']/1e3,data['value'])
mp.show()

