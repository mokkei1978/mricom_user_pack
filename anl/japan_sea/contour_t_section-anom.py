#!/usr/bin/env python
"""水温鉛直断面分布を描く

Usage: contour_t_section.py NDATA YMD

Arguments:
  NDATA date number (see data.py)
  YMD  date for plot(YYYY-MM-DD)
"""

import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from docopt import docopt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import logging

from lib import xarray_maker
#from data import confs
from data_month import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )
date = args.get('YMD')
logger.debug(date)

conf=confs[ndata]
DS = xarray_maker.open_dataset(conf['file'],conf['kind'])
DSclim = xarray_maker.open_dataset(confs[3]['file'],confs[3]['kind'])
logger.debug(DS)

da = DS['thetao'].sel(time=date,lev=slice(1,350),lon=slice(131.,138.),lat=slice(35.,45.)).squeeze()
da = da.mean(dim='lon')
daclim = DSclim['thetao'].sel(time='2008-'+date[5:7],lev=slice(1,350),lon=slice(131.,138.),lat=slice(35.,45.)).squeeze()
daclim = daclim.mean(dim='lon')

danm = da - daclim

fig, ax = plt.subplots()
clevs=np.arange(0.,30.1,2.)
danm.plot.pcolormesh( x='lat',y='lev',
                    cmap=cm.coolwarm, levels=np.arange(-4.,4.1,0.25) )
#                    cbar_kwargs={'ticks':clevs} )
cntr2= daclim.plot.contour(x='lat',y='lev',levels=clevs, colors="green", linewidths=0.5)
ax.clabel(cntr2)
cntr = da.plot.contour(x='lat',y='lev',levels=clevs, colors="black", linewidths=0.5)
ax.clabel(cntr)

ax.set_ylim( da['lev'].max(), da['lev'].min() )
ax.xaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title('T anomaly 131-138E '+date)
ax.set_xlabel('')

plt.savefig('temp.png', bbox_inches='tight')
plt.savefig('tanm_sec_'+date+'.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
