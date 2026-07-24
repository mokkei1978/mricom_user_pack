#!/usr/bin/env python
"""MODIS衛星観測によるクロロフィルa分布を季節平均で描く

Usage: plot_chla-season.py FILE

Arguments:
  FILE path of input file (複数ファイル/globパターンも可。月別クライマトロジー
       ファイル(AQUA_MODIS.*.L3m.MC.CHL.chlor_a.*.nc)を入力し、季節
       (DJF/MAM/JJA/SON)ごとに月をまとめて平均して出力する)
"""

import sys
sys.path.append('.')

import re

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

MONTH_TO_SEASON = {
    12: 'DJF', 1: 'DJF', 2: 'DJF',
    3: 'MAM', 4: 'MAM', 5: 'MAM',
    6: 'JJA', 7: 'JJA', 8: 'JJA',
    9: 'SON', 10: 'SON', 11: 'SON',
}

DATE_RE = re.compile(r'\.(\d{4})(\d{2})\d{2}_(\d{4})\d{4}\.')


def preprocess(ds):
    fname = ds.encoding['source']
    y0, mm, y1 = DATE_RE.search(fname).groups()
    month = int(mm)
    return ds.expand_dims(month=[month]).assign_coords(
        season=('month', [MONTH_TO_SEASON[month]]),
        yr_start=('month', [int(y0)]),
        yr_end=('month', [int(y1)]),
    )


DS = xr.open_mfdataset(file_in, combine='nested', concat_dim='month', preprocess=preprocess)
logger.debug(DS)

da = DS['chlor_a']

y0 = int(DS['yr_start'].min())
y1 = int(DS['yr_end'].max())

da_season = da.groupby('season').mean('month', keep_attrs=True)

proj = ccrs.PlateCarree()
vmax = 2.e0

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
        cbar_kwargs={'ticks': np.arange(0, vmax + 1.e-4, 2.e-1)}
    )

    ax.coastlines()
    ax.set_xticks( np.arange(120.,160.1,10.), crs=proj )
    ax.set_yticks( np.arange(20.,50.1,5.), crs=proj )
    ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
    ax.yaxis.set_major_formatter( LatitudeFormatter() )

    ax.set_title(f'Chlorophyll-a ({season}, {y0}-{y1})')

    ax.set_xlabel('')
    ax.set_ylabel('')

    fname = f'chla_{y0}-{y1}_{season}.png'
    plt.savefig(fname, bbox_inches='tight')
    plt.close(fig)

    logger.info(f'OUTPUT: {fname}')
