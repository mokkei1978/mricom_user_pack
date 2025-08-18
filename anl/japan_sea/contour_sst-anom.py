#!/usr/bin/env python
"""SST偏差分布を描く

Usage: contour_sst-anom.py NDATA YMD

Arguments:
  NDATA date number (see data.py)
  YMD   date for plot(YYYY-MM-DD)
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
#logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )
date = args.get('YMD')
logger.debug(date)

conf=confs[ndata]

DS = xarray_maker.open_dataset(conf['file'],conf['kind'])
logger.debug(DS)

DSclim = xarray_maker.open_dataset(confs[1]['file'],confs[1]['kind'])

da = DS['thetao'].sel(time=date).squeeze()
if ndata == 2 :
    da = da.isel(depth=0).squeeze()
undef = conf.get('undef',0.)
if undef != 0. :
    da = da.where( da != undef )

daclim = DSclim['thetao'].sel(time='2004-'+da['time'].dt.strftime('%m-%d').values).squeeze()
daclim = daclim.sel(lon=slice(127,143),lat=slice(33,50))
da2=da.sel(lon=slice(127,143),lat=slice(33,50)).interp(lon=daclim['lon'],lat=daclim['lat'])
da3 = da2 - daclim

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

da3.plot.pcolormesh( transform=proj,
                     cmap=cm.coolwarm, levels=np.arange(-8.,8.1,0.5) )

#- 流速ベクトルを加える
cdate='20230612'
DSu = xarray_maker.open_dataset('../../link/data/netCDF/JPN/2023/nc_u.'+cdate,'mricom-history')
DSv = xarray_maker.open_dataset('../../link/data/netCDF/JPN/2023/nc_v.'+cdate,'mricom-history')
DS = DSu.assign(vo=DSv['vo']).isel(lev=8).squeeze()
thin=10
ax.quiver(x=DS['lon'].values[::thin],y=DS['lat'].values[::thin],
          u=DS['uo'].values[::thin,::thin],v=DS['vo'].values[::thin,::thin],
          color='black',transform=proj, scale=15)

#cntr = da2.plot.contour(transform=proj,levels=np.arange(-8.,8.1,2), colors="black" )
#ax.clabel(cntr)

ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title( conf["name"]+' '+date )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
#plt.savefig('sst'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
