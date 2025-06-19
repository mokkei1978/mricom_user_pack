#!/bin/bash

set -e

python contour_sst.py 3 2025-01-01
python make_sst_ave.py 3 ; python plot_sst_ave.py 3

exit 0
