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
from sklearn.preprocessing import RobustScaler , QuantileTransformer
from sklearn.cluster import KMeans

import flexpart_management.modules.clustering_funs as cfuns

# %%

plt.rcParams[ 'figure.facecolor' ] = 'white'


# %%

# def main() :
# %%
# %%

log.ger.setLevel( log.log.DEBUG )
# %%
# noinspection SpellCheckingInspection
path = \
    '/homeappl/home/aliagadi/wrk/DONOTREMOVE' \
'/flexpart_management_data/runs/' \
'run_2019-10-02_13-42-52_/' \
'log_pol/run_2019-10-02_13-42-52_'
# flp = FLP.FlexLogPol(path,concat=True)
# flp_instance = FLP.FlexLogPol(path,concat=False)
selfFLP = FlexLogPol.FlexLogPol(
    path ,
    # concat=True,
    concat=False ,
    get_clusters=False ,
    # open_merged=False,
    open_merged=True ,
    # merge_ds=False ,
# merge_ds=True ,
    clusters_avail=False ,

    # postprocess set to false since we are opening the reinterpolated
# version
    postprocess=False ,

    use_new_merge_fun=True ,

    # set to false bc already done in the saved version
    filter_r_min_max=False ,
    )
# %%
selfFLP.get_list_datasets_saved()
# %%
# ds = re_interpolate_merged_processed_ds_and_save( selfFLP )
ds = selfFLP.open_ds_version('ds_clustered_18.nc')

# %%
# ds_small = ds[{co.RL:slice(None,None,100)}]

# %%
n_clusters = 18
for i in range( n_clusters ) :
# for i in [  ] :
    cfuns.clus_plot( i ,
               ds ,
               # conc_lab= co.CC,
               conc_lab=co.CONC_SMOOTH_NORM ,
               )
# %%

# %%

# %%

# %%

# %%

# %%
