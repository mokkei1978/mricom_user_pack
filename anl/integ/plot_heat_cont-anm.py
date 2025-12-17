#!/usr/bin/env python
"""貯熱量の時系列を描く：偏差

Usage: plot_heat_cont.py

"""

import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/heat_50m/north_japan_sea/heat_cont.nc')
ds_clim=xr.open_dataset('../../link/data/JPN20-assim/anl_mon-jpn/heat_50m/north_japan_sea/heat_cont-clim.nc')
ds=ds.groupby('time.month') - ds_clim.groupby('time.month').mean(dim='time')

fig, ax = plt.subplots()
ds.hc.plot.line(marker='')

#plt.legend()
#ax.set_title( 'transport' )
ax.set_title( '50m heat content (north Japan Sea)' )
ax.set_xlabel('')
ax.set_ylabel(ds.hc.units)
#ax.set_xlim(pd.to_datetime('2022-01-01'),pd.to_datetime('2024-12-31'))
plt.grid()

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
