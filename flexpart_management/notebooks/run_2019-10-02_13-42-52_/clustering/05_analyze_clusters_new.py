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
import flexpart_management.modules.clustering_funs as cfuns
# %%
from sklearn.cluster import KMeans

import flexpart_management.modules.clustering_funs as cfuns

co.LAB = 'lab'


def re_cluster( _df , nc , df_labs ) :
    k_means = KMeans( n_clusters=nc , random_state=0 )
    labs = k_means.fit_predict( _df )
    print( labs.shape )
    df_labs[ nc ] = labs


def get_lab_ds_current_i( * , meta_cluster_i , current_i ,
                          df_labs , ds_re_lab , ds_sum ) :
    clus_bool = (df_labs[ meta_cluster_i ] == current_i)
    list_labs = df_labs[ clus_bool ].index.values
    print( list_labs )
    _bool = ds_sum[ co.LAB ].isin( list_labs )
    ds_re_lab[ co.LAB ] = ds_re_lab[ co.LAB ].where( ~_bool , current_i )
    # return _bool


def get_re_lab_ds( * , ds , ds_sum , df_labs , meta_cluster_i , ) :
    # noinspection PyShadowingNames
    ds_re_lab = ds.copy()
    # noinspection PyShadowingNames
    for current_i in range( meta_cluster_i ) :
        get_lab_ds_current_i(
            meta_cluster_i=meta_cluster_i ,
            current_i=current_i ,
            df_labs=df_labs ,
            ds_sum=ds_sum ,
            ds_re_lab=ds_re_lab ,
            )
    return ds_re_lab


# def main() :
# %%

plt.rcParams[ 'figure.facecolor' ] = 'white'

# %%

# %%
# %%

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

def get_ds_re_lab_title( current_i , df_labs , meta_cluster_i ) :
    _b = df_labs[ meta_cluster_i ] == current_i
    clust_labs_str = str( df_labs[ meta_cluster_i ][ _b ].index.values )
    title = f'c:{current_i}/{meta_cluster_i} | {clust_labs_str}'
    return title

# %%
# selfFLP,ds = open_if_taito()
path = '/Users/diego/flexpart_management/flexpart_management/tmp_data' \
       '/ds_clustered_18.nc'
ds = xr.open_dataset( path )

conc_lab = 'CONC_smooth_t_300_z_25_r_100_th_50'
new_lab_p = 'conc_smooth_p'
new_lab_p_t = 'conc_smooth_p_t'
cfuns.add_total_per_row( ds , conc_lab , new_lab_p )
cfuns.add_time_per_row( ds , conc_lab , new_lab_p_t )
# %%
# ds = re_interpolate_merged_processed_ds_and_save( selfFLP )

# %%
# ds_small = ds[{co.RL:slice(None,None,100)}]

 # %%
ds = ds.transpose( 'R_CENTER' , 'TH_CENTER' , 'ZMID' , 'releases' )
ds = ds.assign_coords( **{ co.LAB : ds[ co.LAB ] } )

# %%
# df = ds[new_lab_p].to_dataframe()

# %%
ds_trimmed = ds[ new_lab_p ].reset_coords()[ [ new_lab_p , co.LAB ] ]
df: pd.DataFrame = ds_trimmed.to_dataframe()
# %%
cols = list( df.columns )
df_trimmed = df.reset_index()[ [ *cols , co.RL ] ]
# %%

df_g = df_trimmed.groupby( [ co.LAB , co.RL ] )

# %%
df_s = df_g.sum()

# %%
da_lab = df_s.to_xarray()[ new_lab_p ].transpose( co.LAB , co.RL )
# %%
data = da_lab.data
# noinspection PyStatementEffect
data.shape
# %%
from sklearn.preprocessing import QuantileTransformer
scaler = QuantileTransformer()
data_transformed = scaler.fit_transform( data.T ).T
# %%
vector = data_transformed[ 2 ]
print( vector.shape )
# sns.distplot( vector )

# plt.show()
# %%
da_lab_transformed = da_lab.copy()
da_lab_transformed.data = data_transformed
# %%
# da_lab_transformed.plot( cmap=plt.get_cmap( 'Reds' ) )
# plt.show()
# %%
_df: pd.DataFrame = da_lab_transformed.transpose( co.RL ,
                                                  co.LAB ).to_dataframe()
_df = _df.unstack( 0 ).iloc[ : , : ]
print( _df )
# _df.T.plot.scatter( x=9 , y=10 , alpha=.1 , s=100 )
# plt.show()
# %%
meta_cluster_list = [ 2 , 4 , 6 , 8 ]
df_labs = pd.DataFrame( [ ] , _df.index )
df_labs.columns.name = 'num_clus'
for i in meta_cluster_list :
    re_cluster( _df , i , df_labs=df_labs )
# %%

# %%
ds_sum = ds[ new_lab_p ].sum( co.RL )
# %%
# meta_cluster_i = 4
# current_i = 3

# %%

# %%

# %%

for meta_cluster_i in meta_cluster_list :
    # ds_re_lab = ds.copy()
    ds_re_lab = get_re_lab_ds( ds=ds , ds_sum=ds_sum , df_labs=df_labs ,
                               meta_cluster_i=meta_cluster_i )
    for current_i in range( meta_cluster_i ) :
        # re_lab_ds( meta_cluster_i , current_i , df_labs , ds_sum )

        title = get_ds_re_lab_title( current_i , df_labs , meta_cluster_i )

        cfuns.clus_plot(
            ds=ds_re_lab , i_lab=current_i ,
            conc_lab=new_lab_p ,
            conc_lab_ts=new_lab_p_t,
            dpi=100 ,
            figure_size=10 ,
            fig_title=title,

            )

        plt.show()




# %%

# %%
