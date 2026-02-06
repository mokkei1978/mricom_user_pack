#!/usr/bin/env python
"""MXEで計算した貯熱量を1つのnetCDFファイルにまとめる: 気候値

Usage: make_heat_cont_netcdf-clim.py

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

subdir='japan_sea_all'
ncdir='../../link/data/JPN20-assim/anl_mon-jpn/heat_btm/'+subdir+'/clim'
daj=xr.open_mfdataset(ncdir+'/nc_heat_cont.20*')['hc'].sel(depth=1).squeeze()

v1=daj.values * 1.e-6
da = xr.DataArray(data=v1,dims=('time'),attrs={'units':'C m3'})

ds = xr.Dataset(data_vars={'hc':da,},
                coords={'time':daj.time},
                attrs={'model_name':'MOVE-JPN',})
ds.to_netcdf('heat_cont.nc')

logger.info('END: Output heat_cont.nc')
