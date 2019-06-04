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

# %%
ds = xr.open_dataset('/tmp/dd4.nc')
ds2 = xr.open_dataset('/tmp/dd02.nc')

# %%
i = 0 
for i in range(len(ds[fa.RL])):
    di = ds[{fa.RL:i}]
    dii = di[fa.CONC].sum(dim=[fa.TIME,fa.ZM])
    ax = fa.get_ax_bolivia()
    diii = dii * di[fa.LL_DIS]
    diii.plot(ax=ax,cmap=fa.red_cmap(),vmax=800)
    fa.add_chc_lpb(ax)

# %%
for i in range(len(ds[fa.RL])):
# for i in range(1):
    di = ds2[{fa.RL:i}]
    dii = di[fa.CONC].sum(dim=[fa.TIME,fa.ZM])
    ax = fa.get_ax_lapaz()
    diii = dii * di[fa.LL_DIS]
    diii.plot(ax=ax,cmap=fa.red_cmap(),vmax=5)
    fa.add_chc_lpb(ax)

# %%
