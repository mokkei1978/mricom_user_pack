#!/usr/bin/env python
"""硝酸塩(NO3)分布を季節平均で描く

Usage: plot_no3-season.py FILE [VMAX]

Arguments:
  FILE path of input file (複数ファイル/globパターンも可。季節(DJF/MAM/JJA/SON)ごとに全期間平均して出力する)
  VMAX カラーバーの上限値 [mol m-3]。省略時は 1.e-1
"""

import sys
sys.path.append('.')

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from docopt import docopt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cmocean

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

args = docopt(__doc__)
file_in = args.get('FILE')
vmax_arg = args.get('VMAX')

DS = xr.open_mfdataset(file_in)
logger.debug(DS)

da = DS['no3'].sel(depth=1.).squeeze()

y0 = int(da.time.min().dt.year)
y1 = int(da.time.max().dt.year)

da_season = da.groupby('time.season').mean('time', keep_attrs=True)

proj = ccrs.PlateCarree()
vmax = float(vmax_arg) if vmax_arg is not None else 1.e-1

for season in ['DJF', 'MAM', 'JJA', 'SON']:
    if season not in da_season['season'].values:
        logger.warning(f'{season}: no data, skip')
        continue

    da_s = da_season.sel(season=season)

    fig = plt.figure()
    ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
    ax.set_extent((117., 160., 20., 52.), crs=proj )

    da_s.plot.pcolormesh(
        transform=proj, cmap='jet',
        vmin=0, vmax=vmax,
        cbar_kwargs={'ticks': np.arange(0, vmax + 1.e-4, 1.e-2), 'label': 'NO3 [mol m-3]'}
    )

    ax.coastlines()
    ax.set_xticks( np.arange(120.,160.1,10.), crs=proj )
    ax.set_yticks( np.arange(20.,50.1,5.), crs=proj )
    ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
    ax.yaxis.set_major_formatter( LatitudeFormatter() )

    ax.set_title(f'NO3 ({season}, {y0}-{y1})')

    ax.set_xlabel('')
    ax.set_ylabel('')

    fname = f'no3_{y0}-{y1}_{season}.png'
    plt.savefig(fname, bbox_inches='tight')
    plt.close(fig)

    logger.info(f'OUTPUT: {fname}')
