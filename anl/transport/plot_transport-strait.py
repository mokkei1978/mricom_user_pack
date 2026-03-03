#!/usr/bin/env python
"""流量、輸送量の時系列を描く:日本海海峡

Usage: plot_transport-strait.py

"""

import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

#ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/strait/strait_transport.nc')
#ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/strait_t/strait_trans_temp.nc')
#ds=xr.open_dataset('../../link/data/MOVEJPN/anl_day-jpn/strait_t/trans_temp.nc')
ds=xr.open_dataset('trans_month.nc')

da1= ds.tsugaru * 4.2e3 * 1024. * 1.e-12 # [K m3/s] => [TW]
da2= ds.soya * 4.2e3 * 1024. * 1.e-12
da3= ( ds.tsushima_e + ds.tsushima_w ) * 4.2e3 * 1024. * 1.e-12
da4=da3-da2-da1

fig, ax = plt.subplots()
da1.plot.line(label='tsugaru')
da2.plot.line(label='soya')
da3.plot.line(label='tsushima')
da4.plot.line(label='residual')

plt.legend()
#ax.set_title( 'transport' )
ax.set_title( 'T transport' )
ax.set_xlabel('')
ax.set_ylabel('TW')
ax.set_xlim(pd.to_datetime('2022-01-01'),pd.to_datetime('2024-12-31'))

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
