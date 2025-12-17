#!/usr/bin/env python
"""貯熱量の時系列を描く

Usage: plot_heat_cont.py

"""

import xarray as xr
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/heat_50m/north_japan_sea/heat_cont.nc')

fig, ax = plt.subplots()
ds.hc.plot.line()

#plt.legend()
#ax.set_title( 'transport' )
ax.set_title( '50m heat content (north Japan Sea)' )
ax.set_xlabel('')
ax.set_ylabel(ds.hc.units)

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
