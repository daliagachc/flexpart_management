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
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

import funs

mpl.rcParams['figure.dpi'] = 150

# class Dummy:
# def __init__(self):
# # pass

        # %%
path = \
'/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/' + \
'run_2019-09-25_15-25-01_/log_pol/run_2019-09-25_15-25-01_'
# flp = FLP.FlexLogPol(path,concat=True)
# selfFLP = FLP.FlexLogPol(path,concat=False)
selfFLP = FlexLogPol.FlexLogPol(
    path,
    #concat=True,
    concat=False,
    get_clusters=False,
    open_merged=True,
    clusters_avail=False
)

# %%
selfFLP.concat_ds()

# %%

# %%
_s1 = selfFLP.dask_ds_01[co.CONC].sum([co.RL,co.ZT])
_s1 = _s1.load()

# %%
_s2 = selfFLP.dask_ds_02[co.CONC].sum([co.RL,co.ZT])
_s2 = _s2.load()

# %%
__s2 = _s2.loc[{co.R_CENTER:slice(None,.8e0)}]

# %%
ops = dict(robust=True,yscale='log',ylim=(1e-1,1e2),vmin=1e5,vmax=2e6,
          norm=mpl.colors.LogNorm())

# %%
ax = axsplot()
_s1.plot.pcolormesh(ax=ax,**ops)
__s2.plot.pcolormesh(ax=ax,add_colorbar=False, **ops)

# %%
_s1.plot.pcolormesh(**ops)

# %%
_s2.plot.pcolormesh(**ops)

# %%
