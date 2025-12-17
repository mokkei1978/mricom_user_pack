#!/usr/bin/env python
"""輸送量の時系列を描く

Usage: plot_transport-clim.py

"""

import xarray as xr
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/trans_t/north_japan_sea/trans_temp.nc')
ds_clim=ds.groupby('time.month').mean(dim='time')

fig, ax = plt.subplots()
ds_clim.east.plot.line(label='east')
ds_clim.south.plot.line(label='south')

plt.legend()
ax.set_title( 'T transport across boundary (north Japan Sea) (2008-2024)' )
ax.set_xlabel('month')
ax.set_ylabel('C m3/s')

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
