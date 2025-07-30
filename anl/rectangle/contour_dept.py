#!/usr/bin/env python
"""ALE実験における層水深の分布を描く

Usage: contour_dept.py FILE YMD K

Arguments:
  FILE  path of input file
  YMD   date for plot(YYYY-MM-DD)
  K     layer number for plot [0:km-1]

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
file_in = args.get('FILE')
date = args.get('YMD')
klayer = int( args.get('K') )

logger.debug(date)

DS = xr.open_mfdataset(file_in)
logger.debug(DS)

da = DS["dep"].sel(time=date).isel(depth=klayer).squeeze()

ctitle = da.standard_name
cunit = da.units
da = da - da.mean().values

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(0.,60.1,20.), crs=proj )
ax.set_yticks( np.arange(10.,60.1,10.), crs=proj )
ax.set_extent((0., 60., 10., 60.), crs=proj )

clevs=np.arange(-200.,200.1,5.)*1.
llevs=np.arange(-200.,200.1,20.)*1.
da.plot.pcolormesh( transform=proj,
                    cmap=cm.jet_r, levels=clevs,
                    cbar_kwargs={'ticks':llevs} )
cntr = da.plot.contour(transform=proj,levels=llevs, colors='black', linewidths=0.5  )
ax.clabel(cntr)

ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title(ctitle+'['+cunit+'] k='+str(klayer+1)+' '+date)

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
