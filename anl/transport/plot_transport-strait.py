#!/usr/bin/env python
"""流量、輸送量の時系列を描く:日本海海峡

Usage: plot_transport-strait.py

"""

import xarray as xr
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

#ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/strait/strait_transport.nc')
ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/strait_t/strait_trans_temp.nc')

da3=ds.tsushima_e + ds.tsushima_w
da4=da3-ds.tsugaru-ds.soya

fig, ax = plt.subplots()
ds.tsugaru.plot.line(label='tsugaru')
ds.soya.plot.line(label='soya')
da3.plot.line(label='tsushima')
da4.plot.line(label='residual')

plt.legend()
#ax.set_title( 'transport' )
ax.set_title( 'T transport' )
ax.set_xlabel('')
ax.set_ylabel(ds.tsugaru.units)

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
