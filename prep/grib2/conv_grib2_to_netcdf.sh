#!/bin/bash
#- wgrib2 で grib2 ファイルを netCDF に変換する
#-   時間がかかる。大規模な変換には MXE/anl/format_conv/ を用いる。

set -e

year=2025
diro=../../link/data/netCDF/JPN/${year}
mkdir -p ${diro}

wgrib2 ../../link/data/JPN/2025/ssh.20250322.grib2 -netcdf ${diro}/nc_ssh.20250322

exit 0
