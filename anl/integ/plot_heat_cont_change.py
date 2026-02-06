#!/usr/bin/env python
"""貯熱量の時間変化率の時系列を描く

Usage: plot_heat_cont_change.py

"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

#filei='../../link/data/MOVEJPN/anl_mon-jpn/heat_50m/japan_sea_all/heat_cont.nc'
#title='50m heat content (Japan Sea All)'
filei='../../link/data/JPN20-assim/anl_mon-jpn/heat_btm/japan_sea_all/heat_cont-clim.nc'
title='heat content clim change (Japan Sea All)'

ds=xr.open_dataset(filei)

dhc = ds.hc.values - np.roll(ds.hc.values,1)
cal2 = ds.time.values + np.timedelta64(14,'D')
cal3 = np.roll(cal2,+1)
cal3[0] = np.datetime64('2007-12-15T00:00:00') #+np.timedelta64(-1,'Y').astype('<m8[ns]')
dtime = cal2 - cal3
ds['change'] = ('time',dhc /dtime.astype('timedelta64[s]').astype(int) * 4.2e3 * 1024. * 1.e-12 ) 

ds2=xr.open_dataset('../../link/data/JPN20-assim/anl_mon-jpn/heat_200m/japan_sea_all/heat_cont-clim.nc')
dhc2 = ds2.hc.values - np.roll(ds2.hc.values,1)
ds2['change'] = ('time',dhc2 /dtime.astype('timedelta64[s]').astype(int) * 4.2e3 * 1024. * 1.e-12 ) 

ds3=xr.open_dataset('../../link/data/JPN20-assim/anl_mon-jpn/heat_50m/japan_sea_all/heat_cont-clim.nc')
dhc3 = ds3.hc.values - np.roll(ds3.hc.values,1)
ds3['change'] = ('time',dhc3 /dtime.astype('timedelta64[s]').astype(int) * 4.2e3 * 1024. * 1.e-12 ) 

fig, ax = plt.subplots()

ds.change.plot.line(label='all-depth')
ds2.change.plot.line(label='200m')
ds3.change.plot.line(label='50m')

plt.legend()
ax.set_title( title )
ax.set_xlabel('')
ax.set_ylabel('TW')
ax.grid()

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
