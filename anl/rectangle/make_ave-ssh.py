#!/usr/bin/env python
"""時間平均値を求める (SSH)

Usage: make_ave-ssh.py YEAR

Arguments
  YEAR  year
"""

import sys
sys.path.append('.')

import xarray as xr
import pandas as pd
import logging
from lib import xarray_maker
from docopt import docopt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
year = args.get('YEAR')
file_in = '../../link/data/rectangle/result/npl02-org-03/hst_day-main/nc_ssh.'+year
file_out = 'nc_ssh.'+year

time = pd.DatetimeIndex([year+'-01-01'])

DS = xarray_maker.open_dataset(file_in, 'mricom-history')
logger.debug(DS)
dave = DS.mean(dim='time').expand_dims(time=time)

dave.to_netcdf(path=file_out, mode='w')

logger.info('OUTPUT: %s', file_out)
