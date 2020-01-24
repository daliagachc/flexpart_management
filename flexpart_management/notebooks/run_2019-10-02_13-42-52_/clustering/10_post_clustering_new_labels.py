# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
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

# %% [markdown]
# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# %%
# %% [markdown]
# imports
# %%

from useful_scit.imps import *
# noinspection PyUnresolvedReferences
import matplotlib.colors
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
# noinspection PyUnresolvedReferences
import flexpart_management.modules.flx_array as fa
# %%
from sklearn.preprocessing import RobustScaler, QuantileTransformer
from sklearn.cluster import KMeans

import flexpart_management.modules.clustering_funs as cfuns
import cluster_local_funs as lfuns

# %%


log.ger.setLevel(log.log.DEBUG)
# %%
temp_path = co.tmp_data_path
name = 'ds_clustered_18.nc'
ds = xr.open_mfdataset(os.path.join(temp_path, name), concat_dim=co.RL,
                       combine='nested')
# %%
df_prop = pd.read_csv(co.prop_df_path)
# %%

# %%
# ds_small = ds[{co.RL:slice(None,None,100)}]

# %%
n_clusters = 18
for i in range(n_clusters):
    # for i in [  ] :
    name_ = df_prop.set_index('cluster_i')['short_name'][i]
    fig = cfuns.clus_plot(
        i,
        ds,
        # conc_lab= co.CC,
        conc_lab=co.CONC,
        fig_title=name_,
        df_prop = df_prop
    )
    out_path =  os.path.join(lfuns.FIG_PATH, name_ + '.pdf')
    fig.savefig(out_path)
# %%
# %%

# %%

# %%

# %%

# %%
