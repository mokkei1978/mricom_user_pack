#!/bin/bash
#- NOAAサイトから WOA 硝酸塩気候値データをダウンロードする

set -e

mkdir -p woa

for num in `seq -w 0 16` ; do
  wget2 -P "woa" "https://www.ncei.noaa.gov/thredds-ocean/fileServer/woa23/DATA/nitrate/netcdf/all/1.00/woa23_all_n${num}_01.nc"
done

exit 0
