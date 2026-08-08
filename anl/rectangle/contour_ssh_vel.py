#!/usr/bin/env python
"""SSH分布と速度ベクトルを描く

Usage: contour_ssh_vel.py YMD EXPNAME

Arguments:
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
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
date = args.get('YMD')
exp_name = args.get('EXPNAME')

logger.debug(date)

diri='../../link/data/rectangle/result/kida09/hst_day-main'
year='1901'

DS = xr.open_mfdataset(diri+'/nc_ssh.'+year)
logger.debug(DS)

DSu = xr.open_mfdataset(diri+'/nc_u.'+year)
DSv = xr.open_mfdataset(diri+'/nc_v.'+year)

da = DS["zos"].sel(time=date).squeeze()
du = DSu["uo"].sel(time=date).isel(depth=0).squeeze()
dv = DSv["vo"].sel(time=date).isel(depth=0).squeeze()

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(0.,60.1,10.), crs=proj )
ax.set_yticks( np.arange(10.,60.1,10.), crs=proj )
ax.set_extent((0., 60., 10., 60.), crs=proj )

da.plot.pcolormesh(transform=proj,levels=20 )
#ax.clabel(cntr)

ax.quiver(du.lon,du.lat,du,dv,color='black',transform=proj,pivot='mid',scale=500.)

ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title(exp_name+' SSH['+da.units+'] w/ 1st vel '+date)
ax.set_xlabel('')
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight')

logger.info('OUTPUT: temp.png')
