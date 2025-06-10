#!/usr/bin/env python
# coding:utf-8
""" MRI.COM 等のデータ読み込みのラッパー"""

from lib import mricom

def open_dataset( file, kind, **kwargs ):
    """
    データファイルを読み込み、xarrayのdatasetとして返す

    Parameters
    --------
    file : char, list of char or char with regular expression
        入力ファイル。kind によってはリストや正規表現による複数ファイルの指定が可能
    kind : char
        入力ファイルのデータ種別

    Returns
    --------
    return: xarray.Dataset
        kind 毎に用意された読み込みルーチンで作成された Dataset 。
    """

    methods = { 'mricom-history': mricom.open_history ,
                'grads': mricom.open_grads ,
    }
    method_to_read = methods[kind]

    return method_to_read( file, **kwargs )
