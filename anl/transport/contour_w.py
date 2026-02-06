#!/usr/bin/env python
"""ある深さの鉛直流速分布を描く

Usage: contour_w.py YMD KL

Arguments:
  YMD   date for plot(YYYY-MM-DD)
  KL    k-layer number for plot
"""
#  NDATA date number (see data.py)

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
#from data_month import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
#ndata = int( args.get('NDATA') )
date = args.get('YMD')
klayer = args.get('KL')
logger.debug(date)

#conf=confs[ndata]

DS = xarray_maker.open_dataset('../../link/data/JPN20-assim/anl_mon-jpn/wlwl/2008/w2.2*','mricom-history')
logger.debug(DS)


da = DS["w"].sel(time=date).isel(lev=int(klayer)).squeeze()
#if undef != 0. :
#    da = da.where( da != undef )
#da = da.where( da > -20. )

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

da.plot.pcolormesh( transform=proj, levels=np.arange(-10.,10.1,1.)*0.001 )
#                    cbar_kwargs={'ticks':np.arange(0.,30.1,2.)} )

#cntr = da.plot.contour(transform=proj,levels=np.arange(0.,30.,2.), colors="black", linewidths=0.5)
#ax.clabel(cntr)

ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title( 'JPN w at k = '+klayer+' '+date )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
#plt.savefig('t_'+depth_m+'_'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
