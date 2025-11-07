#!/usr/bin/env python
"""モデルの水深図を描く(地図投影)"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import logging
import cmocean

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DS = xr.open_dataset('../../link/data/MOVEJPN/data/topo-jpn.nc')
da = -0.01 * DS['depth']

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

img = da.plot.pcolormesh( transform=proj, vmin=-6000., vmax = 6000.,
                          cmap=cmocean.cm.topo ) #, levels=np.arange(-1.,30.1,1.) )
#fig.colorbar(img)

cntr = da.plot.contour( transform=proj, levels=[-3000.,-200.,], colors="black",
                        linestyles='solid', linewidths=0.5 )
ax.clabel(cntr)

ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title( DS.model_name + ' bathymetry [m]')
ax.set_xlabel('')
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
