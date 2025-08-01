#!/usr/bin/env python
"""JRA-3Qデータの領域平均を計算する

Usage: make_jra3q_ave.py

"""

import sys
sys.path.append('.')

import xarray as xr
import logging

#- local
from lib import xarray_maker
from data_heatflux import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

conf=confs[1]

DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
logger.debug(DS)

dshort = DS['DSWRF_surface'] - DS['USWRF_surface']
dlong = DS['DLWRF_surface'] - DS['ULWRF_surface']
dlatent = - DS['LHTFL_surface']
dsensible = - DS['SHTFL_surface']
dtotal = DS['DSWRF_surface'] - DS['USWRF_surface'] \
       + DS['DLWRF_surface'] - DS['ULWRF_surface'] \
       - DS['LHTFL_surface'] - DS['SHTFL_surface']

grid=xr.open_dataset('./seagrid_japansea.nc')['sea_land']

d1=dshort.where(grid==1.).mean(dim=["longitude","latitude"])
d2=dlong.where(grid==1.).mean(dim=["longitude","latitude"])
d3=dlatent.where(grid==1.).mean(dim=["longitude","latitude"])
d4=dsensible.where(grid==1.).mean(dim=["longitude","latitude"])
d5=dtotal.where(grid==1.).mean(dim=["longitude","latitude"])

ds2 = xr.Dataset({'short':d1,'long':d2,'latent':d3,'sensible':d4,'total':d5})

ds2.to_netcdf('./heatflux_ave.nc')

logger.info('OUTPUT: heatflux_ave.nc')
