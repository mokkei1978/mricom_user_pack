#!/usr/bin/env python
"""貯熱量の熱収支の時系列を描く

Usage: plot_heat_budgetx.py

"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/heat_btm/japan_sea_all/heat_cont.nc')
dhc = ds.hc.values - np.roll(ds.hc.values,1)
cal2 = ds.time.values + np.timedelta64(14,'D')
cal3 = np.roll(cal2,+1)
cal3[0] = np.datetime64('2007-12-15T00:00:00') #+np.timedelta64(-1,'Y').astype('<m8[ns]')
dtime = cal2 - cal3
ds['change'] = ('time',dhc /dtime.astype('timedelta64[s]').astype(int) * 4.2e3 * 1024. * 1.e-12 ) 

dst=xr.open_dataset('nc/strait_t/trans_month.nc')
da2= ( dst.tsushima_e + dst.tsushima_w - dst.tsugaru - dst.soya ) * 4.2e3 * 1024. * 1.e-12
# [K m3/s] => [TW]

daq=xr.open_dataset('nc/japansea_all/heatflux_ave_usui.nc')['total']

fig, ax = plt.subplots()

ds.change.plot.line(label='OHC change',color='black')
da2.plot.line(label='T transport',color='red')
daq.plot.line(label='surface Q',color='blue')
(da2+daq).plot.line(label='T+Q',color='purple',linestyle='dotted')

plt.legend()
ax.set_title( 'All-depth heat content change (Japan Sea)' )
ax.set_xlabel('')
ax.set_ylabel('TW')
ax.grid()
ax.set_xlim(pd.to_datetime('2022-01-01'),pd.to_datetime('2024-12-31'))

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
