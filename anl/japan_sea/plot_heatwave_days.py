#!/usr/bin/env python
"""SST水平平均値と海洋熱波発生の時系列を描く

Usage: plot_heatwave_multiyear.py

"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import cm
import logging
import pandas as pd
import matplotlib.dates as mdates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

#region_name='Japan Sea (North)'
#ncdir='nc/japansea_north'
#region_name='Japan Sea (South)'
#ncdir='nc/japansea_south'
region_name='Japan Sea (All)'
ncdir='nc/japansea_all'
da1=xr.open_dataset(ncdir+'/is_heatwave_ave_mgd.nc')['is_heatwave'].groupby('time.year').sum()
da2=xr.open_dataset(ncdir+'/is_heatwave_ave_him.nc')['is_heatwave'].groupby('time.year').sum()
da3=xr.open_dataset(ncdir+'/is_heatwave_ave_movejpn.nc')['is_heatwave'].groupby('time.year').sum()
da4=xr.open_dataset(ncdir+'/is_heatwave_ave_jpnv2.nc')['is_heatwave'].groupby('time.year').sum()

year=np.append(da1['year'].values,2024)
d1=np.append(da1.values,0)
d2=np.append(np.zeros(36),da2.values[0:7])
d3=np.append(np.zeros(26),da4.values[0:12])
d3=np.append(d3,np.zeros(1))
d3=np.append(d3,da3.values[1:5])

df=pd.DataFrame({'year':year,'MGDSST(1982-2023)':d1,'HIMSST(2018-2024)':d2,'MOVE-JPN(2008-2019,2021-2024)':d3})

fig, ax = plt.subplots()
df.plot.bar(x='year')

#da2.to_series().plot.bar(color='blue', label='MGDSST')
#da1.to_series().plot.bar(color='red', label='HIMSST')



plt.legend()
ax.set_title( 'SST w/ Heatwave '+region_name )
ax.set_xlabel('')
#ax.set_ylabel('C')
#ax.set_xlim(pd.to_datetime('2022-01-01'),pd.to_datetime('2024-12-31'))

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
