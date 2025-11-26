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

da3=ds_clim.tsushima_e + ds_clim.tsushima_w
da4=da3-ds_clim.tsugaru-ds_clim.soya

fig, ax = plt.subplots()
ds_clim.tsugaru.plot.line(label='tsugaru')
ds_clim.soya.plot.line(label='soya')
da3.plot.line(label='tsushima')
da4.plot.line(label='residual')

plt.legend()
ax.set_title( 'transport (2008-2024)' )
ax.set_xlabel('month')
ax.set_ylabel('Sv')

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
