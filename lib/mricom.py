#!/usr/bin/env python
# coding:utf-8
"""MRI.COM のデータ読み込み。xarrayのdatasetとして返す。"""

import xarray as xr
from logging import getLogger
from xgrads import open_CtlDataset

def open_history( file, **kwargs ):
    """MRI.COM history (netCDF) データ読み込み"""
    logger = getLogger(__name__)

    d = xr.open_mfdataset( file )

    logger.debug(d)

    if ( 'depth' in d.dims ):
        d = d.rename({'depth':'lev'})

    return d

def open_grads( file, **kwargs ):
    """grads形式データ読み込み (fileはgrads ctlを指定する)。UNDEF は NaN にする"""
    logger = getLogger(__name__)

    d = open_CtlDataset( file )

    # UNDEF (陸格子など) を NaN にする。データは real(4) なので許容誤差を付けて比べる
    undef = d.attrs['undef']
    d = d.where( abs(d - undef) > abs(undef) * 1.e-6 )

    logger.debug(d)

    return d
