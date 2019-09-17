# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import (pd,np,xr,za,mpl,plt,sns, pjoin,
                              os,glob,dt,sys,ucp,log, splot)
import cartopy.crs as crs

# %%
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

# %%
path = '/proj/atm/saltena/runs/run_2019_05_15/wrf/'

# %%
files = glob.glob(path+'wrfout*d04*2017-12-31*')
files.sort()

# %%
TIME = 'Time'
PBLH = 'PBLH'
XTIME = 'XTIME'
LTIME = 'LOCAL TIME'

# %%
dso = ds = xr.open_mfdataset(files,concat_dim=TIME,combine='nested')
for ll in [co.XLAT,co.XLONG]:
    ds[ll] = ds[ll].mean(co.TIME)
ds[co.XLAT] = ds[co.XLAT].mean(co.WE).load()
ds[co.XLONG] = ds[co.XLONG].mean(co.SN).load()

# %%
ds[LTIME]=(ds[XTIME].to_pandas()-pd.Timedelta(hours=4)).to_xarray()

# %%
ds = ds.swap_dims({co.WE:co.XLONG,co.SN:co.XLAT,co.TIME:LTIME})

# %%
ax = fa.get_ax_lapaz()
ds[PBLH][{LTIME:-1}].plot(ax=ax,transform=crs.PlateCarree())
fa.add_chc_lpb(ax)
ax.set_xlim(co.CHC_LON-1,co.CHC_LON+1)
ax.set_ylim(co.CHC_LAT-1,co.CHC_LAT+1)

# %%
__ds = ds[PBLH]#[{co.TIME:-1}]

# %%
_,ax = splot(figsize=(10,5))
_ds = __ds.sel({co.XLAT:co.CHC_LAT},method='nearest')
_ds = _ds.plot.line(ax=ax,hue=LTIME,add_legend=False,alpha=.5)
ax.axvline(co.CHC_LON,color='k')

# %%
_,ax = splot(figsize=(10,5))
_ds = __ds.sel({co.XLAT:co.CHC_LAT},method='nearest')
_ds = _ds.plot(ax=ax,levels=10,cmap=plt.get_cmap('Reds'))
ax.axvline(co.CHC_LON,color='k')
ax.grid(True,linestyle='--',color='k')
ax.set_axisbelow(False)

# %%
_ds = __ds.sel({co.XLAT:co.CHC_LAT,co.XLONG:co.CHC_LON},method='nearest')

# %%
_ds.plot()

# %%
_ds.min().load()

# %%
ll=list(ds.variables)
ll.sort()

# %%
_ds = ds['TKE_PBL'].sel({co.XLAT:co.CHC_LAT,co.XLONG:co.CHC_LON},method='nearest')

# %%
_ds.plot(x=LTIME,cmap=plt.get_cmap('Reds'))

# %%
_ds = ds['W'].sel({co.XLAT:co.CHC_LAT,co.XLONG:co.CHC_LON},method='nearest')
_ds.plot(x=LTIME,cmap=plt.get_cmap('RdBu_r'))

# %%
file_objs = dso._file_obj.file_objs

# %%
fds = []
for f in file_objs:
    fds.append(f.ds)

# %%
z = wrf.getvar(fds,'wa')
z

# %%
_dds = wrf.vinterp(fds[0],z,'ght_msl',[0,1,2,3,4,5,6])

# %%
_dds.plot.pcolormesh(col='interp_level',col_wrap=2,size=6)

# %%
base_fun = xr.DataArray.plot.pcolormesh

# %%
_dds.plot.pcolormesh

# %%
base_pcolormesh = xr.plot.pcolormesh

# %%
_dds.sum('interp_level').plot.pcolormesh()

# %%
