#!/usr/bin/env python
"""MXEで計算した海峡通過流量を1つのnetCDFファイルにまとめる

Usage: make_strait_transport_netcdf.py

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

ncdir='../../link/data/JPN20-assim/anl_mon-jpn/strait/20*'
daj1=xr.open_mfdataset(ncdir+'/nc_tsugaru.20*')['vt'].sel(depth=1).squeeze()
daj2=xr.open_mfdataset(ncdir+'/nc_soya.20*')['vt'].sel(depth=1).squeeze()
daj3=xr.open_mfdataset(ncdir+'/nc_tsushima_e.20*')['vt'].sel(depth=1).squeeze()
daj4=xr.open_mfdataset(ncdir+'/nc_tsushima_w.20*')['vt'].sel(depth=1).squeeze()

nc2dir='../../link/data/MOVEJPN/anl_mon-jpn/strait/20*'
dam1=xr.open_mfdataset(nc2dir+'/nc_tsugaru.202*')['vt'].sel(depth=1).squeeze()
dam2=xr.open_mfdataset(nc2dir+'/nc_soya.202*')['vt'].sel(depth=1).squeeze()
dam3=xr.open_mfdataset(nc2dir+'/nc_tsushima_e.20*')['vt'].sel(depth=1).squeeze()
dam4=xr.open_mfdataset(nc2dir+'/nc_tsushima_w.20*')['vt'].sel(depth=1).squeeze()

time=np.append(daj1.time.values,pd.date_range(start='2020-01-01',freq='ME',periods=10))
time=np.append(time,dam1.time.values)

dummy_data=np.zeros(10)
dummy_data[:] = np.nan

v1=np.append(daj1.values,dummy_data)
v1=np.append(v1,dam1.values) * 1.e-12
da1 = xr.DataArray(data=v1,dims=('time'),attrs={'units':'Sv'})

v2=np.append(daj2.values,dummy_data)
v2=np.append(v2,dam2.values) * 1.e-12
da2 = xr.DataArray(data=v2,dims=('time'),attrs={'units':'Sv'})

v3=np.append(daj3.values,dummy_data)
v3=np.append(v3,dam3.values) * 1.e-12
da3 = xr.DataArray(data=v3,dims=('time'),attrs={'units':'Sv'})

v4=np.append(daj4.values,dummy_data)
v4=np.append(v4,dam4.values) * 1.e-12
da4 = xr.DataArray(data=v4,dims=('time'),attrs={'units':'Sv'})

ds = xr.Dataset(data_vars={'tsugaru':da1,'soya':da2,'tsushima_e':da3,'tsushima_w':da4,},
                coords={'time':time},
                attrs={'model_name':'MOVE-JPN',})
ds.to_netcdf('strait_transport.nc')

