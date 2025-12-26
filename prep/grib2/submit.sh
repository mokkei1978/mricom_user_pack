#!/bin/bash

set -e

#for year in `seq 1971 2024` ; do
year=2024
for month in `seq -w 1 12` ; do
    sh conv_to_netcdf-jra3q-day.sh ${year}${month}
done

exit 0
