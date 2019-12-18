# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

from useful_scit.imps import *
import matplotlib.colors
import wrf
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

plt.rcParams['figure.facecolor'] = 'white'

# %% [markdown]
# # constants

# %%
V_MAX_MIN_DIC = dict(vmin=1e-8 , vmax=1e-4)

# %%
path = \
    '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/' + \
    'run_2019-10-02_13-42-52_/log_pol/run_2019-10-02_13-42-52_'
# flp = FLP.FlexLogPol(path,concat=True)
# selfFLP = FLP.FlexLogPol(path,concat=False)
selfFLP = FlexLogPol.FlexLogPol(
    path ,
    # concat=True,
    concat=False ,
    get_clusters=False ,
    #     open_merged=False,
    open_merged=True ,
    # merge_ds=False ,
    merge_ds=True ,
    clusters_avail=False ,
    postprocess=True ,
    use_new_merge_fun=True
    )

# %%
ds = selfFLP.merged_ds

# %%
hasl = 'hasl'

# %%

ds[ hasl ] = (ds[ co.TOPO ] / 250).round()*250 + ds[ co.ZM ]

# %%
ds_c = ds.reset_coords()[ co.CC ][ { co.RL : slice(None,None) } ]
ds_h = ds.reset_coords()[ hasl ]

# %%
ds_c_s:xr.DataArray = ds_c.sum([co.RL,co.TH_CENTER])
ds_c_s

# %%

# %%

coords_ = [ co.ZM , co.R_CENTER , co.TH_CENTER ]
ds_c1 = ds_c.transpose( co.RL,*coords_ , transpose_coords=True )
ds_h = ds_h.transpose( *coords_, transpose_coords=True )

# %%
zets = np.arange(250,15000,500)
res = wrf.interplevel(ds_c1,ds_h,zets)

# res.plot()
# plt.show()

# %%
res
res1:xr.DataArray = res.sum([co.TH_CENTER,co.RL])

# %%
# noinspection PyUnresolvedReferences
plt.rcParams['figure.facecolor'] = 'white'
ops = dict(
    norm=mpl.colors.LogNorm(**V_MAX_MIN_DIC),
    cmap=plt.get_cmap('Reds') ,
    xscale='log',
    xlim=(.1,30) ,
    ylim=(0,15000) ,
)
f,ax = plt.subplots( figsize=(10,6) )
res1.plot.pcolormesh(ax =ax , **ops)
ax.set_title('all conc density - height above sea level')
ax.set_xlabel('radial distance from chc [100 km]')
f,ax = plt.subplots( figsize=(10,6) )
ds_c_s.plot(y=co.ZM , x=co.R_CENTER,ax =ax , **ops)
ax.set_title('all conc density - height above ground');
ax.set_xlabel('radial distance from chc [100 km]')

# %%
