#!/usr/bin/env python
"""SST水平平均値の時系列を計算する

Usage: make_sst_ave.py NDATA

Arguments:
  NDATA date number (see data.py)
"""

import sys
sys.path.append('.')

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

da = DS["thetao"].sel(lon=slice(128,140),lat=slice(35,42))
if ndata == 2 :
    da = da.isel(depth=0).squeeze()
undef = conf.get('undef',0.)
if undef != 0. :
    da = da.where( da != undef )

da.mean(dim=["lon","lat"]).to_netcdf(path='./sst_ave.nc',mode='w')

logger.info('OUTPUT: ./sst_ave.nc')
