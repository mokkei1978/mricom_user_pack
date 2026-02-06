#!/usr/bin/env python
"""貯熱量の時系列を描く

Usage: plot_heat_cont.py

"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

#filei='../../link/data/MOVEJPN/anl_mon-jpn/heat_btm/japan_sea_all/heat_cont.nc'
title='heat content clim (Japan Sea All)'
filei='../../link/data/JPN20-assim/anl_mon-jpn/heat_btm/japan_sea_all/heat_cont-clim.nc'
#title='200m heat content clim (Japan Sea All)'

ds=xr.open_dataset(filei)
ds['ohc'] = ds.hc * 4.2e3 * 1024.

ds2=xr.open_dataset('../../link/data/JPN20-assim/anl_mon-jpn/heat_200m/japan_sea_all/heat_cont-clim.nc')
ds2['ohc'] = ds2.hc * 4.2e3 * 1024.
ds3=xr.open_dataset('../../link/data/JPN20-assim/anl_mon-jpn/heat_50m/japan_sea_all/heat_cont-clim.nc')
ds3['ohc'] = ds3.hc * 4.2e3 * 1024.

fig, ax = plt.subplots()

ds.ohc.plot.line(label='all-depth')
#ax.plot( ds.time, ds.hc )
ds2.ohc.plot.line(label='200m')
ds3.ohc.plot.line(label='50m')

plt.legend()
ax.set_title( title )
ax.set_xlabel('')
ax.set_ylabel('J')
yrange=np.array([1.e21,10.e21])
ax.set_ylim(yrange)
ax.grid()

ax2=ax.twinx()
ds.hc.plot.line()
ax2.set_title('')
ax2.set_xlabel('')
ax2.set_ylabel(ds.hc.units)
ax2.set_ylim(yrange/4.2e3/1024.)

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
