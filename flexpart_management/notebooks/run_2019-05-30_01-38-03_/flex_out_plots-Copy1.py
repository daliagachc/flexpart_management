# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

# %%
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as cons

# %%
ds1 = xr.open_dataset('/tmp/dd4.nc')
ds2 = xr.open_dataset('/tmp/dd02.nc')

# %%
dc =ds1[fa.CONC][{fa.RL:20}].sum(dim=[fa.ZM,fa.TIME])

# %%
val=np.array([.09,np.pi/36])*2

# %%
nds= fa.data_array_to_logpolar(dc,*val)

# %%
nds

# %%
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection

# %%
conc = nds/nds[fa.GA]
conc.name = 'conc'

# %%

# %%
ax = fa.get_ax_bolivia()
# fig, ax = plt.subplots()
ax = fa.logpolar_plot(conc.where(conc>0),ax,name='conc',perM=.8,perm=.1,
                 colorbar=True,
                 patch_args={'norm':matplotlib.colors.LogNorm(),'cmap':'viridis'}
                )

# %%
ax = fa.get_ax_bolivia()
# fig, ax = plt.subplots()
ax = fa.logpolar_plot(conc.where(conc>0),ax,name='conc',perM=.8,perm=.1,
                 colorbar=True,
#                  patch_args={'norm':matplotlib.colors.LogNorm()}
                )

# %%
ax = fa.get_ax_bolivia()
# fig, ax = plt.subplots()
ax = fa.logpolar_plot(nds,ax,perM=.99,perm=.1,
                 colorbar=True
                )

# %%
ax = fa.get_ax_lapaz()
# fig, ax = plt.subplots()
ax = fa.logpolar_plot(nds,ax,perM=.95,perm=.1,
                 colorbar=True
                )

# %%

res.plot()

# %%
ax =fa.get_ax_bolivia()
nds.plot(x=fa.LON,y=fa.LAT,ax=ax,transform=fa.PROJ)

# %%
r.max()

# %%
r1=.05
r2=30
n=40
rlog_space = np.linspace(np.log(r1),np.log(r2),n)
r_space = np.e**rlog_space

# %%
plt.figure()
plt.plot(rlog_space)
plt.figure()
plt.plot(r_space)

# %%
RS = 'r_space'
RD = 'r_dis'
RC = 'r_center'
df_r = pd.DataFrame(r_space,columns=[RS])
df_r[RD] = df_r[RS] - df_r[RS].shift()
df_r = df_r
df_r[RC] = (df_r[RS] + df_r[RS].shift())/2
# df_r = df_r.dropna()

# %%
df_r[RS]/df_r[RD]

# %%
ax = fa.get_ax_bolivia()
for r in df_r[RS]:
#     print(r)
    circle = plt.Circle((fa.CHC_LON,fa.CHC_LAT), r, color='k', fill=False, transform=fa.PROJ)
    ax.add_artist(circle)
ax = fa.get_ax_lapaz()
for r in df_r[RS]:
#     print(r)
    circle = plt.Circle((fa.CHC_LON,fa.CHC_LAT), r, color='k', fill=False, transform=fa.PROJ)
    ax.add_artist(circle)

# %%
import area

# %%
obj = {'type':'Polygon','coordinates':[[[0,0],[1,0],[1,1],[0,1]]]}

# %%
area.area(obj)

# %%
res  = nds.copy()

# %%
res.reset_coords()

# %%
dc = ds[fa.CONC][:,0].sum(dim=[fa.TIME])
dc=dc/ds[fa.GA]


# %%
dc.interp(**{fa.LAT:fa.CHC_LAT-1,fa.LON:fa.CHC_LON-1})

# %%
dc[10].plot()

# %%
ds=ds1
ang = -(np.mod(np.arctan2(ds[fa.LAT]-fa.CHC_LAT,ds[fa.LON]-fa.CHC_LON)+np.pi/2,2*np.pi)-np.pi)*180/np.pi
ang = np.floor(ang/10)*10+5
ds['ang']=ang

# %%
res = ang.to_series().unique()
res.sort()
res

# %%
ang.plot(x=fa.LON)

# %%
_r = 2
r_log = np.round(np.log(ds[fa.LL_DIS])/_r,1)*_r
ds['r_log']=r_log

# %%
ax = fa.get_ax_bolivia()
ds['r_log'].plot(ax=ax)

# %%

# %%
dsd = ds[[fa.CONC,'r_log','ang']][{fa.RL:1}].sum(dim=[fa.ZM,fa.TIME])

# %%
df = dsd.to_dataframe()

# %%
rlds = df.groupby(['r_log','ang'])['CONC'].count().to_xarray()

# %%
rlds.plot(vmin=1,vmax=10)

# %%
dsum = df.groupby(['r_log','ang'])['CONC'].sum().to_xarray()

# %%
dsum[:,-3:].plot()

# %%
dsum.ang

# %%
ll_dis = np.e**dsum['r_log']
lat = ll_dis*np.cos(dsum['ang']*np.pi/180)+fa.CHC_LAT
lon = ll_dis*np.sin(dsum['ang']*np.pi/180)+fa.CHC_LON
dsum = dsum.assign_coords(**{fa.LAT:lat,fa.LON:lon})

# %%
ax =fa.get_ax_bolivia()
plt.scatter(lon,lat)

# %%
dsum[:,-1].plot()

# %%
from matplotlib import ticker, cm
ax = fa.get_ax_bolivia()
dsum1 =(dsum/(np.e**dsum['r_log'])**2)
dsum1.plot(x=fa.LON,y=fa.LAT,cmap=fa.red_cmap(),ax=ax,transform=fa.PROJ,vmin=10,vmax=1000,
           norm=matplotlib.colors.LogNorm()
          )
ax = fa.get_ax_lapaz()
dsum1.plot(x=fa.LON,y=fa.LAT,cmap=fa.red_cmap(),ax=ax,transform=fa.PROJ,vmin=10,vmax=1000,norm=matplotlib.colors.LogNorm())

# %%
dsum[:,0]

# %%
lam = 'la_max'
laM = '_min'
lom = 'a_min'
loM = 'a_max'

bounds = [rM,rm,aM,aM]

# %%
dsum

# %%
