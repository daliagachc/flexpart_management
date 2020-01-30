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
import n0_sfc_ratio_clusters_lfc as lfc #local functions and constants
import flexpart_management.modules.constants as co

# %%
from n0_sfc_ratio_clusters_lfc import \
    create_sfc_tot_ds_with_attrs
from useful_scit.imps import *
ucp
# %%
def main():
    # %%
    ds_zs,ds_zg,prop_df = lfc.fa.import_datasets()
    ds_zs['lab'] = ds_zs['lab'][{co.RL: [0]}].sum(co.RL).load()
    ds_zg = ds_zg.loc[{co.R_CENTER:ds_zs[co.R_CENTER]}]

    # %%
    lab_name_dict = prop_df.set_index('cluster_i')['short_name'].to_dict()
    # %%
    dsm = lfc.get_lab_agl(ds_zg, ds_zs, lab_name_dict)
    # %%
    tts = lfc.get_time_series_sfc_tot(dsm, lab_name_dict)
    # %%
    tsdf = lfc.get_time_series_df(tts)
    # %%
    new_ds:xr.Dataset = lfc.create_sfc_tot_ds_with_attrs(tsdf)
    path_out = '/Users/diego/flexpart_management/flexpart_management/' \
               'releases/v02/srr_sfc_tot_clus/srr_sfc_tot_clus.nc'
    new_ds.to_netcdf(path_out)

    # %%
    lfc.plot_ts_conc_sfc_tot(lab_name_dict, tsdf)
    # %%
    lfc.plot_scatter_sfc_tot(lab_name_dict, tsdf)
    # %%
    lfc.plot_ratio_clusters(prop_df,tsdf)

    # %%


