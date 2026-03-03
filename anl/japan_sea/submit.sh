#!/bin/bash
#PBS -l select=1:ncpus=1

set -e
cd ${PBS_O_WORKDIR}

. /home/sakamoto/venv/bin/activate

#python make_jra3q_ave.py
#exit 0

year=2023
#depth_m=$1

#for varname in total short long sensible latent ; do
#for year in 2021 ; do
for mon in `seq -w 8 12` ; do
#for day in `seq -w 1 30` ; do
#    python contour_heatflux_anom.py ${varname} ${year}-${mon}
#    python contour_heat_content-anm.py ${year}-${mon}
    python make_jra3q_hour2day.py ${year} ${mon}
    #python contour_t_vel.py 202306${day}
done
#done
#done

exit 0
