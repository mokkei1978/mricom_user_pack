#!/usr/bin/env python
"""ある緯度での鉛直積分南北速度 vm の東西分布を、複数実験で重ねて描く（GrADS形式ヒストリー）

Usage: section_vm_grads.py YMD LAT LONMAX DIR...

Arguments:
  YMD     date for plot(YYYY-MM-DD)
  LAT     latitude of the section [deg]
  LONMAX  eastern limit of the plot [deg] (e.g., 15 to zoom into the western boundary)
  DIR     directories of history output (e.g., .../result/EXP/hst_day-main).
          The experiment name in the legend is taken from the parent directory.

"""

import sys
sys.path.append('.')

import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from docopt import docopt
from lib.mricom import open_grads

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
date = args.get('YMD')
lat = float(args.get('LAT'))
lonmax = float(args.get('LONMAX'))
dirs = args.get('DIR')

fig, ax = plt.subplots()

for diri in dirs:
    exp_name = os.path.basename(os.path.dirname(os.path.normpath(diri)))
    dv = open_grads(diri+'/hs_sfc_vm.ctl')["vm"].sel(time=date).squeeze()
    sec = dv.sel(lat=lat, method='nearest').sel(lon=slice(None, lonmax))
    logger.debug(sec)
    ax.plot(sec.lon, sec*1.e-5, marker='o', label=exp_name)

ax.axhline(0., color='gray', lw=0.5)
ax.set_xlabel('longitude [deg]')
ax.set_ylabel('vm [10$^5$ cm$^2$/s]')
ax.set_title('depth-integrated v at {:.1f}N, {}'.format(float(sec.lat), date))
ax.legend()

plt.savefig('temp.png', bbox_inches='tight', dpi=200)

logger.info('OUTPUT: temp.png')
