#!/usr/bin/env python
"""水位・流速の水平分布を描く

Usage: eta_vel.py FILE YMD K EXPNAME

Arguments:
  FILE     path of input file
  YMD      date for plot(YYYY-MM-DD)
  K        layer number for plot [0:km-1]
  EXPNAME  name of experiment
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from docopt import docopt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

args = docopt(__doc__)
file_in = args.get('FILE')
date = args.get('YMD')
ckl = args.get('K')
exp_name = args.get('EXPNAME')

#- ファイル読み込み
DS = xr.open_mfdataset(file_in+'/nc_dept.'+date[:4])
klayer = int( ckl )
da = DS["dep"].sel(time=date).isel(depth=klayer).squeeze()

DSu = xr.open_mfdataset(file_in+'/nc_u.'+date[:4])
DSv = xr.open_mfdataset(file_in+'/nc_v.'+date[:4])
u_mps = DSu['uo'].sel(time=date).isel(depth=klayer).squeeze() * 1.e-2
v_mps = DSv['vo'].sel(time=date).isel(depth=klayer).squeeze() * 1.e-2

ctitle = da.standard_name
cunit = da.units
#cunit = "m"
#da = ( da - da.mean().values ) #* 1.e-2
da = da * 1.e-2

if klayer == 1:
    clevs = np.arange(-20., 20.1, 1.)*10 + 400.
    llevs = np.arange(-5., 5.1, 1.)*40 + 400.
    minvel_mps = 0.001
    maxvel_mps = 0.02
else:
    da = - da  #- 海面の高さ
    clevs = np.arange(-20., 20.1, 1.)*0.05
    llevs = np.arange(-5., 5.1, 1.)*0.1
    minvel_mps = 0.02
    maxvel_mps = 0.2

#- 流速 (ベクトルの長さは同じにして、色で流速を示す)
dec = 2  # decimate (間引く間隔)
im=u_mps.shape[1]
jm=u_mps.shape[0]
ilist=list(range(0,im-1,dec))
jlist=list(range(0,jm-1,dec))
u2_mps = u_mps[jlist,ilist]
v2_mps = v_mps[jlist,ilist]
speed2_mps = np.sqrt( u2_mps**2 + v2_mps**2 )
mask = speed2_mps <= minvel_mps
speed2_mps = np.ma.masked_where(mask, speed2_mps)
lon_deg = u2_mps.lon.values
lat_deg = u2_mps.lat.values
u = np.ma.masked_where(mask, u2_mps / np.where(mask, 1, speed2_mps))
v = np.ma.masked_where(mask, v2_mps / np.where(mask, 1, speed2_mps))


#- キャンバス
fig = plt.figure()
#ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0) )
proj = ccrs.PlateCarree()
ax = plt.subplot(1,1,1,projection=ccrs.Mollweide(central_longitude=30) )
ax.set_facecolor('lightgray')
#ax.set_xticks( np.arange(0.,60.1,20.), crs=proj )
#ax.set_yticks( np.arange(10.,60.1,10.), crs=proj )

da.plot.contourf( transform=proj, cmap=cm.bwr, levels=clevs, add_colorbar=False )
cntr = da.plot.contour(transform=proj, levels=llevs, colors='black', linewidths=0.5)
ax.clabel(cntr)

Q = ax.quiver(lon_deg,lat_deg,u,v,speed2_mps,cmap=cm.jet,pivot='mid',transform=proj,
              norm=plt.Normalize(vmin=0.0, vmax=maxvel_mps),
              scale=20, headwidth=6, headlength=8, headaxislength=7)
plt.colorbar(Q, label='Velocity [m/s]', shrink=0.6, ax=ax)
#ax.clabel(cs)

gl = ax.gridlines(draw_labels=True,x_inline=False,linewidth=0.5, color='gray')
gl.top_labels = False
gl.right_labels = False

ax.set_extent((0., 60., 10., 60.), crs=proj )
#ax.set_title(exp_name+' '+ctitle+'['+cunit+'] k='+str(klayer+1)+' '+date)
ax.set_title('')
plt.savefig('temp.png', bbox_inches='tight')
plt.savefig('eta'+ckl+'_'+date+'.png', bbox_inches='tight')

