#!/usr/bin/env python
"""ある深さの水温偏差水平分布を描く(月平均)

Usage: contour_t_anom_mo.py NDATA NCLIM YM DEPTH

Arguments:
  NDATA data number (see data.py)
  NCLIM data number for climatology
  YM    date for plot(YYYY-MM)
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
import datetime

#- local
from lib import xarray_maker
#from data import confs
from data_month import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )
nclim = int( args.get('NCLIM') )
date = args.get('YM')
depth_m = args.get('DEPTH')
logger.debug(date)

conf=confs[ndata]

DSclim = xarray_maker.open_dataset(confs[nclim]["file"],confs[nclim]['kind'])
DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
#logger.debug(DS)

da = DS["thetao"].sel(time=date,lev=depth_m).mean(dim="time")
undef = conf.get('undef',0.)
if undef != 0. :
    da = da.where( da != undef )

#da = da.where( da > -20. )

month = int(date.split('-')[1])
daclim = DSclim["thetao"].sel(lev=depth_m,time=DSclim["thetao"].time.dt.month.isin(month)).mean(dim="time")

daclim2=daclim.sel(lon=slice(127,143),lat=slice(33,50))
da2=da.sel(lon=slice(127,143),lat=slice(33,50)).interp(lon=daclim2['lon'],lat=daclim2['lat'])
da3 = da2 - daclim2


fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

da3.plot.pcolormesh( transform=proj,
                    cmap=cm.coolwarm, levels=np.arange(-8.,8.1,0.5) )

cntr = da3.plot.contour(transform=proj,levels=np.arange(-8.,8.1,2), colors="black" )
ax.clabel(cntr)

ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title( conf["name"]+' Tanom '+date )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
plt.savefig('tanom_'+depth_m+'_'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
