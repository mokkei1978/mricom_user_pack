#!/usr/bin/env python
"""流量、輸送量の時系列を描く

Usage: plot_transport.py

"""

import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

#ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/heat_200m/north_japan_sea-adv/trans_temp.nc')
ds=xr.open_dataset('../../link/data/MOVEJPN/anl_day-jpn/heat_50m/north_japan_sea-adv/trans_temp.nc')

fig, ax = plt.subplots()
ds.east.plot.line(label='east')
ds.south.plot.line(label='south')

plt.legend()
#ax.set_title( 'transport' )
ax.set_title( '50m heat content - lateral adv (north Japan Sea)' )
ax.set_xlabel('')
ax.set_ylabel(ds.east.units)
ax.set_xlim(pd.to_datetime('2023-03-01'),pd.to_datetime('2023-08-31'))

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
