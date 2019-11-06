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

# %% [markdown] {"toc-hr-collapsed": false}
# ## imports

# %%
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
import funs
mpl.rcParams['figure.dpi'] = 150

# %%
log.ger.setLevel(log.log.DEBUG)

# %% [markdown]
# # Code

# %%
path = \
'/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/' + \
'run_2019-09-25_15-25-01_/log_pol/run_2019-09-25_15-25-01_'

# flp = FLP.FlexLogPol(path,concat=True)
# selfFLP = FLP.FlexLogPol(path,concat=False)
selfFLP = FlexLogPol.FlexLogPol(
    path,
#     concat=True,
    concat=False,
    get_clusters=False,
    open_merged=True,
    clusters_avail=False
)

# %%
selfFLP.reset_z_levels()

# %%
selfFLP.add_topo_to_merge_ds()

# %%
_sum_ds = selfFLP.merged_ds.sum([co.R_CENTER,co.TH_CENTER,co.ZM])

# %%
_sum_ds[co.CONC].plot()

# %%
merged_ds = selfFLP.merged_ds

# %%
dsF= selfFLP.filter_hours_with_few_mea()

# %%
co.FILTER = 'FILTER'
_ds1 = dsF.expand_dims(dim={co.FILTER:['filter_few']})

# %%
co.FILTER = 'FILTER'
_ds2 = merged_ds.expand_dims(dim={co.FILTER:['original']})

# %%
_ds3 = xr.merge([_ds1,_ds2])

# %%
_ds3

# %%
_dsSM = FlexLogPol.smooth_merged_ds(_ds3.sel(**{co.FILTER:'filter_few'}))

# %%
_dsSM1 = _dsSM.drop(co.FILTER).expand_dims(dim={co.FILTER:['filter_few_smooth']})

# %%
_ds4 = xr.concat([_ds3,_dsSM1],dim=co.FILTER)

# %%
_cp = selfFLP.coarsen_par

# %%
_da = _ds4[co.CONC].loc[{co.FILTER:'filter_few_smooth'}]

# %%
_da1 = _da.coarsen(**{co.RL:_cp}).mean()

# %%
co.RLC = 'releases_coarsen'
co.CONC_COARS = 'CONC_COARSEN'
_da2 = _da1.rename({co.RL:co.RLC}).drop(co.FILTER).expand_dims(dim={co.FILTER:['filter_few_smooth_coarse']})
_da2.name = co.CONC_COARS

# %%
_da3 = _da2.dropna(co.RLC,how='all').dropna(co.ZM,how='all').dropna(co.R_CENTER,how='all').dropna(co.TH_CENTER,how='all')

# %%
_dst = _ds4[{co.R_CENTER:slice(None,3),co.TH_CENTER:slice(None,4),co.ZM:slice(None,5),co.RL:slice(None,10)}]

# %%
_dat = _da3[{co.R_CENTER:slice(None,3),co.TH_CENTER:slice(None,4),co.ZM:slice(None,5),co.RLC:slice(None,9)}]

# %%
# xr.merge([_dst,_dat]).sel(**{co.FILTER:'filter_few_smooth_coarse'})
_dsm=xr.merge([_ds4,_da3])

# %%
fig,ax = plt.subplots(figsize=(20,5))

_dsm[co.CONC_COARS].sel(**{co.FILTER:'filter_few_smooth_coarse'})[:,2,10,8].plot(ax=ax,label=co.CONC_COARS,alpha=.5)

_dsm[co.CONC].sel(**{co.FILTER:'original'})[:,2,10,8].plot(ax=ax,label=co.CONC,alpha=.5)
_dsm[co.CONC].sel(**{co.FILTER:'filter_few'})[:,2,10,8].plot(ax=ax,label=co.CONC,alpha=.5)

# %%
_dsm[co.CONC].sel(**{co.FILTER:'filter_few'}).sum([co.ZM,co.R_CENTER,co.TH_CENTER]).plot()

# %%
ax.legend()

# %%
ax.figure

# %%
