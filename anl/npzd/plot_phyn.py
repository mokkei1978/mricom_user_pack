#!/usr/bin/env python
"""植物プランクトン分布を描く

Usage: plot_phyn.py FILE

Arguments:
  FILE path of input file
"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from docopt import docopt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cmocean

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
file_in = args.get('FILE')
#date = args.get('YMD')

DS = xr.open_mfdataset(file_in)
logger.debug(DS)

da = DS['phyn'].sel(depth=1.).squeeze()
da = da.where( da != 999. )

da = da * 2.e3
da.attrs['units'] = 'micro g Chl /L'
da.attrs['standard_name'] = 'Chlorophyll a'

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()
ax.set_extent((117., 160., 20., 52.), crs=proj )

vmax = 2.e0
da.plot.pcolormesh(
    transform=proj, cmap='jet',
    vmin=0, vmax=vmax,
    cbar_kwargs={'ticks': np.arange(0, vmax + 1.e-4, 2.e-1)}
)

ax.coastlines()
ax.set_xticks( np.arange(120.,160.1,10.), crs=proj )
ax.set_yticks( np.arange(20.,50.1,5.), crs=proj )
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )

time_str = pd.Timestamp(da.time.values).strftime('%Y-%m')
ax.set_title(f'Phytoplankton ({time_str})')

ax.set_xlabel('')
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
