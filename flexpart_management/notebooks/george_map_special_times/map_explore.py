# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.7.0-rc1
#   kernelspec:
#     display_name: Python [conda env:b36]
#     language: python
#     name: conda-env-b36-py
# ---

# %%
from useful_scit.imps2.defs import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

# %%
pat = Path(co.tmp_data_path) / 'new_log_pol_ds_asl_v01.nc'

# %%
ds = xr.open_dataset(pat)

# %%
ds

# %%
ds['CONC'][{co.RL:10}].sum(co.ZM).plot(y=co.R_CENTER,x=co.TH_CENTER)

# %%
da = ds.loc[{co.RL:'2018-01-10 15'}]

# %%
ax = fa.get_ax_bolivia()
fa.logpolar_plot(da.sum(co.ZM),ax=ax)

# %%
da

# %%
da

# %%
da = ds.loc[{co.RL:slice('2018-01-10 21','2018-01-11 06')}]
da['dis'] = da[co.R_CENTER] * 100
da = da.assign_coords(dis=da['dis'])
da['CONC'].sum(co.TH_CENTER).\
plot(
    x='dis',figsize=(20,5),
#     norm = mpl.colors.SymLogNorm(linthresh=10),
#     xscale = 'log'
    cmap='Reds',
    col=co.RL,
    col_wrap = 4
    
    )

# %%
f,axs = plt.subplots(4,3,subplot_kw={'projection':crt.crs.PlateCarree()})

da = ds.loc[{co.RL:slice('2018-01-10 21','2018-01-11 06')}]

for ax,i in zip(axs.flatten(),da[co.RL]):
    fa.get_ax_bolivia(ax=ax)
    fa.logpolar_plot(da.loc[{co.RL:i}].sum(co.ZM),ax=ax,colorbar=False,)
    ax.legend().remove()

# %%
ds['TOPOGRAPHY'].plot()

# %%
res = plt.plot([.6,1],[0,1],clip_on=False)
ax = plt.gca()
ax.set_xlim(0,.5)
l = res[0]
# l.set_clip_on(False)

# %%

# %%
res

# %%
