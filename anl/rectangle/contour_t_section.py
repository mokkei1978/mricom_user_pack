#!/usr/bin/env python
"""水温鉛直断面分布を描く

Usage: contour_t_section.py FILE YMD

Arguments:
  FILE path of input file
  YMD  date for plot(YYYY-MM-DD)
"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from docopt import docopt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
file_in = args.get('FILE')
date = args.get('YMD')

logger.debug(date)

DS = xr.open_mfdataset(file_in)
logger.debug(DS)


da = DS["thetao"].sel(time=date).sel(lon=30.).squeeze()
#da = da.isel(depth=slice(1,9))

fig = plt.figure()
ax = plt.subplot(1,1,1)
#ax.set_xticks( np.arange(0.,60.1,20.), crs=proj )
#ax.set_yticks( np.arange(10.,60.1,10.), crs=proj )
#ax.set_extent( (10., 60., 300., 500.,) )

cntr = da.plot.contour(levels=20)

ax.clabel(cntr)
ax.set_ylim( da.depth.max(), da.depth.min() )
ax.xaxis.set_major_formatter( LatitudeFormatter() )
#ax.set_title(da.long_name+'['+da.units+'] '+date)

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
