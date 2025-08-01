#!/usr/bin/env python
"""JRA-3Qの平年値ファイルを作る

Usage: make_jra3q_clim.py

"""

import sys
sys.path.append('.')

import xarray as xr
import pandas as pd
import logging

#- local
from lib import xarray_maker
from data_heatflux import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

time = pd.DatetimeIndex(['2020-01-01', '2020-02-01', '2020-03-01','2020-04-01', '2020-05-01', '2020-06-01','2020-07-01', '2020-08-01', '2020-09-01','2020-10-01', '2020-11-01', '2020-12-01',])

conf=confs[1]
DS = xarray_maker.open_dataset(conf["file"],conf['kind'])
logger.debug(DS)
dclim = DS.groupby(DS['time.month']).mean().rename({'month':'time'})
dclim['time'] = time

dclim.to_netcdf(path='./clim.nc',mode='w')

logger.info('OUTPUT: clim.nc')
