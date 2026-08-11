#!/usr/bin/env python
"""JRA-3Q 年平均風応力の分布を描く(風応力ベクトル + 東西成分のカラーシェード)

Usage: plot_wind.py

"""

import sys
sys.path.append('.')

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import cm
from docopt import docopt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)

file_in = '../../link/data/jra3q/month/clim.nc'
ds = xr.open_dataset(file_in)
logger.debug(ds)

uflx = -ds['UFLX_surface'].mean(dim='time')
vflx = -ds['VFLX_surface'].mean(dim='time')
lon_deg = uflx['longitude'].values
lat_deg = uflx['latitude'].values

#- 風応力ベクトルは間引いて描く(極ではベクトル回転が特異点になり誤描画されるため除く)
dec = 6
u2 = uflx.values[1:-1:dec, ::dec]
v2 = vflx.values[1:-1:dec, ::dec]
lon2 = lon_deg[::dec]
lat2 = lat_deg[1:-1:dec]

clevs = np.arange(-0.2, 0.201, 0.02)

#- キャンバス
fig = plt.figure()
#- 表示座標系をデータの座標系(central_longitude=0)と揃える。
#- ずらすとベクトルの回転変換が極付近で不正確になり quiver が乱れるため
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=-160.))
proj = ccrs.PlateCarree(central_longitude=0.)

#- 東西風応力成分のカラーシェード(青-白-赤)
cntr = uflx.plot.contourf(transform=proj, cmap=cm.bwr, levels=clevs,
                           add_colorbar=False)
plt.colorbar(cntr, orientation='horizontal', shrink=0.6, pad=0.08,
             label='Zonal Wind Stress [N/m$^2$]', ax=ax)

#- 風応力ベクトル
Q = ax.quiver(lon2, lat2, u2, v2, color='black', transform=proj,
              scale=3., width=0.0025, pivot='mid')
ax.quiverkey(Q, 0.88, -0.12, 0.1, '0.1 N/m$^2$', labelpos='E', coordinates='axes')

ax.set_facecolor('lightgray')
ax.add_feature(cfeature.LAND, color='lightgray')
ax.coastlines(lw=0.5)
ax.set_extent((90., 285., -15., 63.), crs=proj)
ax.set_xticks(np.arange(90., 286., 30.), crs=proj)
ax.set_yticks(np.arange(-15., 63.1, 15.), crs=proj)
ax.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label=True))
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.set_title('Wind Stress (Annual Mean)')
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight', dpi=200)
logger.info('OUTPUT: temp.png')
