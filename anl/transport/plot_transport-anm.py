#!/usr/bin/env python
"""輸送量の時系列を描く

Usage: plot_transport-anm.py

"""

import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

#ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/heat_200m/north_japan_sea-adv/trans_temp.nc')
ds=xr.open_dataset('../../link/data/MOVEJPN/anl_day-jpn/heat_200m/north_japan_sea-adv/trans_temp.nc').resample(time='ME').mean()
cunits=ds.east.units
ds_clim=ds.groupby('time.month').mean(dim='time')
ds=ds.groupby('time.month') - ds_clim

doffset=3.e7

da3=-ds.east + ds.south
da3_base = da3 * 0.e0 + 0.e0
da3 = da3 + 0.e0
da3_roll = da3.rolling(time=7,center=True).mean()

da1=ds.east
da1_base = da1 * 0.e0 - doffset
da1 = da1 - doffset
da1_roll = da1.rolling(time=7,center=True).mean()

da2=ds.south
da2_base = da2 * 0.e0 + doffset
da2 = da2 + doffset
da2_roll = da2.rolling(time=7,center=True).mean()

fig, ax = plt.subplots()
da3.plot.line(color='lightgreen')
da3_base.plot.line(color='green',linestyle=':')
da3_roll.plot.line(label='net',color='green')
da1.plot.line(color='lightblue')
da1_base.plot.line(color='blue',linestyle=':')
da1_roll.plot.line(label='east',color='blue')
da2.plot.line(color='yellow')
da2_base.plot.line(color='orange',linestyle=':')
da2_roll.plot.line(label='south',color='orange')

plt.legend(loc='upper left')
ax.set_title( '200m heat content - lateral adv anom' )
ax.set_xlabel('')
ax.set_ylabel(cunits)
ax.set_xlim(pd.to_datetime('2022-01-01'),pd.to_datetime('2024-12-31'))
plt.grid()

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
