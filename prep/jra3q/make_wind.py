#!/usr/bin/env python
# coding:utf-8
"""JRA-3Q 気候値データ (clim.nc) から風応力成分 (UFLX_surface, VFLX_surface) を
grads形式(big_endianバイナリ + ctl)で書き出す

UFLX_surface, VFLX_surface は大気側から見た運動量フラックスなので、
海洋に作用する風応力として使うために符号を反転させる。

Usage: make_wind.py [--in=FILE] [--out=BASE]

Options:
  --in=FILE   入力netCDFファイル [default: ../../link/data/jra3q/month/clim.nc]
  --out=BASE  出力ファイルのベース名。BASEx.gd/.ctl(uflx), BASEy.gd/.ctl(vflx),
              BASE_grid.d を作成する [default: wind]
"""

import sys
sys.path.append('.')

import numpy as np
import xarray as xr
from docopt import docopt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UNDEF = -0.9990000e+34

MONTH = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
         'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


def grads_date(t):
    """numpy.datetime64 -> grads の日付表記(例: 00Z01JAN2020)に変換する"""
    ts = t.astype('datetime64[s]').item()
    return f'{ts.hour:02d}Z{ts.day:02d}{MONTH[ts.month - 1]}{ts.year:04d}'


def write_grid(file_grid, lon, lat):
    """経度・緯度をまとめて1レコードの Fortran unformatted sequential (big_endian) で書き出す"""
    lon_be = lon.astype('>f8')
    lat_be = lat.astype('>f8')
    nbyte = (lon_be.size + lat_be.size) * 8

    with open(file_grid, 'wb') as f:
        np.array([nbyte], dtype='>i4').tofile(f)
        lon_be.tofile(f)
        lat_be.tofile(f)
        np.array([nbyte], dtype='>i4').tofile(f)


def write_ctl(file_ctl, file_gd, lon, lat, time, name, long_name):
    """grads ctl ファイルを書き出す(1変数)"""
    nx, ny, nt = lon.size, lat.size, time.size
    dlon = float(lon[1] - lon[0])
    dlat = float(lat[1] - lat[0])

    with open(file_ctl, 'w') as f:
        f.write(f'DSET ^{file_gd}\n')
        f.write('OPTIONS big_endian\n')
        f.write('TITLE JRA-3Q climatological wind stress\n')
        f.write(f'UNDEF {UNDEF:.7E}\n')
        f.write(f'XDEF {nx:5d} LINEAR {lon[0]:.6f} {dlon:.6f}\n')
        f.write(f'YDEF {ny:5d} LINEAR {lat[0]:.6f} {dlat:.6f}\n')
        f.write('ZDEF     1 LINEAR 1 1\n')
        f.write(f'TDEF {nt:5d} LINEAR {grads_date(time[0])} 1MO\n')
        f.write('VARS 1\n')
        f.write(f'  {name} 0 99 {long_name}\n')
        f.write('ENDVARS\n')


def main():
    args = docopt(__doc__)
    file_in = args['--in']
    base_out = args['--out']
    file_grid = f'{base_out}_grid.d'

    logger.info('READ: %s', file_in)
    ds = xr.open_dataset(file_in)

    lon = ds['longitude'].values
    lat = ds['latitude'].values
    time = ds['time'].values

    varinfo = [
        (f'{base_out}x.gd', f'{base_out}x.ctl', 'uflx', ds['UFLX_surface'],
         ds['UFLX_surface'].attrs.get('long_name', 'UFLX_surface')),
        (f'{base_out}y.gd', f'{base_out}y.ctl', 'vflx', ds['VFLX_surface'],
         ds['VFLX_surface'].attrs.get('long_name', 'VFLX_surface')),
    ]

    for file_gd, file_ctl, name, da, long_name in varinfo:
        logger.info('WRITE: %s', file_gd)
        with open(file_gd, 'wb') as f:
            for it in range(time.size):
                dat = da.isel(time=it).values.astype(np.float32)
                #- 大気側の運動量フラックス -> 海洋に作用する風応力へ符号反転
                dat = -dat
                dat = np.where(np.isnan(dat), np.float32(UNDEF), dat)
                dat.astype('>f4').tofile(f)

        logger.info('WRITE: %s', file_ctl)
        write_ctl(file_ctl, file_gd, lon, lat, time, name, long_name)

    logger.info('WRITE: %s', file_grid)
    write_grid(file_grid, lon, lat)

    logger.info('DONE')


if __name__ == '__main__':
    main()
