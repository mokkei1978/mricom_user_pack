#!/usr/bin/env python
"""流速鉛直断面分布を描く

Usage: contour_v_section.py YMD

Arguments:
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
#from data_month import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
date = args.get('YMD')
logger.debug(date)

DS = xarray_maker.open_dataset('../../link/data/MOVEJPN/month/nc_v.2*','mricom-history')
#DSclim = xarray_maker.open_dataset(confs[3]['file'],confs[3]['kind'])
logger.debug(DS)

da = DS['vo'].sel(time=date,lat=40.,method='nearest').sel(lev=slice(1,200),lon=slice(131.,138.)).squeeze()

#for it in da['time']:
#    danm.loc[{'time':it}] -= daclim.sel(time='2008-'+ str(it.time.dt.month.values) ).squeeze()
#danm -= daclim.sel(time='2008-'+ str(da.time.dt.month.values) ).squeeze()

fig, ax = plt.subplots()
clevs=np.arange(-40.,40.1,5.)
#da.plot.pcolormesh( x='lat',y='lev',
da.plot.pcolormesh( x='lon',y='lev',
                    cmap=cm.RdYlBu_r, levels=np.arange(-40.,40.1,1.),
                    cbar_kwargs={'ticks':clevs} )
#cntr = da.plot.contour(x='lat',y='lev',levels=clevs, colors="black", linewidths=0.5)
cntr = da.plot.contour(x='lon',y='lev',levels=clevs, colors="black", linewidths=0.5)
ax.clabel(cntr)

ax.set_ylim( da['lev'].max(), da['lev'].min() )
ax.xaxis.set_major_formatter( LatitudeFormatter() )
#ax.set_title(da.long_name+'['+da.units+'] '+date)

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
