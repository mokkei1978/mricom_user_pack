#!/bin/bash

set -e

for year in `seq 1971 2024` ; do
    sh conv_to_netcdf-jra3q.sh ${year}
done

exit 0
