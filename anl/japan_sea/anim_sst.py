#!/usr/bin/env python
"""アニメーション用にSST分布を連番で描く

Usage: contour_sst.py NDATA YMD

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

DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
logger.debug(DS)
#DSclim = xarray_maker.open_dataset(confs[1]["file"],confs[1]['kind'])

da = DS["thetao"]
if ndata == 5 :
    da = da.isel(lev=6) #.squeeze()
undef = conf.get('undef',0.)
if undef != 0. :
    da = da.where( da != undef )

fig = plt.figure(figsize=(16,10))

#da.sel(time=it).squplot.pcolormesh( transform=proj,
#                    cmap=cm.jet, levels=np.arange(-1.,30.1,1.) )

for it in da['time']:
    ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
    proj = ccrs.PlateCarree()
    ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
    ax.set_yticks( np.arange(35.,45.1,5.), crs=proj )
    ax.set_extent( (128., 140., 35., 45.), crs=proj )
    da.sel(time=it).squeeze().plot.pcolormesh( transform=proj,
                    cmap=cm.jet, levels=np.arange(-1.,30.1,1.) )
#cntr = da.plot.contour(transform=proj,levels=20, colors="black" )
#ax.clabel(cntr)
    cdate = str(it.dt.strftime('%Y%m%d').values)
    ax.set_title( conf["name"]+' '+cdate )
    ax.coastlines()
    ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
    ax.yaxis.set_major_formatter( LatitudeFormatter() )
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.savefig('sst'+ cdate +'.png', bbox_inches='tight')
    plt.savefig('temp.png', bbox_inches='tight')
    plt.clf()




#plt.show()
#logger.info('OUTPUT: temp.png')
