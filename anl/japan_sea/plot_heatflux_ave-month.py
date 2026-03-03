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

da=xr.open_dataset('nc/japansea_all/heatflux_ave_usui.nc')[varname]
da2=xr.open_dataset('nc/japansea_all/heatflux_ave_month.nc')[varname]
da2['time'] = da2.time + pd.to_timedelta(14,unit='D')
                                          
fig, ax = plt.subplots()

da.plot.line()
da2.plot.line()

plt.legend()
ax.set_title( 'Heat flux over Japan Sea: '+varname )
ax.set_xlabel('')
ax.set_ylabel('[W/m2]')

ax.set_xlim(pd.to_datetime('2022-01-01'),pd.to_datetime('2024-12-31'))

#plt.savefig('heatflux_ave-'+varname+'.png', bbox_inches='tight')
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
