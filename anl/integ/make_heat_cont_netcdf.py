#!/usr/bin/env python
"""MXEで計算した貯熱量を1つのnetCDFファイルにまとめる

Usage: make_heat_cont_netcdf.py

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

subdir='north_japan_sea'
ncdir='../../link/data/JPN20-assim/anl_mon-jpn/heat_50m/'+subdir+'/20*'
daj=xr.open_mfdataset(ncdir+'/nc_heat_content.20*')['hc'].sel(depth=1).squeeze()

nc2dir='../../link/data/MOVEJPN/anl_mon-jpn/heat_50m/'+subdir+'/20*'
dam=xr.open_mfdataset(nc2dir+'/nc_heat_content.20*')['hc'].sel(depth=1).squeeze()

time=np.append(daj.time.values,pd.date_range(start='2020-01-01',freq='ME',periods=10))
time=np.append(time,dam.time.values)

dummy_data=np.zeros(10)
dummy_data[:] = np.nan

v1=np.append(daj.values,dummy_data)
v1=np.append(v1,dam.values) * 1.e-6
da = xr.DataArray(data=v1,dims=('time'),attrs={'units':'C m3'})

ds = xr.Dataset(data_vars={'hc':da,},
                coords={'time':time},
                attrs={'model_name':'MOVE-JPN',})
ds.to_netcdf('heat_cont.nc')

logger.info('END: Output heat_cont.nc')
