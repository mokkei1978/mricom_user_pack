#!/usr/bin/env python
"""輸送量日別値から月別値の値を計算する（重みをUsui and Hiroseにならう）

Usage: make_trans_month.py

"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
from docopt import docopt
import logging
import pandas as pd
import calendar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

ds=xr.open_dataset('../../link/data/MOVEJPN/anl_day-jpn/strait_t/trans_temp.nc')

ym = []
last_day = []
for year in range(2022,2025):
    for month in range(1,13):
        ym.append(f'{year}-{month:02}')
        last_day.append(f'{calendar.monthrange(year,month)[1]:02}')

ymd = []
for i in range(len(ym)-1):
    ymd.append(ym[i]+'-'+last_day[i])
dso=xr.Dataset(coords={'time':pd.to_datetime(ymd)})

varnames = list(ds.data_vars)
da=ds[varnames[0]]
dout = np.zeros((len(varnames),len(ym)-1))
for i in range(len(ym)-1):
    nm1=da.sel(time=ym[i]).size
    nm2=da.sel(time=ym[i+1]).size
    nm3=min([nm1,nm2])

    wgt1=[]
    for j in range(nm1+nm2) :
        if j <= nm3 -1 :
            wgt1 += [j+1]
        elif nm3 - 1 < j <= nm1 - 1 :
            wgt1 += [nm3]
        elif nm1 - 1 < j < nm1 + nm3 - 1 :
            wgt1 += [nm1+nm3-j-1]
        else :
            wgt1 += [0]

    wgt2=[0]
    wgt2 += wgt1[0:-1]
    wgt=( np.array(wgt1) + np.array(wgt2) ) * 0.5 / nm3 / nm1

    for index, vname in enumerate(varnames):
        dout[index,i] = np.sum(ds[vname].sel(time=slice(ym[i],ym[i+1])).values*wgt)

for index, vname in enumerate(varnames):
    dso[vname] = ('time',dout[index,:])

dso.to_netcdf(path='trans_month.nc',mode='w')
logger.info('OUTPUT: trans_month.nc')
