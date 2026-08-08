#!/usr/bin/env python
"""白地図を描く"""

import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

fig = plt.figure()
ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=180) )
ax.patch.set_facecolor('white')
proj = ccrs.PlateCarree()
ax.set_extent((130., 142., 29., 37.), crs=proj )

ax.coastlines()
ax.add_feature(cfeature.LAND, facecolor='gray')
ax.set_xticks( np.arange(130.,140.1,5.), crs=proj )
ax.set_yticks( np.arange(30.,36.1,2.), crs=proj )
ax.xaxis.set_major_formatter( LongitudeFormatter(zero_direction_label=True) )
ax.yaxis.set_major_formatter( LatitudeFormatter() )

#plt.show()
plt.savefig('temp.png', bbox_inches='tight', dpi=200 )

logger.info('OUTPUT: temp.png')
