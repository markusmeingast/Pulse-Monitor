#!/home/markus/.pyenv/shims/python3

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as mp
import peakutils as pu
from IPython.display import clear_output
import sys, os, glob
import scipy as sp
import scipy.interpolate as spi

raw_names = sorted(glob.glob("../01_raw/201912*.csv"))
#raw_names = ['../01_raw/20190821-202607.csv'
#'../01_raw/20190717-121646-millis.csv'
#'../01_raw/20190728-031008.csv']

for k in range(0,len(raw_names)):
	fname = raw_names[k]
	dname = fname[10:25]
	print('Processing: '+fname)
	data = pd.read_csv('../01_raw/'+fname,header=None,names=['time','signal'])
	print('Length: '+str(len(data)))
	data['avg'] = data['signal'].rolling(4,center=True).mean()
	idx = pu.indexes(np.array(data['avg'].fillna(0)), thres=0.8, min_dist=120)
	print('Peaks: '+str(len(idx)))

	os.system('mkdir ../03_samples/'+dname)

	for i in range(1,len(idx)-2):
	#for i in range(1,2):
		#clear_output()
		if i%10 == 0:
			print(str(i)+' of '+str(len(idx)))
		mp.clf()
		#sample = data.iloc[idx[i]-60:idx[i]+120]
		sample = data.iloc[idx[i]:idx[i+1]]
		f = spi.interp1d(np.linspace(0,200,len(sample)), sample["avg"].values, kind='linear')
		out = pd.DataFrame(f(np.linspace(0,199,200)))
		outname = dname+'-{0:04d}'.format(i)+'.csv'
		out.to_csv('../03_samples/'+dname+'/'+outname,header=False,index=False)
		mp.plot(out)
		mp.savefig('../03_samples/'+dname+'/'+outname[:-3]+'png')

