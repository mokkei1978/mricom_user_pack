#!/usr/bin/env python
'''MGDSSTの各格子各月の線形トレンドを求める
'''
import xarray as xr
import numpy as np
from lib import xarray_maker

DS = xarray_maker.open_dataset('../../link/data/MGDSST/month/30yrs/*/nc_sst.*','mricom-history')
da = DS.thetao

dso = xr.Dataset(coords={'lon':DS.lon,'lat':DS.lat},
                 attrs={'data':'MGDSST',})
year=np.arange(-14.5,15.5,1.0)
for label,group in da.groupby('time.month'):
    dam = group
    dam['time'] = year
    dso[f't{label:02}'] = dam.polyfit(dim='time',deg=1).polyfit_coefficients

dso.to_netcdf(path='mgdsst_trend.nc',mode='w')
