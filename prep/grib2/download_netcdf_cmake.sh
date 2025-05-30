#!/bin/bash
#- netCDFありでwgrib2 をインストールした場合、cmakeファイルを用意する

set -e

mkdir -p cmake

wget2 -P cmake https://raw.githubusercontent.com/NOAA-EMC/wgrib2/52938a1145cc2b3ceb6bf3b80a9dc106d786820c/cmake/FindNetCDF.cmake

exit 0
