#!/bin/bash

set -e

#year=$1
#depth_m=$1

#for varname in total short long sensible latent ; do
for year in 2021 ; do
for mon in `seq -w 1 12` ; do
#    python contour_heatflux_anom.py ${varname} ${year}-${mon}
    python contour_tanm_section.py 2 ${year}-${mon}
done
done
#done

exit 0
