#!/usr/bin/env python
"""SSH分布を描く

Usage: contour_ssh.py FILE YMD EXPNAME

Arguments:
  FILE path of input file
  YMD  date for plot(YYYY-MM-DD)
  EXPNAME  name of experiment

"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from docopt import docopt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
file_in = args.get('FILE')
date = args.get('YMD')
exp_name = args.get('EXPNAME')

logger.debug(date)

DS = xr.open_mfdataset(file_in)
logger.debug(DS)

da = DS["zos"].sel(time=date).squeeze()
da = da * 1.e-2

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=180.) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(100.,281.,40.), crs=proj )
ax.set_yticks( np.arange(-10.,61.,20.), crs=proj )
ax.set_extent( (98., 285., -16., 64.), crs=proj )
#ax.set_xticks( np.arange(120.,150.1,10.), crs=proj )
#ax.set_yticks( np.arange(25.,50.1,5.), crs=proj )
#ax.set_extent( (120., 155., 22., 52.), crs=proj )
#ax.set_xticks( np.arange(0.,100.1,20.), crs=proj )
#ax.set_yticks( np.arange(0.,60.1,10.), crs=proj )
#ax.set_extent((0., 100., 0., 62.), crs=proj )

#cntr = da.plot.contour(transform=proj,levels=20 )
clevs=np.arange(-80.,80.1,10.)*1.e-2
da.plot.pcolormesh( transform=proj, cmap='RdBu_r', vmin=-0.8, vmax=0.8,
                    add_colorbar=False )
#                    cbar_kwargs={'orientation':'horizontal','label':'',
#                                 'shrink':0.6,'ticks':clevs} )
cntr = da.plot.contour(transform=proj,levels=clevs, colors="black",linewidths=0.2 )
ax.clabel(cntr, fontsize=8)

ax.add_feature(cfeature.LAND, facecolor='gray')
ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
#ax.set_title(exp_name+' SSH ['+da.units+'] '+date) #+date[:4])
ax.set_title('')
ax.set_xlabel('')
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight',dpi=300)

logger.info('OUTPUT: temp.png')
