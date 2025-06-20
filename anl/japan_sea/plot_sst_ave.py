#!/usr/bin/env python
"""SST水平平均値の時系列を描く(make_sst_ave.py の出力を使う)

Usage: plot_sst_ave.py NDATA

Arguments:
  NDATA date number (see data.py)
"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from docopt import docopt
import logging
import pandas as pd
import matplotlib.dates as mdates

#- local
from lib import xarray_maker
from data import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
ndata = int( args.get('NDATA') )
logger.debug(ndata)

conf=confs[ndata]

dm=xr.open_dataset('sst_ave.nc')
#dm_norm=xr.open_dataset('sst_ave_norm.nc')

grouped=dm.groupby("time.year")

colors={'2018':(0.4,0.4,1.),
     '2019':(0.5,0.5,1.),
     '2020':(0.6,0.6,1.),
#     '2021':(0.7,0.7,1.),
     '2021':'yellow',
     '2022':(0.8,0.8,1.),
     '2023':'orange',
     '2024':'red',
     '2025':'purple',}

fig, ax = plt.subplots()

#dm_norm["time"]=pd.to_datetime('2020-'+dm_norm.time.dt.strftime('%m-%d').values)
#dm_norm["thetao"].plot.line(xlim=[pd.Timestamp('2020-01-01'),pd.Timestamp('2020-12-31')],
#                              label='norm', color='black', linewidth=2 )

for year, group in grouped:
    logger.debug(colors.get(str(year)))
    dyear = group
    dyear["time"]=pd.to_datetime('2020-'+group.time.dt.strftime('%m-%d').values)
    dyear["thetao"].plot.line(xlim=[pd.Timestamp('2020-01-01'),pd.Timestamp('2020-12-31')],
                              label=str(year), color=colors.get(str(year)))

plt.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.set_title( conf["name"]+' Japan Sea' )
ax.set_xlabel('')
ax.set_ylabel('C')

#plt.show()
#plt.savefig('sst'+date+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
