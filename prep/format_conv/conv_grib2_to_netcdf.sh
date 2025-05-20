#!/bin/bash
# grib2 ファイルを netCDF に変換する

set -e

year=2025
diro=../../link/data/netCDF/JPN/${year}
mkdir -p ${diro}

wgrib2 ../../link/data/JPN/2025/ssh.20250322.grib2 -netcdf ${diro}/nc_ssh.20250322

exit 0
