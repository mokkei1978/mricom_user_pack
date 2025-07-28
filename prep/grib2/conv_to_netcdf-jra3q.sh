#!/bin/bash
#- wgrib2 で grib2 ファイルを netCDF に変換する: JRA-3Q

set -e

year=$1
dir_base="../../link/data/jra3q"
diro=${dir_base}/netCDF2/${year}
mkdir -p ${diro}

for month in `seq -w 1 12` ; do
    YYYYMM=${year}${month}
    wgrib2 ${dir_base}/Monthly/fcst_phy2m125/fcst_phy2m125.${YYYYMM} -set_ftime "0 month fcst" -nc4 -netcdf ${diro}/nc_phy2m.${YYYYMM}
done

#- -set_date 19700102 for 1970/01

exit 0
