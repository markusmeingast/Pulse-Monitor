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

#raw_names = sorted(glob.glob("../01_raw/*.csv"))
raw_names = [
#'../01_raw/20190821-202607.csv'
#'../01_raw/20190717-121646-millis.csv'
#'../01_raw/20190728-031008.csv'
'../01_raw/20191011-211152.csv',
'../01_raw/20191011-212200.csv',
'../01_raw/20191011-213207.csv',
'../01_raw/20191011-220154.csv',
'../01_raw/20191011-221202.csv',
'../01_raw/20191011-222209.csv',
'../01_raw/20191011-223216.csv',
'../01_raw/20191011-224223.csv',
'../01_raw/20191011-225230.csv',
'../01_raw/20191011-230814.csv',
'../01_raw/20191011-231821.csv',
'../01_raw/20191011-234821.csv',
'../01_raw/20191011-235828.csv',
'../01_raw/20191012-000835.csv',
'../01_raw/20191012-001842.csv',
'../01_raw/20191012-002849.csv',
'../01_raw/20191012-003856.csv',
'../01_raw/20191012-004903.csv',
'../01_raw/20191012-005910.csv',
'../01_raw/20191012-010917.csv',
'../01_raw/20191012-011924.csv',
'../01_raw/20191012-012930.csv',
'../01_raw/20191012-013937.csv',
'../01_raw/20191012-014944.csv',
'../01_raw/20191012-015951.csv',
'../01_raw/20191012-020958.csv',
'../01_raw/20191012-022005.csv',
'../01_raw/20191012-023011.csv',
'../01_raw/20191012-024018.csv',
'../01_raw/20191012-025025.csv',
'../01_raw/20191012-030032.csv',
'../01_raw/20191012-031039.csv',
'../01_raw/20191012-032046.csv',
'../01_raw/20191012-033053.csv',
'../01_raw/20191012-034100.csv',
'../01_raw/20191012-035107.csv',
'../01_raw/20191012-040114.csv',
'../01_raw/20191012-041121.csv',
'../01_raw/20191012-042128.csv',
'../01_raw/20191012-043135.csv',
'../01_raw/20191012-044142.csv',
'../01_raw/20191012-045149.csv',
'../01_raw/20191012-050155.csv',
'../01_raw/20191012-051202.csv',
'../01_raw/20191012-052209.csv',
'../01_raw/20191012-053216.csv',
'../01_raw/20191012-054223.csv',
'../01_raw/20191012-055230.csv',
'../01_raw/20191012-060237.csv',
'../01_raw/20191012-061243.csv',
'../01_raw/20191012-062250.csv',
'../01_raw/20191012-063257.csv',
'../01_raw/20191012-064304.csv',
'../01_raw/20191012-065311.csv',
'../01_raw/20191012-070318.csv',
'../01_raw/20191012-071325.csv',
'../01_raw/20191012-072332.csv',
'../01_raw/20191012-073339.csv',
'../01_raw/20191012-074345.csv'
]

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

