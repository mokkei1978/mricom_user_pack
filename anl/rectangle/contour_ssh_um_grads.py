#!/usr/bin/env python
"""SSH分布と鉛直積分した速度ベクトルを描く（GrADS形式ヒストリー）

Usage: contour_ssh_um_grads.py DIR YMD EXPNAME

Arguments:
  DIR  directory of history output (e.g., .../result/EXP/hst_day-main)
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
from lib.mricom import open_grads

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
diri = args.get('DIR')
date = args.get('YMD')
exp_name = args.get('EXPNAME')

da = open_grads(diri+'/hs_ssh.ctl')["zos"].sel(time=date).squeeze()
du = open_grads(diri+'/hs_sfc_um.ctl')["um"].sel(time=date).squeeze()
dv = open_grads(diri+'/hs_sfc_vm.ctl')["vm"].sel(time=date).squeeze()
logger.debug(da)

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()

ax.set_xticks( np.arange(0.,60.1,10.), crs=proj )
ax.set_yticks( np.arange(10.,60.1,10.), crs=proj )
ax.set_extent((-1., 61., 9., 61.), crs=proj )

da.plot.pcolormesh(transform=proj, cmap='RdBu_r', center=0.,
                   cbar_kwargs={'label':'SSH [cm]'} )

ax.quiver(du.lon,du.lat,du,dv,color='black',transform=proj,pivot='mid')

ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )
ax.set_title(exp_name+' SSH w/ depth-integrated vel. '+date)
ax.set_xlabel('')
ax.set_ylabel('')

plt.savefig('temp.png', bbox_inches='tight',dpi=200)

logger.info('OUTPUT: temp.png')
