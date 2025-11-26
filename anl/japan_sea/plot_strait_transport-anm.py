#!/usr/bin/env python
"""海峡通過流量の時系列を描く

Usage: plot_strait_transport.py

"""

import xarray as xr
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/strait/strait_transport.nc')

ds_clim=ds.groupby('time.month').mean(dim='time')
ds=ds.groupby('time.month') - ds_clim

da3=ds.tsushima_e + ds.tsushima_w
da3_base = da3 * 0.e0 + 0.e0
da3 = da3 + 0.e0
da3_roll = da3.rolling(time=7,center=True).mean()

da1=ds.tsugaru
da1_base = da1 * 0.e0 - 1.e0
da1 = da1 - 1.e0
da1_roll = da1.rolling(time=7,center=True).mean()

da2=ds.soya
da2_base = da2 * 0.e0 + 1.e0
da2 = da2 + 1.e0
da2_roll = da2.rolling(time=7,center=True).mean()

fig, ax = plt.subplots()
da3.plot.line(color='lightgreen')
da3_base.plot.line(color='green',linestyle=':')
da3_roll.plot.line(label='tsushima',color='green')
da1.plot.line(color='lightblue')
da1_base.plot.line(color='blue',linestyle=':')
da1_roll.plot.line(label='tsugaru',color='blue')
da2.plot.line(color='yellow')
da2_base.plot.line(color='orange',linestyle=':')
da2_roll.plot.line(label='soya',color='orange')

plt.legend(loc='upper left')
ax.set_title( 'transport anomaly w/ 7-month running mean' )
ax.set_xlabel('')
ax.set_ylabel('Sv')

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
