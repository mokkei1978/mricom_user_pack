#!/bin/bash
#- wgrib2 で grib2 ファイルを netCDF に変換する: JRA-3Q

set -e

YYYYMM=$1

cd ../../link/data/jra3q/org/Daily/fcst_phy2m125/${YYYYMM}/
diro="../../../../hour/${YYYYMM}"
mkdir -p ${diro}

files=$( ls fcst_phy2m125.* )

for file in ${files} ; do
    suffix=${file#*.}
    wgrib2 ${file} -nc4 -netcdf ${diro}/nc_phy2m.${suffix}
done

exit 0
