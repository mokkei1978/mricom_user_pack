#!/usr/bin/env python
"""海洋熱波しきい値水平平均値の時系列を計算する

Usage: make_heatwave_thres_ave.py
"""

import sys
sys.path.append('.')

import xarray as xr
import pandas as pd
import logging
from lib import xarray_maker
from data import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

DS = xr.open_mfdataset('../../link/data/netCDF/MGDSST/heatwave/mgdsst365_jpn_thre_11win_1991-2020.nc')
logger.debug(DS)
grid=xr.open_dataset( 'nc/japansea_all/seagrid_mgd.nc' )['sea_land']
da = DS['tos'].where(grid==1.).mean(dim=['lon','lat'])

dan = da # no leap year

dal1=da.isel(time=range(59))
dal2=da.isel(time=range(58,60)).mean()
dal2['time'] = da.isel(time=58)['time']
dal3=da.isel(time=range(59,365))
dal=xr.concat([dal1,dal2,dal3],dim='time')

for year in range(1982,2026):
    logger.debug(year)
    if ( year % 4 ) == 0:
        dao = dal.copy()
    else:
        dao = dan.copy()

    dao['time']=pd.date_range(start=str(year)+'-01-01',end=str(year)+'-12-31')
    logger.debug(dao)

    if year == 1982:
        daout = dao.copy()
    else:
        daout = xr.concat([daout,dao],dim='time')

    logger.debug(daout)

fileo='./heatwave_thres_ave.nc'
daout.to_netcdf(path=fileo,mode='w')
logger.info('OUTPUT: '+fileo)
