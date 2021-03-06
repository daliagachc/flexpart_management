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
import \
    flexpart_management.notebooks.george_data_analysisV02.n_01_ft_candidate_lfc as lfc
# local functions and constants
from useful_scit.imps import *
from flexpart_management.modules import constants as co, flx_array as fa

# noinspection PyStatementEffect
fa, lfc, plt, co;

# %%
# def main():
# %%

# %%
df = pd.read_excel(
    '/Volumes/mbProD/flexpart_management_data/flexpart_management/tmp_data/data_george_ccV02.xlsx')
# %%
# CONSTANTS
t0, t1, name, h11, h12, h21, h22, tlen = \
    't0_utc', 't1_utc', 'name', 'h11', 'h12', 'h21', 'h22', 'length[h]'
# %%
ds = fa.open_temp_ds('ds_clustered_18.nc')
da = ds[co.CONC]
# %%
r = df.iloc[0]
# %%
log.ger.setLevel(log.log.INFO)

dzr = da.sum([co.RL, co.TH_CENTER]).load()
# %%
dv = (da / da['r_length'])
# dvzr = dv.sum([co.RL,co.TH_CENTER]).load()

dvzr = dv.sum([co.RL, co.TH_CENTER]).load()
# %%
dvzr = dvzr.assign_coords(km=dvzr[co.R_CENTER] * 100)
import matplotlib.colors as colors

vmax = dvzr.quantile(.9)
vmin = vmax * 1e-3
dvzr.plot(
    # norm=colors.LogNorm(vmin=vmin, vmax=vmax),
    # xscale='log',
    vmax = vmax,
    figsize = (8,4),
    x='km', y=co.ZM)

plt.show()

# %%

# %%
# %%
# %%
# %%

# %%

# %%

# %%

# %%
