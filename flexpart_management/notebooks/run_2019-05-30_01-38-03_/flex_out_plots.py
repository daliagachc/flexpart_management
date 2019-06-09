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
import flexpart_management.modules.constants
import flexpart_management.modules.flx_array as fa
from useful_scit.imps import *

# %%
ds = xr.open_dataset('/tmp/dd4.nc')
ds2 = xr.open_dataset('/tmp/dd02.nc')

# %%
i = 0 
for i in range(len(ds[flexpart_management.modules.constants.RL])):
    di = ds[{flexpart_management.modules.constants.RL:i}]
    dii = di[flexpart_management.modules.constants.CONC].sum(dim=[flexpart_management.modules.constants.TIME,
                                                                  flexpart_management.modules.constants.ZM])
    ax = fa.get_ax_bolivia()
    diii = dii * di[flexpart_management.modules.constants.LL_DIS]
    diii.plot(ax=ax,cmap=fa.red_cmap(),vmax=800)
    fa.add_chc_lpb(ax)

# %%
for i in range(len(ds[flexpart_management.modules.constants.RL])):
# for i in range(1):
    di = ds2[{flexpart_management.modules.constants.RL:i}]
    dii = di[flexpart_management.modules.constants.CONC].sum(dim=[flexpart_management.modules.constants.TIME,
                                                                  flexpart_management.modules.constants.ZM])
    ax = fa.get_ax_lapaz()
    diii = dii * di[flexpart_management.modules.constants.LL_DIS]
    diii.plot(ax=ax,cmap=fa.red_cmap(),vmax=5)
    fa.add_chc_lpb(ax)

# %%
