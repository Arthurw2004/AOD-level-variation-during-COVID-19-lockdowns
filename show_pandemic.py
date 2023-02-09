import numpy as np
import numpy.ma as ma
import glob
from pyhdf.SD import SD, SDC
import matplotlib.pyplot as plt
import pandas as pd
import datetime 
import scipy.stats as sst
import math
import sys

city = sys.argv[1]
dateparse = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
aodRec = pd.read_csv(city+ 'AOD_pandemic_peroid.csv',parse_dates={'datetime': [0]},  date_parser=dateparse,index_col = 0, dtype= {'TimeDiff':np.float32, 'AOD':np.float32})

aodavg = pd.DataFrame()
aodavg['TimeDiff'] = aodRec.TimeDiff.resample('Y').mean()
aodavg['AOD'] = aodRec.AOD.resample('Y').mean()
aod2020 = pd.DataFrame()
aod2020 = aodavg[aodavg.index.year>=2015]
fig= plt.figure(figsize=(7, 6),dpi=200)
plt.rcParams['font.size'] = 18
#fig= plt.figure()
plt.plot(aod2020.index-1, aod2020['AOD'], color='black',lw=2.5)
plt.ylim([0.2, 1.0])
plt.xlabel('Year')
plt.ylabel('AOD')
#plt.title('Averaged AOD for pandemic lockdown period')
fig.tight_layout()
#plt.savefig(city+'monthlyAOD.png')
print(aod2020)

AODbenchmark = aod2020.drop(aod2020[aod2020.index.year>2019].index)
print(AODbenchmark)
pvalue = np.zeros((3))
mean = AODbenchmark.mean(axis=0, skipna = True)['AOD']
std = AODbenchmark.std(axis=0, skipna = True)['AOD']
#std = math.sqrt(AODbenchmark['AOD'].var())
z = sst.zscore(aod2020['AOD'])
print(z)
pvalue[0] = sst.norm.sf(abs(aod2020['AOD'][-3] - mean)/std)*2
pvalue[1] = sst.norm.sf(abs(aod2020['AOD'][-2] - mean)/std)*2
pvalue[2] = sst.norm.sf(abs(aod2020['AOD'][-1] - mean)/std)*2
pvalue[2] = sst.norm.sf(abs(aod2020['AOD'][-1] - mean)/std)*2
print(mean, std, aod2020['AOD'][-2], (aod2020['AOD'][-2]-mean)/mean, pvalue[-2],  aod2020['AOD'][-1], (aod2020['AOD'][-1]-mean)/mean, pvalue[-1] )
#print( (aod2020['AOD'][-2] - mean)/std, (aod2020['AOD'][-1] - mean)/std )
outfile = open('citystatistics5yr.txt', 'a')
outfile.write('%s, %f, %f, %f, %f, %f, %f, %f, %f\n' % (city, mean, std, aod2020['AOD'][-2], (aod2020['AOD'][-2]-mean)/mean, pvalue[-2],  aod2020['AOD'][-1], (aod2020['AOD'][-1]-mean)/mean, pvalue[-1]) )
outfile.close()
print(pvalue)
plt.plot(aod2020.index-1, np.full(7, mean),  '--', color='black')
plt.savefig(city+'AOD.pan.jpg')
plt.show()
