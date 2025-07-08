#!/usr/bin/env python
"""T分布を描く

Usage: contour_t.py NDATA YMD DEPTH

Arguments:
  NDATA date number (see data.py)
  YMD   date for plot(YYYY-MM-DD)
  DEPTH depth for plot [m]
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
#from data import confs
from data_month import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )
date = args.get('YMD')
depth_m = args.get('DEPTH')
logger.debug(date)

conf=confs[ndata]

DSclim = xarray_maker.open_dataset(confs[3]["file"],confs[3]['kind'])
DSclim = DSclim.rename({'depth':'lev'})

DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
DS = DS.rename({'depth':'lev'})
logger.debug(DS)

da = DS["thetao"].sel(time=date).sel(lev=depth_m).squeeze()
undef = conf.get('undef',0.)
if undef != 0. :
    da = da.where( da != undef )

da = da.where( da > -20. )
daclim = DSclim["thetao"].sel(time='2008-'+da['time'].dt.strftime('%m').values).sel(lev=depth_m).squeeze().where( da != 9.999e20 )

da = da - daclim


fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

da.plot.pcolormesh( transform=proj,
                    cmap=cm.coolwarm, levels=np.arange(-8.,8.1,0.5) )

cntr = da.plot.contour(transform=proj,levels=np.arange(-8.,8.1,2), colors="black" )
ax.clabel(cntr)

ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title( conf["name"]+' Tanom '+depth_m+'m '+date )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
plt.savefig('tanom_'+depth_m+'_'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
