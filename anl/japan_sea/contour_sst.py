#!/usr/bin/env python
"""SST分布を描く

Usage: contour_sst.py NDATA YMD

Arguments:
  NDATA date number (see data.py)
  YMD   date for plot(YYYY-MM-DD)
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )
date = args.get('YMD')
logger.debug(date)

conf=confs[ndata]

DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
logger.debug(DS)

da = DS["thetao"].sel(time=date).squeeze()
if ndata == 2 :
    da = da.isel(depth=0).squeeze()
undef = conf.get('undef',0.)
if undef != 0. :
    da = da.where( da != undef )

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
ax.set_title( conf["name"]+' '+date )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
#plt.savefig('sst'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
