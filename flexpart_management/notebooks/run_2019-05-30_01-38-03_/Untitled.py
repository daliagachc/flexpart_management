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
rel = slice(0,None)
tim = slice(0,None)
dic = {fa.RL:rel,fa.TIME:tim}
zc = 'ZMID*CONC'
dsn = ds2[[fa.CONC]][dic]
dsn[zc]=dsn[fa.CONC]*dsn[fa.ZM]

# %%
val=np.array([.09,np.pi/36])*2

# %%
dsn[zc]=dsn[zc].where(dsn[zc]>0)

# %%
dim2keep = [fa.TIME,fa.RL]

# %%
dsum = dsn.sum(dim=fa.ZM)
dsum = dsum.where(dsum[fa.CONC]>0)

# %%
_a1 = fa.data_array_to_logpolar(dsum[zc],*val,dim2keep=dim2keep)
_a2 = fa.data_array_to_logpolar(dsum[fa.CONC],*val,dim2keep=dim2keep)


# %%
z=(_a1/_a2)
zn='z'
z.name = zn

# %%
z99 = z.quantile(.99).values
c99 = _a2.quantile(.99).values

# %%
c99

# %%

ax = fa.get_ax_bolivia()
fa.logpolar_plot(z,ax=ax,name=zn,patch_args={'cmap':'viridis'})
ax = fa.get_ax_bolivia()
fa.logpolar_plot(_a2,ax=ax,perM=.99)

# %%

# %%
