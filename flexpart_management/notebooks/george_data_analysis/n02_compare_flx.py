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
import flexpart_management.notebooks.george_data_analysis.n02_compare_flx_lfc as lfc
#local functions and constants

from flexpart_management.modules import fa
from flexpart_management.modules import co
from useful_scit.imps import *
fa,co,plt;

# %%
from flexpart_management.notebooks.george_data_analysis.n02_compare_flx_lfc import \
    plot_for_time_stamp


# def main():
# %%
data = lfc.import_george_data()
time_stamps = data['candidate_ft_timestamps']
# %%
flx_ds = fa.open_temp_ds('ds_clustered_18.nc')
# %%
flx_ds = lfc.add_is_it_ft_candidate(flx_ds, time_stamps)
# %%
lfc.plot_z_above_sea_level_comparison(flx_ds)

# %%
lfc.plot_above_ground_level(flx_ds)
# %%
def boo(r):
    r0 = xr.DataArray(r.iloc[0])
    r1 = xr.DataArray(r.iloc[1])
    rl_ = flx_ds[co.RL]
    res = np.logical_and(rl_>=r0,rl_<=r1)
    return res

time_stamps['boo']=time_stamps.apply(boo,axis=1)
# %%
clocks = {
    0:[[[10,4],[4,10]]],
    1:[[[6,10],[10,6]]],
    2:[[[0,7],[7,12]]],
    3:[[[9,4],[4,9]]],
    4:[[[0,12]]],
    5:[[[6,12],[0,6]]],
    6: [[[11, 5], [5, 11]]],
    7: [[[11, 5], [5, 11]]],
    8: [[[10, 3], [3, 10]]],
    9: [[[9, 3], [3, 9]]],
}
_df = pd.DataFrame(clocks).T
time_stamps['hs']=_df
# %%


for l,r in time_stamps.iloc[:].iterrows():
    if np.isnan(r['hs']).all():
        hs = None
    else:
        hs = r['hs']
    lfc.plot_for_time_stamp(flx_ds, r, l,hs=hs)
# %%


# %%

# %%


# %%
