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

dateparse = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
city =sys.argv[1]
aodRec = pd.read_csv(city + 'AOD.csv',parse_dates={'datetime': [0]},  date_parser=dateparse,index_col = 0, dtype= {'TimeDiff':np.float32, 'AOD':np.float32})


monthnames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jly', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

aodavg = pd.DataFrame()
aodavg['TimeDiff'] = aodRec.TimeDiff.resample('M').median()
aodavg['AOD'] = aodRec.AOD.resample('M').median()
#print(aodavg)
aod2020 = pd.DataFrame()
aod2020 = aodavg[aodavg.index.year>=2010]
aod2020=aod2020.dropna()
print(aod2020)
fig= plt.figure(figsize=(7, 6),dpi=200)
plt.rcParams['font.size'] = 18
plt.plot(aod2020.index, aod2020['AOD'],color="black",lw=2.5)
plt.ylim([0, 2.0])
plt.xlabel('Year')
plt.ylabel('AOD')
#plt.title('Monthly AOD for 2010-2021')
fig.tight_layout()
plt.savefig(city+'monthlyAOD.jpg')
plt.show()

