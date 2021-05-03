# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: b37
#     language: python
#     name: b37
# ---

# %% tags=[]
from useful_scit.imps2.defs import *

# %% tags=[]
p = './data/cluster_series_v3.nc'

# %% tags=[]
po = './data/csv'

# %%
os.makedirs(po,exist_ok=True)

# %% tags=[]
ds = xr.open_dataset(p)

# %% tags=[]
va = list(ds.data_vars)

# %% tags=[]
for v in va:
    res = ds[v].to_dataframe()
    oo = pjoin(po,f'{v}.csv')
    res.to_csv(oo)

# %%
