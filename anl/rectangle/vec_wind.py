#!/usr/bin/env python
"""風応力分布を描く(grads形式のモデル強制力ファイルを直接に読む)

Usage: vec_wind.py YMD

Arguments:
  YMD  date for plot(YYYY-MM-DD)
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

from lib import xarray_maker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
date = args.get('YMD')
logger.debug(date)

DS = xarray_maker.open_dataset('../../../rectangle_data/wind_2gyre.01/wind_x.ctl','grads')
#- 風応力ファイルのパスを指定する
logger.debug(DS)

taux = DS["uo"].values.squeeze()
tauy = DS["uo"].values.squeeze() * 0.0
tau_mag = np.sqrt( taux**2 + tauy**2 )
lon_deg = DS["lon"].values
lat_deg = DS["lat"].values

fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0) )

proj = ccrs.PlateCarree()
cntr = ax.contourf(lon_deg,lat_deg,tau_mag,transform=proj,cmap=cm.Oranges)
fig.colorbar(cntr)

Q = ax.quiver(lon_deg,lat_deg,taux,tauy,color='black',transform=proj)

ax.set_xticks( np.arange(0.,60.1,10.), crs=proj )
ax.set_yticks( np.arange(10.,60.1,10.), crs=proj )
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
#ax.set_extent((127., 143., 33., 50.), crs=proj )
ax.set_title( 'wind stress [dyn/cm^2]' )

plt.show()
#plt.savefig('temp.png', bbox_inches='tight')
#logger.info('OUTPUT: temp.png')
