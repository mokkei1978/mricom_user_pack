#!/usr/bin/env python
"""SST分布を描く

Usage: contour_sst.py

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
import cartopy.feature as cfeature
from lib import xarray_maker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#logger.info('START')

DS = xarray_maker.open_dataset('../../link/data/MGDSST/month/2015/nc_sst.*','mricom-history')
DSn = xarray_maker.open_dataset('../../link/data/MGDSST/month/norm/nc_sst.2*','mricom-history')
logger.debug(DS)

da = DS['thetao'].sel(time=slice('2015-10','2015-12')).mean(dim='time')
dan = DSn['thetao'].sel(time=slice('2004-10','2004-12')).mean(dim='time')
da = da - dan

#da = da.rolling(lat=3,center=True).mean().rolling(lon=3,center=True).mean()
da = da.rolling(lat=3,center=True).mean()
 
fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=-160.) )
proj = ccrs.PlateCarree(central_longitude=0.)

ax.set_xticks(np.arange(-180,180.1,60),crs=proj)
ax.set_yticks(np.arange(-90,90.1,30),crs=proj)

#ax.add_feature(cfeature.LAND,color='gray', edgecolor='black',hatch='///')
#ax.coastlines(lw=0.5)

da.plot.pcolormesh( transform=proj,
                    cbar_kwargs={'orientation':'horizontal','shrink':0.5,'ticks':(1.,2.,3.,4.),'label':''},
                    cmap=cm.binary, levels=np.arange(0.5,4.1,0.5) )

da.plot.contour(transform=proj,levels=[1.,3.], colors="black", linewidths=0.2 )
cntr = da.plot.contour(transform=proj,levels=[2.,4.], colors="black", linewidths=0.2 )
ax.clabel(cntr)

ax.patch.set_facecolor('lightgray')
ax.add_feature(cfeature.LAND,color='lightgray') #,hatch='x')
ax.coastlines(lw=0.5)
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title('')
ax.set_xlabel('')
ax.set_ylabel('')
plt.tick_params(labelsize=10)

#xr.plot.pcolormesh(da,'lont','latt',

#plt.show()
#plt.savefig('sst'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight',dpi=200)
logger.info('OUTPUT: temp.png')

