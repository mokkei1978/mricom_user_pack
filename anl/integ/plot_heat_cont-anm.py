#!/usr/bin/env python
"""貯熱量の時系列を描く：偏差

Usage: plot_heat_cont.py

"""

import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('START')

subdir='heat_200m/japan_sea_all'
ds=xr.open_dataset('../../link/data/MOVEJPN/anl_mon-jpn/'+subdir+'/heat_cont.nc')
ds_clim=xr.open_dataset('../../link/data/JPN20-assim/anl_mon-jpn/'+subdir+'/heat_cont-clim.nc')
ds=ds.groupby('time.month') - ds_clim.groupby('time.month').mean(dim='time')

ds['hcj'] = ds.hc * 4.2e3 * 1024.  # [C cm3] => [J]
ds['tave'] = ds.hc / 1.79e14       #         => [C]

fig, ax = plt.subplots()
ds.tave.plot.line(color='red') #,marker='o')

#plt.legend()
ax.set_title( '200m heat content anm (Japan Sea All)' )
ax.set_xlabel('')
ax.set_ylabel('ave K')
#ax.set_xlim(pd.to_datetime('2022-01-01'),pd.to_datetime('2024-12-31'))
plt.grid()

ax2=ax.twinx()
ds.hcj.plot.line(color='red')
ax2.set_title('')
ax2.set_xlabel('')
ax2.set_ylabel('J')
#ax2.set_ylim(yrange/4.2e3/1024.)

#plt.show()
plt.savefig('temp.png', bbox_inches='tight')
logger.info('OUTPUT: temp.png')
