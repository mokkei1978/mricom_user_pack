#!/bin/bash
#- wgrib2 library を用いた場合のコンパイル・オプションを調べる
#- CMake でビルドするように指示があるが、CMakeを使わない場合のコンパイル方法を知るため
#-  https://github.com/NOAA-EMC/wgrib2

set -e

#sh download_netcdf_cmake.sh

mkdir -p build
cd build
cmake ..
make clean
make VERBOSE=1

exit 0
