#!/usr/bin/env python
"""日本海のJRA-3Q 陸海グリッドファイルを作る

Usage: make_jra3q_seagrid.py

"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import logging

#- local
from lib import xarray_maker
from data_heatflux import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

conf=confs[0]
DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
logger.debug(DS)

da = DS['DSWRF_surface'].isel(time=0).squeeze()
da = da*0.

da[100,104:106] = 1.
da[101,104:109] = 1.
da[102,104:110] = 1.
da[103,103:112] = 1.
da[104,103:112] = 1.
da[105,104:112] = 1.
da[106,106:112] = 1.
da[107,109:113] = 1.
da[108,110:114] = 1.
da[109,111:114] = 1.

da = da.drop_vars('time').rename('sea_land')

da.to_netcdf(path='./seagrid_japansea.nc',mode='w')
logger.info('OUTPUT: seagrid_japansea.nc')

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

da.plot.pcolormesh( transform=proj,
                    cmap=cm.RdYlBu_r, levels=np.arange(0.1,0.9,0.1))


ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')

