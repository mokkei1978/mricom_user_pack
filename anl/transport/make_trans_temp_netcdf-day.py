#!/usr/bin/env python
"""MXEで計算した温度輸送量を1つのnetCDFファイルにまとめる: daily

Usage: make_trans_temp_netcdf-day.py

"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

subdir='heat_200m/north_japan_sea-adv'
ncdir='../../link/data/JPN20-assim/anl_day-jpn/'+subdir+'/20*'
daj1=xr.open_mfdataset(ncdir+'/nc_trans_t-e.20*')['vt'].sel(depth=1).squeeze()
daj2=xr.open_mfdataset(ncdir+'/nc_trans_t-s.20*')['vt'].sel(depth=1).squeeze()

nc2dir='../../link/data/MOVEJPN/anl_day-jpn/'+subdir+'/20*'
dam1=xr.open_mfdataset(nc2dir+'/nc_trans_t-e.20*')['vt'].sel(depth=1).squeeze()
dam2=xr.open_mfdataset(nc2dir+'/nc_trans_t-s.20*')['vt'].sel(depth=1).squeeze()

time=np.append(daj1.time.values,pd.date_range(start='2020-01-01',freq='D',periods=301))
time=np.append(time,dam1.time.values)

dummy_data=np.zeros(301)
dummy_data[:] = np.nan

v1=np.append(daj1.values,dummy_data)
v1=np.append(v1,dam1.values) * 1.e-6
da1 = xr.DataArray(data=v1,dims=('time'),attrs={'units':'C m3/s'})

v2=np.append(daj2.values,dummy_data)
v2=np.append(v2,dam2.values) * 1.e-6
da2 = xr.DataArray(data=v2,dims=('time'),attrs={'units':'C m3/s'})

ds = xr.Dataset(data_vars={'east':da1,'south':da2,},
                coords={'time':time},
                attrs={'model_name':'MOVE-JPN',})
ds.to_netcdf('trans_temp.nc')

logger.info('END: Output trans_temp.nc')
