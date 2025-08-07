#!/usr/bin/env python
"""SST水平平均値(領域は data.py のseagrid)の時系列を計算する

Usage: make_sst_ave.py NDATA

Arguments:
  NDATA date number (see data.py)
"""

import sys
sys.path.append('.')

import xarray as xr
from docopt import docopt
import logging
from lib import xarray_maker
from data import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )
logger.debug(ndata)

conf=confs[ndata]

DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
logger.debug(DS)

seagrid = { 'HIMSST':'him',
            'MGDSSTnorm':'mgd',
            'MGDSST':'mgd',
            'MOVEJPN':'jpn', }
dataname=seagrid[conf['name']]
grid=xr.open_dataset( 'nc/japansea_north/seagrid_' + dataname + '.nc' )['sea_land']

da = DS["thetao"]
if ndata == 2 :
    da = da.isel(depth=0).squeeze()
if ndata == 0 :
    da = da.where( da != 88.8 )
undef = conf.get('undef',0.)
if undef != 0. :
    da = da.where( da != undef )

fileo='./sst_ave.nc'
da.where(grid==1.).mean(dim=["lon","lat"]).to_netcdf(path=fileo,mode='w')

logger.info('OUTPUT: '+fileo)
