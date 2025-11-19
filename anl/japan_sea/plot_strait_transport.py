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

ds=xr.open_dataset('strait_transport.nc')

da3=ds.tsushima_e + ds.tsushima_w
da4=da3-ds.tsugaru-ds.soya

fig, ax = plt.subplots()
ds.tsugaru.plot.line(label='tsugaru')
ds.soya.plot.line(label='soya')
da3.plot.line(label='tsushima')
da4.plot.line(label='residual')

plt.legend()
ax.set_title( 'transport' )
ax.set_xlabel('')
#ax.set_ylabel('C')

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
