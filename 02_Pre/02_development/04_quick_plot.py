#!/home/markus/.pyenv/shims/python3

import pandas as pd
import glob
import sys
import matplotlib.pylab as mp

csvs = glob.glob('../03_samples/03_samples_peak_to_peak_streched/20191004-222339/*.csv')

data = pd.DataFrame()

for i in range(len(csvs)):
	data = data.append(pd.read_csv(csvs[i],header=None).T,ignore_index=True)

data.T.plot()
mp.show()


