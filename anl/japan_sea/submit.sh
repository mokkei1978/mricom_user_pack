#!/bin/bash

set -e

year=$1
#depth_m=$1

#for varname in total short long sensible latent ; do
#for year in 2021 ; do
for mon in `seq -w 1 12` ; do
#for day in `seq -w 1 30` ; do
#    python contour_heatflux_anom.py ${varname} ${year}-${mon}
    python contour_heat_content-anm.py ${year}-${mon}
    #python contour_t_vel.py 202306${day}
done
#done
#done

exit 0
