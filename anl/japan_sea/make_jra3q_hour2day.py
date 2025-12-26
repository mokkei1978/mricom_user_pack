#!/usr/bin/env python
"""JRA-3Qデータの時別値を日別値に平均する

Usage: make_jra3q_hour2day.py YYYY MM

Arguments:
  YYYY       year
  MM         month (0 padding)

"""

import xarray as xr
import pandas as pd
from docopt import docopt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
year = args.get('YYYY')
month = args.get('MM')

DS = xr.open_mfdataset('../../link/data/jra3q/hour/'+year+month+'/nc_phy2m.2*')
logger.debug(DS)
ds2 = DS.groupby(DS['time.day']).mean().rename({'day':'time'})

nday = ds2.sizes['time']

time =[]
for n in range(nday):
    time.append(year+'-'+month+f'-{ds2.time.values[n]:02}')

ds2['time'] = pd.DatetimeIndex(time)

ds2.to_netcdf('./nc_phy2m.'+year+month)

#logger.info('OUTPUT: heatflux_ave.nc')
