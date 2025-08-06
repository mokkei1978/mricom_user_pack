#!/usr/bin/env python
"""SST水平平均値から海洋熱波が起こっているかを判定する

Usage: judge_heatwave_ave.py
"""

import xarray as xr
import logging
from lib import xarray_maker
from data import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

ncdir='nc/japansea_all'
#sst=xr.open_dataset(ncdir+'/sst_ave_him.nc')['thetao']
sst=xr.open_dataset(ncdir+'/sst_ave_jpnv2.nc')['thetao']
thres=xr.open_dataset(ncdir+'/heatwave_thres_ave.nc')['tos']

logger.debug(thres)

d1= sst > thres
#d1 = d1.sel(time=d1['time.year']==2023)

d2 = d1.copy()
im = d1.shape[0]

##- 5日以上連続しないものを落とす
for i in range( im ):
    if not d1[i] :
        continue

    nsuc = 1
    for j in range(1,5):
        if i+j >= im :
            break
        if not d1[i+j] :
            break
        nsuc = nsuc + 1

    for j in range(1,5):
        if i-j < 0 :
            break
        if not d1[i-j] :
            break
        nsuc = nsuc + 1

    if nsuc < 5:
        logger.debug(i)
        logger.debug(nsuc)
        d2[i] = False

d3 = d2.copy()
##- 2日以下のギャップは一続きの海洋熱波とする
for i in range( 2, im-2 ):
    if d2[i] :
        continue

    nsuc = 1
    for j in range(1,3):
        if d2[i+j] :
            break
        nsuc = nsuc + 1

    for j in range(1,3):
        if d2[i-j] :
            break
        nsuc = nsuc + 1

    if nsuc <= 2:
        logger.debug(i)
        logger.debug(nsuc)
        d3[i] = True

d3.name='is_heatwave'
d3.to_netcdf(path='./is_heatwave_ave.nc',mode='w')
logger.info('OUTPUT: ./is_heatwave_ave.nc')
