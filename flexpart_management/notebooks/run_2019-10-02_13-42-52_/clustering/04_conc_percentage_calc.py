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
import flexpart_management.modules.clustering_funs as cfuns
from flexpart_management.modules.clustering_funs import (
    add_total_per_row ,
    add_time_per_row ,
    )

plt.rcParams[ 'figure.facecolor' ] = 'white'
co.LAB = 'lab'

plt.style.use('seaborn-whitegrid')
plt.rcParams["legend.frameon"] = True
plt.rcParams["legend.fancybox"] = True

# %%
# def main() :

log.ger.setLevel( log.log.DEBUG )

# %%
# noinspection PyUnusedLocal,PyShadowingNames
def open_if_taito() :
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

                 # postprocess set to false since we are opening the re interpolated
                 # version
                 postprocess=False ,

                 use_new_merge_fun=True ,

                 # set to false bc already done in the saved version
                 filter_r_min_max=False ,
                 )
                 selfFLP.get_list_datasets_saved()
                 # noinspection PyUnresolvedReferences
                 ds = selfFLP.open_ds_version( 'ds_clustered_18.nc' )
                 return selfFLP , ds


# %%
# selfFLP,ds = open_if_taito()
path = '/Users/diego/flexpart_management/flexpart_management/tmp_data' \
   '/ds_clustered_18.nc'
ds = xr.open_dataset( path )
# %%
# %%
# %%
conc_lab = 'CONC_smooth_t_300_z_25_r_100_th_50'
new_lab_p = 'conc_smooth_p'
new_lab_p_t = 'conc_smooth_p_t'
add_total_per_row( ds , conc_lab , new_lab_p )
add_time_per_row( ds , conc_lab , new_lab_p_t )
# print( da_tot )

# %%
# ds[new_lab_p].sum([co.RL,co.ZM],keep_attrs=True).plot()
# plt.show()
# ds[new_lab_p_t].sum(fa.get_dims_complement(ds,co.RL),keep_attrs=True).plot()
# plt.show()

# %%
n_clusters = 18
for i in range(n_clusters) :
    # for i in [  ] :
    cfuns.clus_plot( i ,
                     ds ,
                     # conc_lab= co.CC,
                     conc_lab=new_lab_p ,
                     figure_size=12,
                     dpi=100,
                     conc_lab_ts = new_lab_p_t
                     )

plt.show()
# %%
# main()


# %%

# %%


#

# %%

# %%

# %%
