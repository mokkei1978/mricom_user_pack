#!/usr/bin/env python
"""SST水平平均値の時系列を描く(make_sst_ave.py の出力を使う)

Usage: plot_heatwave.py YEAR

Arguments:
  YEAR  year to plot

"""

import sys
sys.path.append('.')

import xarray as xr
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import cm
from docopt import docopt
import logging
import pandas as pd
import matplotlib.dates as mdates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
year = int( args.get('YEAR') )
logger.debug(year)

#dm=xr.open_dataset('nc/sst_ave.nc')
#dh=xr.open_dataset('nc/is_heatwave_ave.nc')
dm=xr.open_dataset('nc/sst_ave_him.nc')
dh=xr.open_dataset('nc/is_heatwave_ave_him.nc')
dnorm=xr.open_dataset('nc/sst_ave_norm.nc')['thetao']
if year % 4 != 0 :
    dnorm=dnorm.drop_sel(time='2004-02-29')
dnorm["time"]=pd.to_datetime(str(year)+'-'+dnorm.time.dt.strftime('%m-%d').values)

fig, ax = plt.subplots()

da=dm['thetao'].sel(time=dm['time.year']==year)
dh=dh['is_heatwave'].sel(time=dh['time.year']==year)

da.plot.line(color='red', label=str(year))

for i in range(dh.shape[0]-1):
    if not dh[i]:
        continue
    ax.axvspan(dh['time'].isel(time=i).dt.strftime('%Y-%m-%d').values, dh['time'].isel(time=i+1).dt.strftime('%Y-%m-%d').values, color='yellow', alpha=0.4)

dnorm.plot.line(color='gray',label='normal')

plt.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.set_title( 'SST Japan Sea' )
ax.set_xlabel('')
ax.set_ylabel('C')

#plt.show()
plt.savefig('heatwave_'+str(year)+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
