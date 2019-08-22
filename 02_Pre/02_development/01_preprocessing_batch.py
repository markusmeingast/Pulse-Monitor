#!/home/pi/Software/python3.7/bin/python3

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as mp
import peakutils as pu
from IPython.display import clear_output
import sys, os, glob

#raw_names = sorted(glob.glob("../01_raw/*.csv"))
raw_names = [
'../01_raw/20190822-092110.csv',
'../01_raw/20190822-093115.csv',
'../01_raw/20190822-094120.csv',
'../01_raw/20190822-095124.csv',
'../01_raw/20190822-100129.csv',
'../01_raw/20190822-101135.csv'
]

for k in range(0,len(raw_names)):
	fname = raw_names[k]
	dname = fname[10:25]
	print('Processing: '+fname)
	data = pd.read_csv('../01_raw/'+fname,header=None,names=['time','signal'])
	print('Length: '+str(len(data)))
	data['avg'] = data['signal'].rolling(4,center=True).mean()
	idx = pu.indexes(np.array(data['avg'].fillna(0)), thres=0.8, min_dist=50)
	print('Peaks: '+str(len(idx)))

	'''
	mp.plot(data['time'],data['avg'],label='Raw')
	mp.plot(data['time'].iloc[idx],data['avg'].iloc[idx],'rx')
	mp.plot([data['time'].iloc[idx[:-2]+120],data['time'].iloc[idx[:-2]+120]],[0,700],'b--')
	mp.plot([data['time'].iloc[idx[:-2]-60],data['time'].iloc[idx[:-2]-60]],[0,700],'g--')
	mp.legend()
	mp.axis([data['time'].iloc[14000],data['time'].iloc[15000],0,700])
	#mp.axis([160000,170000,0,700])
	'''

	os.system('mkdir ../03_samples/'+dname)

	for i in range(1,len(idx)-2):
		#clear_output()
		if i%10 == 0:
			print(str(i)+' of '+str(len(idx)))
		mp.clf()
		sample = data.iloc[idx[i]-60:idx[i]+120]
		outname = dname+'-{0:04d}'.format(i)+'.csv'
		sample.to_csv('../03_samples/'+dname+'/'+outname,header=False,index=False)
		mp.plot(sample["time"],sample["avg"])
		mp.savefig('../03_samples/'+dname+'/'+outname[:-3]+'png')

