#!/usr/bin/env python
"""ALE実験における層水深の分布を描く

Usage: contour_dept.py FILE YMD K EXPNAME

Arguments:
  FILE     path of input file
  YMD      date for plot(YYYY-MM-DD)
  K        layer number for plot [0:km-1]
  EXPNAME  name of experiment

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
exp_name = args.get('EXPNAME')

logger.debug(date)

DS = xr.open_mfdataset(file_in)
logger.debug(DS)

da = DS["dep"].sel(time=date).isel(depth=klayer).squeeze()

ctitle = da.standard_name
#cunit = da.units
cunit = "m"
#da = ( da - da.mean().values ) * 1.e-2
da = da * 1.e-2

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(0.,60.1,20.), crs=proj )
ax.set_yticks( np.arange(10.,60.1,10.), crs=proj )
ax.set_extent((0., 60., 10., 60.), crs=proj )
#ax.set_xticks( np.arange(0.,100.1,20.), crs=proj )
#ax.set_yticks( np.arange(0.,60.1,10.), crs=proj )
#ax.set_extent((0., 100., 0., 62.), crs=proj )


#clevs=np.arange(-100.,100.1,1.)*1.
#llevs=np.arange(-100.,100.1,10.)*1.
clevs=np.arange(0.,200.1,1.)*3.
llevs=np.arange(0.,200.1,10.)*3.
da.plot.pcolormesh( transform=proj,
                    cmap=cm.jet_r, levels=clevs,
                    cbar_kwargs={'ticks':llevs,'shrink':0.7} )
cntr = da.plot.contour(transform=proj,levels=llevs, colors='black', linewidths=0.5  )
ax.clabel(cntr)

ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title(exp_name+' '+ctitle+'['+cunit+'] k='+str(klayer+1)+' '+date)
ax.set_xlabel('')
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
