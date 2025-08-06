#!/usr/bin/env python
"""海洋熱波しきい値分布を描く

Usage: contour_heatwave_thres.py NDAY

Arguments:
  NDAY  number of day
"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from docopt import docopt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import logging

#- local
from lib import xarray_maker
from data import confs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
#logger.info('START')

args = docopt(__doc__)
nday = int( args.get('NDAY') )
logger.debug(nday)

DS = xr.open_mfdataset('../../link/data/netCDF/MGDSST/heatwave/mgdsst365_jpn_thre_11win_1991-2020.nc')
logger.debug(DS)

da = DS['tos'].isel(time=nday).squeeze()
#if ndata == 2 :
#    da = da.isel(depth=0).squeeze()
#undef = conf.get('undef',0.)
#if undef != 0. :
#    da = da.where( da != undef )

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

da.plot.pcolormesh( transform=proj,
                    cmap=cm.jet, levels=np.arange(-1.,30.1,1.) )

cntr = da.plot.contour(transform=proj,levels=20, colors="black" )
ax.clabel(cntr)

ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title( 'marine heatwave thres '+str(nday) )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
#plt.savefig('sst'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
