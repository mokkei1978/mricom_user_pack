#!/usr/bin/env python
"""層水深の分布と速度ベクトルを描く

Usage: contour_dept_vel.py YMD K EXPNAME

Arguments:
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

diri='../../link/data/rectangle/result/kida12/hst_day-main'
year='1901'

DS = xr.open_mfdataset(diri+'/nc_dept.'+year)
logger.debug(DS)

da = DS["dep"].sel(time=date).isel(depth=klayer).squeeze()

DSu = xr.open_mfdataset(diri+'/nc_u.'+year)
DSv = xr.open_mfdataset(diri+'/nc_v.'+year)
du = DSu["uo"].sel(time=date).isel(depth=klayer).squeeze()
dv = DSv["vo"].sel(time=date).isel(depth=klayer).squeeze()

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
clevs=np.arange(0.,600.1,10.)*1.
llevs=np.arange(0.,600.1,50.)*1.
da.plot.pcolormesh( transform=proj,
                    cmap=cm.jet_r, levels=clevs,
                    cbar_kwargs={'ticks':llevs,'shrink':0.7} )
cntr = da.plot.contour(transform=proj,levels=llevs, colors='black', linewidths=0.5  )
ax.clabel(cntr)

ax.quiver(du.lon,du.lat,du,dv,color='black',transform=proj,pivot='mid',scale=100.)

ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title(exp_name+' '+ctitle+'['+cunit+'] k='+str(klayer+1)+' '+date)
ax.set_xlabel('')
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
