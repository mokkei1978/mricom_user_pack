#!/usr/bin/env python
"""表層の貯熱量分布を描く

Usage: contour_heat_content.py YM

Arguments:
  YM    date for plot(YYYY-MM)
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
#from data_month import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
date = args.get('YM')
logger.debug(date)

#DS = xr.open_mfdataset('../../link/data/MOVEJPN/anl_mon-jpn/heat_200m/202?/nc_t_integ_vert.2*')
DS = xr.open_mfdataset('../../link/data/JPN20-assim/anl_mon-jpn/heat_200m/clim/nc_t_integ_vert.2*')
logger.debug(DS)

da = DS["tz"].sel(time=date).squeeze()
da = 1.e-4 * da
#undef = conf.get('undef',0.)
#if undef != 0. :
#    da = da.where( da != undef )

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )


clevs=np.arange(0.,40.1,5.)
da.plot.pcolormesh( transform=proj,
                    cmap=cm.jet, levels=np.arange(0.,40.1,1.),
                    cbar_kwargs={'ticks':clevs,'label':''} )

cntr = da.plot.contour(transform=proj,levels=clevs, colors="black", linewidths=0.5)
ax.clabel(cntr)

ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title( ' Heat content (200m) [x100 C m] '+date )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
plt.savefig('heat_200m_'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
