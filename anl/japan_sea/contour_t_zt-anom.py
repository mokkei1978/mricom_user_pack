#!/usr/bin/env python
"""水温鉛直時間分布を描く

Usage: contour_t_zt.py FILE

Arguments:
  FILE path of input file
"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from docopt import docopt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
file_in = args.get('FILE')

DS = xr.open_dataset(file_in)
logger.debug(DS)

da = DS["thetao"].sel(lev=slice(1,200))
da = da.sel(time=slice('2022-01','2022-12'))

DSclim = xr.open_dataset('nc/japansea_all/t_3d_ave_clim.nc')
daclim = DSclim["thetao"].sel(lev=slice(1,200))
danm = da.copy()

#for it in range(da.shape[0]):
for it in da['time']:
    danm.loc[{'time':it}] -= daclim.sel(time='2008-'+ str(it.time.dt.month.values) ).squeeze()

fig, ax = plt.subplots()

clevs=np.arange(0.,30.1,2.)
danm.plot.pcolormesh( x='time',y='lev',
                    cmap=cm.coolwarm, levels=np.arange(-4.,4.1,0.25) )
#                    cbar_kwargs={'ticks':clevs} )
cntr = da.plot.contour(x='time',y='lev',levels=clevs, colors="black", linewidths=0.5)
#ax.clabel(cntr)

ax.set_ylim( da.lev.max(), da.lev.min() )
ax.set_title('Tanomaly Japan Sea (All)')

plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
