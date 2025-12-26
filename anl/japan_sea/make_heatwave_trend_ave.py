#!/usr/bin/env python
"""海洋熱波しきい値用に、SST水平平均値のトレンド時系列を計算する

Usage: make_heatwave_trend_ave.py
"""

import xarray as xr
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

ds=xr.open_dataset('../../link/data/MGDSST/heatwave/mgdsst_trend.nc')
grid=xr.open_dataset( 'nc/japansea_all/seagrid_mgd.nc' )['sea_land']

#- 月データフレームを作る
data_m=np.zeros(13)
for month in range(1,13):
    data_m[month-1] = ds[f't{month:02}'].where(grid==1.).mean(dim=['lon','lat'])[0].values
data_m[12] = data_m[0]

print(data_m[:12])

dates_m = pd.date_range(start='2004-01-01', periods=13, freq='MS')
df_monthly = pd.DataFrame({'trend': data_m}, index=dates_m)

#- 日毎xarrayデータを作る
df = df_monthly.resample('D').interpolate(method='linear')
df = df[ (df.index.year !=2005) ]
#print(df.head(61))

dal = df.to_xarray().rename({'index':'time',})
dan = df[(df.index.month !=2)|(df.index.day !=29)].to_xarray().rename({'index':'time',})

for year in range(1982,2026):
    if ( year % 4 ) == 0:
        dao = dal.copy()
    else:
        dao = dan.copy()
    dao['time']=pd.date_range(start=str(year)+'-01-01',end=str(year)+'-12-31')
    dao['trend'] = dao.trend*(float(year)-2005.5)

    if year == 1982:
        daout = dao.copy()
    else:
        daout = xr.concat([daout,dao],dim='time')

fileo='./sst_trend_ave.nc'
daout.to_netcdf(path=fileo,mode='w')
logger.info('OUTPUT: '+fileo)
