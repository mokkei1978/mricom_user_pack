#!/usr/bin/env python
"""SST水平平均値と海洋熱波発生の時系列を描く

Usage: plot_heatwave_multiyear.py

"""

import sys
sys.path.append('.')

import xarray as xr
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
date_first='2018-01-01'
date_last='2024-12-31'
da=xr.open_dataset(ncdir+'/sst_ave_him.nc')['thetao'].sel(time=slice(date_first,date_last))
dh=xr.open_dataset(ncdir+'/is_heatwave_ave_him.nc')['is_heatwave'].sel(time=slice(date_first,date_last))
dh2=xr.open_dataset(ncdir+'/is_heatwave_ave_him-detrend.nc')['is_heatwave'].sel(time=slice(date_first,date_last))

dnorml=xr.open_dataset(ncdir+'/sst_ave_norm.nc')['thetao']
dnormn=dnorml.drop_sel(time='2004-02-29').copy()
dnorm=xr.concat([dnormn,dnormn,dnorml,dnormn,dnormn,dnormn,dnorml],dim='time')
dnorm["time"]=pd.date_range(start=date_first,end=date_last)

fig, ax = plt.subplots()

da.plot.line(color='red', label='HIMSST')

is_now = False
h1_first = []
h1_last = []
for i in range(dh.shape[0]-1):
    if is_now == dh[i]:
        continue
    if is_now :
        h1_first.append(i)
    else :
        h1_last.append(i)
    is_now = not is_now

for ifirst, ilast in zip( h1_first, h1_last ):
    ax.axvspan(dh['time'].isel(time=ifirst).dt.strftime('%Y-%m-%d').values, dh['time'].isel(time=ilast).dt.strftime('%Y-%m-%d').values, color='yellow', alpha=0.4)

is_now = False
h2_first = []
h2_last = []
for i in range(dh2.shape[0]-1):
    if is_now == dh2[i]:
        continue
    if is_now :
        h2_first.append(i)
    else :
        h2_last.append(i)
    is_now = not is_now
for ifirst, ilast in zip( h2_first, h2_last ):
    ax.axvspan(dh2['time'].isel(time=ifirst).dt.strftime('%Y-%m-%d').values, dh2['time'].isel(time=ilast).dt.strftime('%Y-%m-%d').values, color='orange', alpha=0.4)

dnorm.plot.line(color='gray',label='normal')

plt.legend()
ax.set_title( 'SST w/ Heatwave '+region_name )
ax.set_xlabel('')
ax.set_ylabel('C')
ax.set_xlim(pd.to_datetime('2022-01-01'),pd.to_datetime('2024-12-31'))

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
