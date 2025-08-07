#!/usr/bin/env python
"""日本海のHIMSST/MGDSST 陸海グリッドファイルを作る

Usage: make_seagrid.py NDATA

Arguments:
  NDATA date number (see data.py, 0/4)
"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
from docopt import docopt
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import logging

#- local
from lib import xarray_maker
from data import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )
logger.debug(ndata)

conf=confs[ndata]
DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
logger.debug(DS)

da = DS['thetao'].isel(time=0).squeeze()
da = da*0.

#- all
#da.loc[{'lon':slice(128,140),'lat':slice(35,47)}] = 1.
#da.loc[{'lon':slice(138,140),'lat':slice(35,36)}] = 0.
#da.loc[{'lon':slice(140,142),'lat':slice(43,47)}] = 1.

#- south
da.loc[{'lon':slice(130,140),'lat':slice(35,40)}] = 1.
da.loc[{'lon':slice(138,140),'lat':slice(35,36)}] = 0.

#- north
#da.loc[{'lon':slice(130,140),'lat':slice(40,45)}] = 1.

da = da.drop_vars('time').rename('sea_land')

da.to_netcdf(path='./seagrid.nc',mode='w')
logger.info('OUTPUT: seagrid.nc')


fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )
da.where(da > 0.5).plot.pcolormesh( transform=proj, add_colorbar=False,
                    cmap=cm.RdYlBu_r, levels=np.arange(0.1,0.9,0.1))
ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')

