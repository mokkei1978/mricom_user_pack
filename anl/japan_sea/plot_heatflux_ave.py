#!/usr/bin/env python
"""海面熱フラックス領域平均値の時系列を描く

Usage: plot_heatflux_ave.py VARNAME

Arguments:
  VARNAME  variable name for plot (long/short/sensible/latent)

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
from data_heatflux import confs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
varname = args.get('VARNAME')

da=xr.open_dataset('./heatflux_ave.nc')[varname]

grouped=da.groupby("time.year")

labels={
     '2022':'1948-2022',
     '2023':'2023',
     '2024':'2024',
     '2025':'2025',}
colors={
     '2023':'orange',
     '2024':'red',
     '2025':'purple',}
widths={
     '2023':1.,
     '2024':1.,}

fig, ax = plt.subplots()

for year, group in grouped:
    dyear = group
    dyear["time"]=pd.to_datetime('2020-'+group.time.dt.strftime('%m-15').values)
    dyear.plot.line(xlim=[pd.Timestamp('2020-01-01'),pd.Timestamp('2020-12-31')],
                    label=labels.get(str(year),''),
                    color=colors.get(str(year),'gray'),linewidth=widths.get(str(year),0.5))

plt.legend()
ax.set_title( 'Heat flux over Japan Sea: '+varname )
ax.set_xlabel('')
ax.set_ylabel('[W/m2]')

plt.savefig('heatflux_ave-'+varname+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
