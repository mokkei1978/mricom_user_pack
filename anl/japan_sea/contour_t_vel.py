#!/usr/bin/env python
"""水温分布と流速ベクトルを重ねて描く

Usage: contour_t_vel.py YMD

Arguments:
  YMD   date for plot(YYYYMMDD)
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

#- local
from lib import xarray_maker
from data import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
cdate = args.get('YMD')

DSt = xarray_maker.open_dataset('../../link/data/netCDF/JPN/2023/nc_t.'+cdate,'mricom-history')
DSu = xarray_maker.open_dataset('../../link/data/netCDF/JPN/2023/nc_u.'+cdate,'mricom-history')
DSv = xarray_maker.open_dataset('../../link/data/netCDF/JPN/2023/nc_v.'+cdate,'mricom-history')
DS = DSu.assign(vo=DSv['vo']).isel(lev=8).squeeze()
da = DSt['thetao'].isel(lev=8).squeeze()

fig = plt.figure()#figsize=(10,8))

ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()
ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

da.plot.pcolormesh( transform=proj,
                    cmap=cm.jet, levels=np.arange(-1.,30.1,1.) )
cntr = da.plot.contour(transform=proj,levels=[10.], colors="black", linewidths=0.5 )
ax.clabel(cntr)

#DS.plot.quiver(x='lon',y='lat',u='uo',v='vo',color='black',transform=proj)
thin=10
ax.quiver(x=DS['lon'].values[::thin],y=DS['lat'].values[::thin],
          u=DS['uo'].values[::thin,::thin],v=DS['vo'].values[::thin,::thin],
          color='black',transform=proj, scale=15)

ax.set_title( 'T w/ velocity at 50m '+cdate )
ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_xlabel('')
ax.set_ylabel('')

plt.savefig('tvel_'+cdate+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
