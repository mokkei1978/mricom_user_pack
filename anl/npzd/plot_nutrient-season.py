#!/usr/bin/env python
"""World Ocean Atlas 2023 栄養塩(硝酸塩・リン酸塩など)気候値の海面値を季節平均で描く

Usage: plot_nutrient-season.py FILE [VMAX]

Arguments:
  FILE path/globパターン of input files (月別クライマトロジーファイル
       woa23_all_{c}01_01.nc 〜 woa23_all_{c}12_01.nc (c は要素記号1文字、
       例えば硝酸塩なら n, リン酸塩なら p) を含むディレクトリ内のファイルに
       マッチさせればよい。年平均(00)・季節(13-16)ファイルは自動的に
       除外される。季節(DJF/MAM/JJA/SON)ごとに月をまとめて平均して出力する)
  VMAX カラーバーの上限値 [mol m-3]。省略時はデータの最大値から自動決定する
"""

import sys
sys.path.append('.')

import glob
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
vmax_arg = args.get('VMAX')

MONTH_TO_SEASON = {
    12: 'DJF', 1: 'DJF', 2: 'DJF',
    3: 'MAM', 4: 'MAM', 5: 'MAM',
    6: 'JJA', 7: 'JJA', 8: 'JJA',
    9: 'SON', 10: 'SON', 11: 'SON',
}

FNAME_RE = re.compile(r'_([a-z]{1,2})(\d{2})_\d{2}\.nc$')


def parse_fname(fname):
    m = FNAME_RE.search(fname)
    if not m:
        return None, None
    code, mm = m.groups()
    return code, int(mm)


def preprocess(ds):
    fname = ds.encoding['source']
    _, mm = parse_fname(fname)
    return ds.expand_dims(month=[mm]).assign_coords(
        season=('month', [MONTH_TO_SEASON[mm]]),
    )


files = sorted(
    f for f in glob.glob(file_in) if parse_fname(f)[1] in MONTH_TO_SEASON
)
if not files:
    logger.error(f'{file_in}: no monthly (01-12) files matched')
    sys.exit(1)

code = parse_fname(files[0])[0]
varname = f'{code}_an'

DS = xr.open_mfdataset(
    files, combine='nested', concat_dim='month', preprocess=preprocess,
    decode_times=False, join='override',
)
logger.debug(DS)

da = DS[varname].isel(time=0, depth=0)

m = re.search(r'moles_of_(\w+?)_per_unit_mass', da.attrs.get('standard_name', ''))
element = m.group(1).capitalize() if m else varname
da.attrs['long_name'] = element

units = da.attrs.get('units', '')

rho_sw_kgpm3 = 1025.  # kg m-3, 海水密度の概算値(表層)

if units == 'micromoles_per_kilogram':
    da = da * rho_sw_kgpm3 * 1.e-6
    units = 'mol m-3'
    da.attrs['long_name'] = element

da_season = da.groupby('season').mean('month', keep_attrs=True)

proj = ccrs.PlateCarree()

da_region = da_season.sel(lon=slice(117., 160.), lat=slice(20., 52.))
data_max = float(da_region.max())


def nice_vmax(value):
    if value <= 0:
        return 1.0
    magnitude = 10. ** np.floor(np.log10(value))
    for mult in (1., 2., 2.5, 5., 10.):
        candidate = mult * magnitude
        if candidate >= value:
            return candidate
    return 10. * magnitude


vmax = float(vmax_arg) if vmax_arg is not None else nice_vmax(data_max)
tick_step = vmax * 0.1

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
        cbar_kwargs={'ticks': np.arange(0, vmax + 1.e-4, tick_step), 'label': f'{element} [{units}]'}
    )

    ax.coastlines()
    ax.set_xticks( np.arange(120.,160.1,10.), crs=proj )
    ax.set_yticks( np.arange(20.,50.1,5.), crs=proj )
    ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
    ax.yaxis.set_major_formatter( LatitudeFormatter() )

    ax.set_title(f'{element} ({season}, WOA23)')

    ax.set_xlabel('')
    ax.set_ylabel('')

    fname = f'{element.lower()}_woa23_{season}.png'
    plt.savefig(fname, bbox_inches='tight')
    plt.close(fig)

    logger.info(f'OUTPUT: {fname}')
