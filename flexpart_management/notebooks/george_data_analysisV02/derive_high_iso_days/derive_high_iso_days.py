# ---
# jupyter:
#   jupytext:
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
from flexpart_management.notebooks.george_data_analysisV02.derive_high_iso_days.derive_high_iso_days_lfc import *

# %%
df_ts = fa.open_iso_ts()
# %%
crh, c45, cbc = 'RH_station', 'C4_C5_compounds', 'BC'
col_int = [crh, c45, cbc]
# %%
_da: xr.DataArray = df_ts[col_int].to_xarray().to_array()
_da.plot(row='variable', sharey=False, figsize=(20, 10))
plt.show()
# %%

_da: xr.DataArray = df_ts[col_int].to_xarray().to_array()
_boo = _da[co.RL].dt.month == 1
_da.where(_boo).plot(row='variable', sharey=False, figsize=(20, 10))
plt.show()
# %%
import xarray.plot
_da: xr.DataArray = df_ts[col_int].to_xarray().to_array()
_boo = _da[co.RL].dt.month == 1
fg:xr.plot.FacetGrid = xr.plot.FacetGrid(
    _da,
    row='variable', sharey=False, figsize=(20, 10)
)


# %%
fg:xr.plot.FacetGrid = xr.plot.FacetGrid(
    _da,
    row='variable', sharey=False, figsize=(20, 10)
)
def _f(*a,**k):
    pass
    # pprint.pprint(a)
    # pprint.pprint(k)
fg.map_dataarray(_f,x=co.RL,y='variable')

plt.show()
# %%
# TODO: this is far from bing completed.
# %%
# %%
# %%
# %%
