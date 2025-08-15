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

da = DS['thetao'].sel(time=date,lev=slice(1,200),lon=slice(131.,138.),lat=slice(35.,45.)).squeeze()
da = da.mean(dim='lon')

for it in da['time']:
    danm.loc[{'time':it}] -= daclim.sel(time='2008-'+ str(it.time.dt.month.values) ).squeeze()

fig, ax = plt.subplots()
clevs=np.arange(0.,30.1,2.)
da.plot.pcolormesh( x='lat',y='lev',
                    cmap=cm.jet, levels=np.arange(-2.,32.1,1.),
                    cbar_kwargs={'ticks':clevs} )
cntr = da.plot.contour(x='lat',y='lev',levels=clevs, colors="black", linewidths=0.5)
ax.clabel(cntr)

ax.set_ylim( da['lev'].max(), da['lev'].min() )
ax.xaxis.set_major_formatter( LatitudeFormatter() )
#ax.set_title(da.long_name+'['+da.units+'] '+date)

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
