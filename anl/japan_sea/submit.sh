#!/bin/bash

set -e

#year=$1
depth_m=$1

#for year in 2022 2024 ; do
for year in 2023 ; do
for mon in `seq -w 1 12` ; do
    python contour_t.py 2 ${year}-${mon} ${depth_m}
done
done

exit 0
