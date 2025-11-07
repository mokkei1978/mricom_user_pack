#!/usr/bin/env python
"""流速分布を描く

Usage: vec_uv.py YM DEPTH

Arguments:
  YM  date for plot(YYYYMM)
  DEPTH depth for plot [m]
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
date = args.get('YM')
depth_m = args.get('DEPTH')
logger.debug(date)

year=date[0:4]
DSu = xarray_maker.open_dataset('../../link/data/JPN20-assim/hst_mon-jpn/nc_u/'+year+'/nc_u.'+date,'mricom-history')
DSv = xarray_maker.open_dataset('../../link/data/JPN20-assim/hst_mon-jpn/nc_v/'+year+'/nc_v.'+date,'mricom-history')

logger.debug(DSu)

#u_cmps = DSu['uo'].sel(time=date,lev=depth_m).squeeze()
#v_cmps = DSv['vo'].sel(time=date,lev=depth_m).squeeze()
u_cmps = DSu['uo'].sel(lev=depth_m).squeeze()
v_cmps = DSv['vo'].sel(lev=depth_m).squeeze()
speed_cmps = np.sqrt( u_cmps**2 + v_cmps**2 )

im=u_cmps.shape[1]
jm=u_cmps.shape[0]
ilist=list(range(0,im-1,10))
jlist=list(range(0,jm-1,10))
u2_cmps = u_cmps[jlist,ilist]
v2_cmps = v_cmps[jlist,ilist]
speed2_cmps = speed_cmps[jlist,ilist]
u2_cmps = u2_cmps / speed2_cmps
v2_cmps = v2_cmps / speed2_cmps
lon_deg = u2_cmps.lon.values
lat_deg = u2_cmps.lat.values
u2_cmps = np.where( speed2_cmps > 10. , u2_cmps, np.nan )

fig = plt.figure(figsize=(12,8))
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()
ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

speed_cmps.plot.contourf(transform=proj,cmap=cm.Oranges)
#cntr = ax.contourf(lon_deg,lat_deg,mag_cmps,transform=proj,cmap=cm.Oranges)
#fig.colorbar(cntr)

Q = ax.quiver(lon_deg,lat_deg,u2_cmps,v2_cmps,color='black',transform=proj,scale=50)

ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title( 'velocity [cm/s] '+depth_m+'m '+date )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
plt.savefig('uv_'+depth_m+'_'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
