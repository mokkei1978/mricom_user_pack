#!/usr/bin/env python
# coding:utf-8
"""MRI.COM のデータ読み込み。xarrayのdatasetとして返す。"""

import xarray as xr
from logging import getLogger

def open_history( file, **kwargs ):
    """MRI.COM history (netCDF) データ読み込み"""
    logger = getLogger(__name__)

    d = xr.open_mfdataset( file )

    logger.debug(d)

    return d
