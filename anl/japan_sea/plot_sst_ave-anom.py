#!/usr/bin/env python
"""SST水平平均値の偏差の時系列を描く(make_sst_ave.py の出力を使う)

Usage: plot_sst_ave-anom.py NDATA

Arguments:
  NDATA date number (see data.py)
"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from docopt import docopt
import logging
import pandas as pd
import matplotlib.dates as mdates

#- local
from lib import xarray_maker
from data import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )
logger.debug(ndata)

conf=confs[ndata]

#region_name='Japan Sea (South)'
#ncdir='nc/japansea_south'
#region_name='Japan Sea (North)'
#ncdir='nc/japansea_north'
region_name='Japan Sea (All)'
ncdir='nc/japansea_all'
ds1=xr.open_dataset(ncdir+'/sst_ave_mgd.nc')
#ds1['thetao'] = ds1.thetao.rolling(time=31,center=True).mean()
grouped1=ds1.groupby("time.year")
ds2=xr.open_dataset(ncdir+'/sst_ave_him.nc').sel(time=slice('2018-01-01','2025-12-31'))
#ds2['thetao'] = ds2.thetao.rolling(time=31,center=True).mean()
grouped2=ds2.groupby("time.year")
dm_norm=xr.open_dataset(ncdir+'/sst_ave_norm.nc')

labels={
     '1982':'1982-2017(MGD)',
     '2022':'2018-2022',
     '2023':'2023',
     '2024':'2024',
     '2025':'2025',}
colors={
     '2023':'purple',
     '2024':'red',
     '2025':'orange',}
#    '2018':(0.4,0.4,1.),
#     '2019':(0.5,0.5,1.),
#     '2020':(0.6,0.6,1.),
#     '2021':(0.7,0.7,1.),
#     '2021':'yellow',
#     '2022':(0.8,0.8,1.),

fig, ax = plt.subplots()

dm_norm["time"]=pd.to_datetime('2020-'+dm_norm.time.dt.strftime('%m-%d').values)

for year, group in grouped1:
    if year >= 2018 :
        continue
    logger.debug(colors.get(str(year)))
    dyear = group
    dyear["time"]=pd.to_datetime('2020-'+group.time.dt.strftime('%m-%d').values)
    dyear = dyear - dm_norm

    dyear = dyear.resample(time='ME').mean()     #- monthly
    dyear["time"]=pd.to_datetime('2020-'+dyear.time.dt.strftime('%m-15').values)

    dyear["thetao"].plot.line(xlim=[pd.Timestamp('2020-01-01'),pd.Timestamp('2020-12-31')],
                              ylim=[-4.2,4.2],
                              label=labels.get(str(year),''),
                              color=colors.get(str(year),'gray'), linewidth=0.5)

for year, group in grouped2:
    logger.debug(colors.get(str(year)))
    dyear = group
    dyear["time"]=pd.to_datetime('2020-'+group.time.dt.strftime('%m-%d').values)
    dyear = dyear - dm_norm
    dyear = dyear.resample(time='ME').mean()
    dyear["time"]=pd.to_datetime('2020-'+dyear.time.dt.strftime('%m-15').values)
    dyear["thetao"].plot.line(xlim=[pd.Timestamp('2020-01-01'),pd.Timestamp('2020-12-31')],
                              label=labels.get(str(year),''),
                              color=colors.get(str(year),'lightskyblue'))

plt.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=15))
ax.set_title( 'Monthly HIMSST anomaly (Japan Sea)' )
#ax.set_title( conf["name"]+' anomaly (31d runmean) '+ region_name )
ax.set_xlabel('')
ax.set_ylabel('[C]',fontsize='large')
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
plt.grid(axis='y')

#plt.show()
#plt.savefig('sst'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
