# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
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

# def main() :
from flexpart_management.modules.clustering_funs import \
    (
    get_con_norm_r_with_mask_over_threshold , plot_conc_norm_r ,
    print_mask_true_false ,
    multi_smoothing ,
    plot_sum_hist_df ,
    plot_distplot_scaled_v2 ,
    plot_distplot_scaled_vectors ,
    get_r_length ,
    plot_conc_over_distance ,
    clus_plot ,
    )

# %%
from flexpart_management.modules.constants import CONC_SMOOTH_NORM

plt.rcParams[ 'figure.facecolor' ] = 'white'
CONC_norm_r = 'CONC_norm_r'


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
ds = xr.open_dataset(
    os.path.join( selfFLP.datasets_path , 'ds_above_sea_level.nc' )
    )
# %%
# lets change nan to 0 so that they nan dont spread when smoothing
da:xr.DataArray = ds['CONC']
ds['CONC'] = da.where(~da.isnull(),0)
# %%
# lets smooth the dataset and define its name for later calling
var_dict = dict( r_var=[ 1 ] ,
                 th_var=[ .5 ] ,
                 z_var=[ .25 ] ,
                 t_var=[ 3 ] )
df_ , ds_smooth = \
    multi_smoothing( ds , **var_dict , con_var=co.CONC , truncate=3 )

conc_smooth_name = df_[ 'name_col' ][ 0 ]

# %%
ax_ops = { 'ylim' : (0 , 2.5) , 'xscale' : 'log' }
_ , ax = plt.subplots()
plot_conc_over_distance( ds , ax=ax , ax_ops=ax_ops )
plot_conc_over_distance( ds , ax=ax , ax_ops=ax_ops ,
                         conc_lab=conc_smooth_name )
ax.legend( bbox_to_anchor=(1.04 , 1) , borderaxespad=0 )
ax.set( **ax_ops )
ax.figure.tight_layout()
plt.show()
# %%
r_length = get_r_length( ds )
ds = ds.assign_coords( **{ 'r_length' : r_length } )
# %%
con_smooth_norm_r = ds[ conc_smooth_name ] / ds[ 'r_length' ]
conc_smooth_norm_r_name = 'conc_smooth_norm_r'
ds[ conc_smooth_norm_r_name ] = con_smooth_norm_r
# %%
c_sum_r = ds[ conc_smooth_norm_r_name ].sum(
    [ co.RL , co.ZM , co.TH_CENTER ] )
ds_over_r: xr.DataArray = ds[ conc_smooth_norm_r_name ] / c_sum_r
conc_smooth_norm = CONC_SMOOTH_NORM
desc = '''conc divided by the sum at each radial length. also smoothed'''
ds_over_r = ds_over_r.assign_attrs( desc=desc )
ds[ conc_smooth_norm ] = ds_over_r

# %%
ds[ conc_smooth_name ].sum( [ co.RL , co.ZM ] ).plot( yscale='log' )
plt.show()
ds[ co.CONC ].sum( [ co.RL , co.ZM ] ).plot( yscale='log' )
plt.show()
ds[ conc_smooth_norm_r_name ].sum( [ co.RL , co.ZM ] ).plot( yscale='log' )
plt.show()
# %%
ds[ conc_smooth_norm ].sum( [ co.RL , co.ZM ] ).plot( yscale='log' )
plt.gca().set_title( conc_smooth_norm )
plt.show()
# %%
# da: xr.DataArray = ds[ co.CONC ]
# ds[ co.CONC ] = da.where( ~da.isnull() , 0 )

# %%
ds = get_con_norm_r_with_mask_over_threshold(
    ds ,
    conc_label=conc_smooth_norm
    )
# %%
ds[ conc_smooth_norm ]
# %%
# %%
print_mask_true_false( ds[ conc_smooth_norm ] )
# %%
plot_conc_norm_r( ds[ conc_smooth_norm ] )
# %%
# %%
# df_ , ds = multi_smoothing( ds )
# ds: xr.Dataset
# # %%
# smooth_dict = df_.to_dict()
# ds = ds.assign_attrs( **{ 'smooth_dict' : smooth_dict } )
# chosen_smooth = 'chosen_smooth'
# th__ = {
#     chosen_smooth :
#         'CONC_norm_r_smooth_t_300_z_50_r_100_th_50'
#     }
# ds = ds.assign_attrs( **th__ )
# # %%
# multi_smooth_plot( CONC_norm_r , df_ , ds )
# %%
# %%
# dss: xr.DataArray = ds[ ds.attrs[ chosen_smooth ] ]
dss: xr.DataArray = ds[ conc_smooth_norm ]
dss_above: xr.DataArray = dss.where( dss[ co.above_thre_label ] )
# %%

_da = dss_above.reset_coords( drop=True )
_df = _da.to_dataset( dim=co.RL ).to_dataframe()
# %%
log.ger.debug( len( _df ) )
_df1 = _df.dropna( axis=0 , how='all' )
log.ger.debug( len( _df1 ) )
# %%
scaler = RobustScaler(
    with_centering=False , quantile_range=(0 , 95) )
scaler = QuantileTransformer()
_dft = scaler.fit_transform( _df1.T ).T
# %%
_dft
# %%
plt.hist( _dft[ : , 23 ] )
plt.gca().set_title( 'dist over dime 2' )
plt.show()
plt.hist( _dft[ 23 ] )
plt.gca().set_title( 'dist over dime 1' )
plt.show()
# %%
print( _dft[ 23 ].shape )
print( _dft[ : , 23 ].shape )
# %%
log.ger.debug( f'shape of dft {_dft.shape}' )
# %%
# %%
plot_distplot_scaled_vectors( _dft )

# %%
plot_distplot_scaled_v2( _dft )
# df_uns = df_conc.unstack(level=0)
# %%
# %%
df__sum = plot_sum_hist_df( _df1 )
n_clusters = 18

k_means = KMeans(
    n_clusters=n_clusters , random_state=0 )

k_means = k_means.fit( _dft , sample_weight=df__sum )
labels_ = k_means.labels_

# %%
# %%
log.ger.debug( f'labels shape: {labels_.shape}' )
# %%
plt.hist( labels_ , bins=np.arange( -.5 , n_clusters + .5 , 1 ) )
ax: plt.Axes = plt.gca()
ax.set_xticks( range( n_clusters ) )
ax.set_xlabel( 'cluster n.' )
ax.set_ylabel( 'n cells in cluster' )
plt.show()

# %%
# ds_reset_coords = ds[ ds.attrs[ chosen_smooth ] ].reset_coords(
# drop=True )
ds_reset_coords = ds[ conc_smooth_norm ].reset_coords( drop=True )
_df = ds_reset_coords.to_dataset( co.RL ).to_dataframe()
# %%
_df_t_full = scaler.fit_transform( _df.T ).T
# %%
df_scaled: pd.DataFrame = _df.copy()
df_scaled[ : ] = _df_t_full
# %%
df_scaled.columns.name = co.RL
df_stacked = df_scaled.stack()
# %%
df_stacked.isnull().value_counts()
# %%
df_over_zero = df_stacked[ df_stacked > -1 ]
sns.distplot( df_over_zero.sample( 10000 ) )
plt.show()
# %%
# this line take too long to run for some reason
# ds[ 'scaled' ] = df_stacked.to_xarray()
# %%
full = _df_t_full.copy()
full[ ~(full > 0) ] = 0
# %%
labs = k_means.predict( full )
# %%
lab_df = _df[ [ ] ].copy()
lab_df[ 'lab' ] = labs
lab_df
# %%
ds[ 'lab' ] = lab_df[ 'lab' ].to_xarray()

# %%
lab__sum = ds.groupby( 'lab' ).sum()
# %%
ds_vars = list( lab__sum.variables )
for v in ds_vars :
    lab__sum[ v ].plot()
    ax: plt.Axes = plt.gca()
    ax.set_xticks( range( n_clusters ) )
    ax.set_xlabel( 'cluster n.' )
    # ax.set_ylabel('n cells in cluster')
    plt.show()

# %%
selfFLP.save_ds_version(
    ds=ds ,
    file_name='ds_clustered_18.nc' ,
    attrs={ 'clustered' : 1 , 'n_clusters' : 8 }
    )
# %%
# for i in range( n_clusters ) :
for i in [ 1 , 13 , 10 ] :
    clus_plot( i ,
               ds ,
               # conc_lab= co.CC,
               conc_lab=conc_smooth_norm ,
               )
# %%

plt.figure( dpi=300 )
# for i in range( n_clusters ) :
for i in [ 1 , 13 , 10 ] :
    dl: xr.DataArray = ds.where( ds[ 'lab' ] == i )[ co.CONC ]
    dl = dl.sum( [ co.TH_CENTER , co.R_CENTER , co.ZM ] )
    dl.plot( label=i )
plt.gca().legend()
plt.show()
# %%
# %%
# %%

# %%

# %%

# %%

# main()
