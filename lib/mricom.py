#!/usr/bin/env python
# coding:utf-8
"""MRI.COM のデータ読み込み。xarrayのdatasetとして返す。"""

import os
import re
import xarray as xr
from logging import getLogger
from xgrads import open_CtlDataset, CtlDescriptor

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

    ctl = CtlDescriptor( file=file )

    # 実験が ctl の TDEF より短いとき（interval_step <= 0 では TDEF が 1 年分になる）は、
    # データファイルにある分だけ読む
    nt = count_records( ctl )
    if nt < len(ctl.tdef.samples):
        logger.info('TDEF %d -> %d (records in data files): %s',
                    len(ctl.tdef.samples), nt, file)
        ctl = ctl_with_tdef( file, nt )

    d = open_CtlDataset( ctl )

    # UNDEF (陸格子など) を NaN にする。データは real(4) なので許容誤差を付けて比べる
    undef = d.attrs['undef']
    d = d.where( abs(d - undef) > abs(undef) * 1.e-6 )

    logger.debug(d)

    return d


def count_records( ctl ):
    """データファイルにある時間レコード数を返す"""
    if ctl.template:
        files = [ f for f in ctl.dsetPath if os.path.exists(f) ]
    else:
        files = [ ctl.dsetPath ]
    return sum( os.path.getsize(f) // ctl.tRecLength for f in files )


def ctl_with_tdef( file, nt ):
    """TDEF の個数を nt に書き換えた CtlDescriptor を返す"""
    dirname = os.path.dirname( os.path.abspath(file) )
    with open( file ) as f:
        content = f.read()

    # content で渡すと DSET の ^（ctl のディレクトリ）が展開されないので、先に展開する
    content = content.replace( '^', dirname + '/' )
    content = re.sub( r'^(\s*tdef\s+)\d+', r'\g<1>' + str(nt), content,
                      flags=re.IGNORECASE | re.MULTILINE )

    return CtlDescriptor( content=content )
