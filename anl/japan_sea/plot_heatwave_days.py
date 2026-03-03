#!/usr/bin/env python
"""海洋熱波発生日/年の時系列を描く

Usage: plot_heatwave_days.py

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
ncdir='nc/japansea_all/detrend'
#ncdir='nc/japansea_all'
da1=xr.open_dataset(ncdir+'/is_heatwave_ave_mgd.nc')['is_heatwave'].groupby('time.year').sum()
da2=xr.open_dataset(ncdir+'/is_heatwave_ave_him.nc')['is_heatwave'].groupby('time.year').sum()
da2=da2.isel(year=slice(0,7))
da3=xr.open_dataset(ncdir+'/is_heatwave_ave_movejpn.nc')['is_heatwave'].groupby('time.year').sum()
da4=xr.open_dataset(ncdir+'/is_heatwave_ave_jpnv2.nc')['is_heatwave'].groupby('time.year').sum()

year=da1['year'].values #np.append(da1['year'].values,2024)
d1=da1 #np.append(da1.values,0)
d2=np.append(np.zeros(36),da2.values[0:7])
d3=np.append(np.zeros(26),da4.values[0:12])
d3=np.append(d3,np.zeros(1))
d3=np.append(d3,da3.values[1:5])

#df=pd.DataFrame({'year':year,'MGDSST(1982-2024)':d1,'HIMSST(2018-2024)':d2,'MOVE-JPN(2008-2019,2021-2024)':d3})
#df=pd.DataFrame({'year':year,'MGDSST':d1,'HIMSST':d2.astype(np.int64)})

fig, ax = plt.subplots()
#df.plot(x='year',y='MGDSST',kind='bar',ax=ax)
#df.plot(x='year',y='HIMSST',kind='scatter',ax=ax)

plt.bar(year,d1,label='MGDSST')
plt.scatter(year[-7:],da2.values[0:7],label='HIMSST')

#da2.to_series().plot.bar(color='blue', label='MGDSST')
#da1.to_series().plot(kind='bar',color='red', label='HIMSST',ax=ax)
#da2.to_series().plot(kind='line',ax=ax.twinx()) #color='blue', label='MGDSST')


plt.legend()
#ax.set_title( 'Heatwave days'+region_name )
#ax.set_title( 'Marine Heatwave days (Japan Sea)' )
ax.set_title( 'Marine Heatwave days (detrended) (Japan Sea)' )
ax.set_xlabel('')
ax.set_ylabel('[days]',fontsize='large')
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.set_ylim((0,200))
plt.grid(axis='y')

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
