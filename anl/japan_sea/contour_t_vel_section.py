#!/usr/bin/env python
"""水温と流速の鉛直断面分布を重ねて描く

Usage: contour_t_vel_section.py YMD

Arguments:
  YMD  date for plot(YYYYMMDD or YYYYMM)
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
cdate = args.get('YMD')

DSt = xarray_maker.open_dataset('../../link/data/MOVEJPN/month/nc_t.'+cdate,'mricom-history')
#DSu = xarray_maker.open_dataset('../../link/data/MOVEJPN/month/nc_u.'+cdate,'mricom-history')
DSv = xarray_maker.open_dataset('../../link/data/MOVEJPN/month/nc_v.'+cdate,'mricom-history')
#DSclim = xarray_maker.open_dataset(confs[3]['file'],confs[3]['kind'])

dat = DSt['thetao'].sel(lat=40.2,method='nearest').sel(lev=slice(1,200),lon=slice(129.,139.)).squeeze()
dav = DSv['vo'].sel(lat=40.2,method='nearest').sel(lev=slice(1,200),lon=slice(129.,139.)).squeeze()

#for it in da['time']:
#    danm.loc[{'time':it}] -= daclim.sel(time='2008-'+ str(it.time.dt.month.values) ).squeeze()
#danm -= daclim.sel(time='2008-'+ str(da.time.dt.month.values) ).squeeze()

fig, ax = plt.subplots(figsize=(10,8))
#da.plot.pcolormesh( x='lat',y='lev',

dat.plot.pcolormesh( x='lon',y='lev',
                     cmap=cm.jet, levels=np.arange(-1.,30.1,1.) )
cntr = dav.plot.contour(x='lon',y='lev',levels=np.arange(-40.,40.1,5.), colors="black", linewidths=0.5)
ax.clabel(cntr)

ax.set_ylim( dat['lev'].max(), dat['lev'].min() )
ax.xaxis.set_major_formatter( LongitudeFormatter() )
#ax.set_title(da.long_name+'['+da.units+'] '+date)

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
