#!/usr/bin/env python
"""水温の時間・緯度ホフメラー図を描く

Usage: contour_t_yt.py NDATA

Arguments:
  NDATA date number (see data.py)
"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from docopt import docopt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import pandas as pd
import logging

from lib import xarray_maker
#from data import confs
from data_month import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )

conf=confs[ndata]
DS = xarray_maker.open_dataset(conf['file'],conf['kind'])
DSclim = xarray_maker.open_dataset(confs[3]['file'],confs[3]['kind'])
logger.debug(DS)

lev_m=50.
da = DS['thetao'].sel(lev=lev_m,lon=slice(131.,138.),lat=slice(35.,45.)).squeeze()
da = da.mean(dim='lon')
daclim = DSclim['thetao'].sel(lev=lev_m,lon=slice(131.,138.),lat=slice(35.,45.)).squeeze()
daclim = daclim.mean(dim='lon')

danm = da.copy()
for it in da['time']:
    danm.loc[{'time':it}] -= daclim.sel(time='2008-'+ str(it.time.dt.month.values) ).squeeze()

daclim=xr.concat([daclim,daclim,daclim,daclim],dim='time')
daclim['time']=pd.date_range(start='2021-01',end='2024-12',freq='MS')

fig, ax = plt.subplots()
clevs=np.arange(0.,30.1,2.)
#clevs=[8.,10.]
#clevs=[10.]
danm.plot.pcolormesh( x='time',y='lat',
                    cmap=cm.coolwarm, levels=np.arange(-4.,4.1,0.25) )
#                    cbar_kwargs={'ticks':clevs} )
cntr2= daclim.plot.contour(x='time',y='lat',levels=clevs, colors="green", linewidths=0.5)
ax.clabel(cntr2)
cntr = da.plot.contour(x='time',y='lat',levels=clevs, colors="black", linewidths=0.5)
ax.clabel(cntr)

#ax.set_ylim( da['lev'].max(), da['lev'].min() )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title('T anomaly 131-138E at depth = '+str(lev_m))
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight')
#plt.savefig('tanm_sec_'+date+'.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
