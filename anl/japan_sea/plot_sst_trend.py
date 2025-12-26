#!/usr/bin/env python
'''ある格子、ある月のSST線形トレンドを描画する
'''

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from lib import xarray_maker

DS = xarray_maker.open_dataset('../../link/data/MGDSST/month/30yrs/*/nc_sst.*','mricom-history')
#DS = xarray_maker.open_dataset('../../link/data/MGDSST/month/202*/nc_sst.*','mricom-history')
da = DS.thetao.sel(lat=35.,lon=130,method='nearest')
da01=da.groupby('time.month')[1]
#year=np.arange(1991,2021)
year=np.arange(-14.5,15.5,1.0)
da01['time']=year
coefs=da01.polyfit(dim='time',deg=1).polyfit_coefficients.values

fig, ax = plt.subplots()
da01.plot.line()
ax.plot(year,coefs[0]*year+coefs[1])
plt.savefig('temp.png', bbox_inches='tight')

