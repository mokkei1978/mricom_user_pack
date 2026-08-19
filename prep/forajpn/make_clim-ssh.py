#!/usr/bin/env python
"""FORA-JPN60 (hst_mon-np) のSSH(海面高度)月毎平年値ファイルを作る

Usage: make_clim-ssh.py

"""

import sys
sys.path.append('.')

import xarray as xr
import pandas as pd
import logging
from lib import xarray_maker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

file_in = '/data01/sakamoto/FORA_JPN/hst_mon-np/nc_ssh/*/nc_ssh.*'
file_out = 'clim.nc'

time = pd.DatetimeIndex(['2020-01-01', '2020-02-01', '2020-03-01','2020-04-01', '2020-05-01', '2020-06-01','2020-07-01', '2020-08-01', '2020-09-01','2020-10-01', '2020-11-01', '2020-12-01',])

DS = xarray_maker.open_dataset(file_in, 'mricom-history')
logger.debug(DS)
dclim = DS.groupby(DS['time.month']).mean().rename({'month':'time'})
dclim['time'] = time

dclim.to_netcdf(path=file_out, mode='w')

logger.info('OUTPUT: %s', file_out)
