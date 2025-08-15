#!/usr/bin/env python
"""水温の深度・時間ホフメラー図を描く

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

fig, ax = plt.subplots()

clevs=np.arange(0.,30.1,2.)
da.plot.pcolormesh( x='time',y='lev',
                    cmap=cm.jet, levels=np.arange(-2.,32.1,1.),
                    cbar_kwargs={'ticks':clevs} )
cntr = da.plot.contour(x='time',y='lev',levels=clevs, colors="black", linewidths=0.5)
ax.clabel(cntr)

ax.set_ylim( da.lev.max(), da.lev.min() )
ax.set_title('T Japan Sea (All)')

plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
