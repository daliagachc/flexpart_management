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
#     display_name: PyCharm (flexpart_management)
#     language: python
#     name: pycharm-1dd40459
# ---

# %%
# local functions and constants

# from n0_explore_cluster_vertical_dist_lfc import *
# import n0_explore_cluster_vertical_dist_lfc as lfc

import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array
import n0_explore_cluster_vertical_dist_lfc as lfc

# %%
from n0_explore_cluster_vertical_dist_lfc import plot_histogram_vertical_masl

ds, ds_zg, prop_df = flexpart_management.modules.flx_array.import_datasets()
# %%
comp_dim, da_conc, da_norm, da_zi_cumsum = lfc.process_ds_zg(ds_zg,cum_sum_start=0)
# %%

# %%
lfc.plot_cum_sum(da_zi_cumsum)
# %%
lfc.plot_norm_cum_sum(da_norm)
# %%
da_z0 = da_zi_cumsum[{co.ZM:0}]
# %%


# %%
lfc.plot_z0_timeseries(da_z0)

# %%
df0, ds_z0 = lfc.savgol_filtering(da_z0)
# %%
lfc.plot_sg_filter(da_z0, ds_z0)
# %%
lfc.plot_diurnal_variation_z0_level(df0)

# %%
lfc.notation_for_diurnal_plot()
# %%
comp_dim, da_conc, da_norm, da_zi_cumsum =\
    lfc.process_ds_zg(ds_zg,cum_sum_start=6)

da_zFT = da_zi_cumsum[{co.ZM:-1}]
# %%
lfc.plot_z0_timeseries(da_zFT)

# %%
dfFT, ds_zFT = lfc.savgol_filtering(da_zFT)
# %%
lfc.plot_sg_filter(da_zFT, ds_zFT)
# %%
lfc.plot_diurnal_variation_z0_level(dfFT)

# %% [markdown]
# cells above grid 6 ~ 3km

# %%
lfc.plot_histogram_vertical_masl(da_conc,ds)

# %%
