#!/bin/bash

set -e

python vec_wind.py 1901-01-01
python contour_ssh.py ../../link/omipj-data/mricom_user/rectangle/nc_ssh.1901 1901-01-10
python contour_t_section.py ../../link/omipj-data/mricom_user/rectangle/nc_t.1901 1901-01-10

exit 0
