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
#cdata='him'
cdata='mgd'
#cdata='jpnv2'
#cdata='movejpn'
sst=xr.open_dataset(ncdir+'/sst_ave_'+cdata+'.nc')['thetao']
thres=xr.open_dataset(ncdir+'/heatwave_thres_ave.nc')['tos']
trend=xr.open_dataset(ncdir+'/sst_trend_ave.nc')['trend']

logger.debug(thres)

#d1= sst > ( thres + trend )  #- トレンドを考慮
d1= sst > thres

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
fileo='./is_heatwave_ave_'+cdata+'.nc'
d3.to_netcdf(path=fileo,mode='w')
logger.info('OUTPUT: '+fileo)
