#!/usr/bin/env python
"""海面熱フラックス偏差分布を描く

Usage: contour_heatflux_anom.py VARNAME YM

Arguments:
  VARNAME  variable name for plot (long/short/sensible/latent/total)
  YM       date for plot(YYYY-MM)
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
from data_heatflux import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
varname = args.get('VARNAME')
date = args.get('YM')
logger.debug(date)

conf=confs[0]

DSclim = xarray_maker.open_dataset(confs[2]["file"],confs[2]['kind'])
DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
logger.debug(DS)

dateclim = '2020-'+date.split('-')[1]

if ( varname == 'short' ):
    da = DS['DSWRF_surface'].sel(time=date).squeeze() - DS['USWRF_surface'].sel(time=date).squeeze()
    daclim = DSclim['DSWRF_surface'].sel(time=dateclim).squeeze() - DSclim['USWRF_surface'].sel(time=dateclim).squeeze()
elif ( varname == 'long' ):
    da = DS['DLWRF_surface'].sel(time=date).squeeze() - DS['ULWRF_surface'].sel(time=date).squeeze()
    daclim = DSclim['DLWRF_surface'].sel(time=dateclim).squeeze() - DSclim['ULWRF_surface'].sel(time=dateclim).squeeze()
elif ( varname == 'latent' ):
    da = - DS['LHTFL_surface'].sel(time=date).squeeze()
    daclim = - DSclim['LHTFL_surface'].sel(time=dateclim).squeeze()
elif ( varname == 'sensible' ):
    da = - DS['SHTFL_surface'].sel(time=date).squeeze()
    daclim = - DSclim['SHTFL_surface'].sel(time=dateclim).squeeze()
elif ( varname == 'total' ):
    da = DS['DSWRF_surface'].sel(time=date).squeeze() - DS['USWRF_surface'].sel(time=date).squeeze() \
       + DS['DLWRF_surface'].sel(time=date).squeeze() - DS['ULWRF_surface'].sel(time=date).squeeze() \
       - DS['LHTFL_surface'].sel(time=date).squeeze() \
       - DS['SHTFL_surface'].sel(time=date).squeeze()
    daclim = DSclim['DSWRF_surface'].sel(time=dateclim).squeeze() - DSclim['USWRF_surface'].sel(time=dateclim).squeeze() \
       + DSclim['DLWRF_surface'].sel(time=dateclim).squeeze() - DSclim['ULWRF_surface'].sel(time=dateclim).squeeze() \
       - DSclim['LHTFL_surface'].sel(time=dateclim).squeeze() \
       - DSclim['SHTFL_surface'].sel(time=dateclim).squeeze()

da = da - daclim

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(35.,50.1,5.), crs=proj )
ax.set_extent( (127., 143., 33., 50.), crs=proj )

da.plot.pcolormesh( transform=proj,
                    cmap=cm.RdYlBu_r, levels=np.arange(-100.,100.1,5.),
                    cbar_kwargs={'ticks':np.arange(-100.,100.1,10.)} )

cntr = da.plot.contour(transform=proj,levels=np.arange(-100.,100.1,10.), colors="black", linewidths=0.5)
ax.clabel(cntr)

ax.coastlines()
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title( conf["name"]+' heatflux anom '+varname+' [w/m2]'+date )
ax.set_xlabel('')
ax.set_ylabel('')

#plt.show()
plt.savefig('heatfluxa_'+date+'_'+varname+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
