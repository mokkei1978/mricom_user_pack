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

dnorml=xr.open_dataset(ncdir+'/sst_ave_norm.nc')['thetao']
dnormn=dnorml.drop_sel(time='2004-02-29').copy()
dnorm=xr.concat([dnormn,dnormn,dnorml,dnormn,dnormn,dnormn,dnorml],dim='time')
dnorm["time"]=pd.date_range(start=date_first,end=date_last)

fig, ax = plt.subplots()

da.plot.line(color='red', label='HIMSST')

for i in range(dh.shape[0]-1):
    if not dh[i]:
        continue
    ax.axvspan(dh['time'].isel(time=i).dt.strftime('%Y-%m-%d').values, dh['time'].isel(time=i+1).dt.strftime('%Y-%m-%d').values, color='yellow', alpha=0.4)

dnorm.plot.line(color='gray',label='normal')

plt.legend()
ax.set_title( 'SST w/ Heatwave '+region_name )
ax.set_xlabel('')
ax.set_ylabel('C')
ax.set_xlim(pd.to_datetime('2022-01-01'),pd.to_datetime('2024-12-31'))

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
