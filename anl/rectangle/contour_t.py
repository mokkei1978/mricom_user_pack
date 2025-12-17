#!/usr/bin/env python
"""水温分布を描く

Usage: contour_t.py FILE YMD DEPTH EXPNAME

Arguments:
  FILE path of input file
  YMD  date for plot(YYYY-MM-DD)
  DEPTH depth for plot [m]
  EXPNAME  name of experiment

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
depth_m = args.get('DEPTH')
exp_name = args.get('EXPNAME')

logger.debug(date)

DS = xr.open_mfdataset(file_in)
logger.debug(DS)

da = DS["thetao"].sel(time=date).sel(depth=depth_m).squeeze()

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

#ax.set_xticks( np.arange(0.,60.1,20.), crs=proj )
#ax.set_yticks( np.arange(10.,60.1,10.), crs=proj )
#ax.set_extent((0., 60., 10., 60.), crs=proj )
ax.set_xticks( np.arange(0.,100.1,20.), crs=proj )
ax.set_yticks( np.arange(0.,60.1,10.), crs=proj )
ax.set_extent((0., 100., 0., 62.), crs=proj )

cntr = da.plot.contour(transform=proj,levels=20 )
ax.clabel(cntr)

ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title(exp_name+' T['+da.units+'] '+date+' '+depth_m+'m')
ax.set_xlabel('')
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
