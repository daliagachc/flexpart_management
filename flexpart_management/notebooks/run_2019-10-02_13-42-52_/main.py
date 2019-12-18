# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
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

# %%
from useful_scit.imps import *
from xarray import Dataset

import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

import flexpart_management.modules.clustering_funs as funs

mpl.rcParams[ 'figure.dpi' ] = 150

log.ger.setLevel( log.log.DEBUG )

# %%
# def main():

# %%
path = \
    '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/' + \
    'run_2019-10-02_13-42-52_/log_pol/run_2019-10-02_13-42-52_'
# flp = FLP.FlexLogPol(path,concat=True)
    # selfFLP = FLP.FlexLogPol(path,concat=False)
selfFLP = FlexLogPol.FlexLogPol(
    path ,
    # concat=True,
    concat=False ,
    get_clusters=False ,
#     open_merged=False,
    open_merged=True ,
    # merge_ds=False ,
    merge_ds=True ,
    clusters_avail=False ,
    postprocess=True ,
    use_new_merge_fun=True
    )

# %%
dsF = selfFLP.merged_ds
_ds = dsF[co.CC][{co.RL:200,co.ZM:1}]
_ds.plot(yscale='log')
plt.show()

# %%
selfFLP.reset_z_levels()

# %%
dsF = selfFLP.filter_hours_with_few_mea()

# %%
dsSM = ds1 = FlexLogPol.smooth_merged_ds(
    dsF, t=3 , z=.5 , r=.4 , th=.4
    )



# %%
funs.plot_general( ds1 )
plt.show()
funs.plot_general( selfFLP.merged_ds )
plt.show()

# %%
funs.plot_general_lapaz( ds1 )
plt.show()
funs.plot_general_lapaz( selfFLP.merged_ds )
plt.show()

# %%
dsZ = dsSM.copy()
dfcc = selfFLP.get_vector_df_for_clustering( selfFLP.coarsen_par ,
                                             ar=dsZ[ co.CONC ] )

# %%
funs.plot_hist_values( dfcc )
plt.show()

# %%
funs.plot_hist_all_values( dfcc )
plt.show()

# %%

# %%

# lest create the dataset again
dscc = funs.rebuild_the_dscc( dfcc )

funs.print_percentage_res_time_mass_considered( dscc )

# %%

MAX_LENGTH = 25
dscc = funs.preprocess_dscc_for_clustering( MAX_LENGTH , dscc )

# %%
funs.plot_cells_used_for_clustering( dscc )

# %%
funs.plot_sample_of_vectors_norm_used_for_clustering( dscc )

# %%
funs.plot_hist_all_log( dscc[ co.CONC_NORMS ] )

# %%
funs.plot_hist_all_log(
    dscc[ co.CONC_NORMS ].where( dscc[ co.LAB_CLUSTER_THRESHOLD ] ) )

# %%
# this one take a long time
dscc = funs.do_clust_multiple( dscc )

# %%
funs.plot_bar_charts_for_each_cluster_set( dscc )

# %%

# %%
dscc = funs.calc_silhouette_scores( dscc )

dscc[ co.SIL_SC ].plot()

# %%
# ii = 2

# %%
# _d = dscc.loc[{co.CLUS_LENGTH_DIM:ii}][[co.FLAG,co.SIL_SC,
# SIL_SAMPLE]].stack({co.DUM_STACK:[co.R_CENTER,co.TH_CENTER,co.ZM]})

# %%
funs.plot_sil_score_grid( dscc )

# %%
_n = 4
# _f = 2
_ss1 = funs.get_df_for_plot( _n , dscc )

# %%
_ss1.plot( sharex=True , sharey=True , layout=(2 , -1) , subplots=True ,
           figsize=(10 , 5) , color=ucp.cc ) ;

# %%
_ss1.plot.area( legend=True , figsize=(12 , 6) , color=ucp.cc )

# %%
dscc

# %%
dscc = funs.add_lat_lon_to_dscc( dscc , selfFLP )

# %%
funs.plot_clust_in_bolivia( _n , dscc )

# %%
_n = 18
funs.plot_clust_in_lapaz( _n , dscc )

# %%

_n = 18
funs.plot_clust_bolivia_individual( _n , dscc )

# %%
_f = 2
_n = 18
funs.plot_distance_height_chc( _n , dscc )

# %%
dscc = funs.add_dis_km_dscc( dscc )

# %%
dsF[ co.TOPO ]

# %%
mpl.rcParams[ 'figure.dpi' ] = 300
_cols = 6
_rows = 3
fig , axs = plt.subplots( _rows , _cols , sharex=True , sharey=True ,
                          figsize=(3.5 * _cols , 2.5 * _rows) )
axsf = axs.flatten()

log.ger.setLevel( log.log.ERROR )
_ds = funs.plot_dis_height_quantiles_chc( _n , dsF , dscc , axs=axsf )
fig.tight_layout()

# %%
mpl.rcParams[ 'figure.dpi' ] = 300
_cols = 6
_rows = 3
fig , axs = plt.subplots( _rows , _cols , sharex=True , sharey=True ,
                          figsize=(3.5 * _cols , 2.5 * _rows) )
axsf = axs.flatten()

log.ger.setLevel( log.log.ERROR )

# %%
for _f in range( _n ) :
    ax = axsplot( figsize=(5 , 4) )
    funs.plot_dis_height_quantiles_chc_single( _f , _n , dsF , dscc , axs=ax )

# %%

# %%
# !jupyter-nbconvert --to markdown main.ipynb

# %%
dscc[ co.CONC ].sum( [ co.TH_CENTER , co.ZM , co.RL ] ).plot()

# %%
dscc[ co.CONC ].sum( [ co.TH_CENTER , co.RL ] ).plot.line( x=co.R_CENTER ) ;

# %%
_n = 18
funs.plot_influences( _n , dscc )

# %%
less_than = 1000000
more_than = 0
height_less_than = 100000000

_ds = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ].copy()
try : _ds = _ds.drop( co.KMEAN_OBJ )
except : pass

_dss = _ds.copy()
_ds[ co.CONC ] = _ds[ co.CONC ].where( dscc[ co.R_CENTER ] < less_than ,
                                       0 ).where(
    dscc[ co.R_CENTER ] > more_than , 0 ).where(
    dscc[ co.ZM ] < height_less_than , 0 )
_ds1 = _ds[ [ co.CONC , co.FLAG ] ]
_dss1 = _dss[ [ co.CONC , co.FLAG ] ]
_ds2 = _ds1.to_dataframe()
_dss2 = _dss1.to_dataframe()
_ds3 = _ds2[ [ co.CONC , co.FLAG ] ]
_dss3 = _dss2[ [ co.CONC , co.FLAG ] ]
_df = _ds3.reset_index( [ co.R_CENTER , co.TH_CENTER , co.ZM ] ,
                        drop=True ).reset_index().set_index(
    [ co.FLAG , co.RL ] )
_dff = _dss3.reset_index( [ co.R_CENTER , co.TH_CENTER , co.ZM ] ,
                          drop=True ).reset_index().set_index(
    [ co.FLAG , co.RL ] )
_df1 = _df.sort_index().groupby( [ co.FLAG , co.RL ] ).sum()
_dff1 = _dff.sort_index().groupby( [ co.FLAG , co.RL ] ).sum()
_df2 = _df1.unstack( co.FLAG )[ co.CONC ]
_dff2 = _dff1.unstack( co.FLAG )[ co.CONC ]
_df2 = 100 * (_df2.T / _dff2.T.sum()).T

# %%
_f = 1
for _f in range( _n ) :
    ax = axsplot()
    _df3 = _df2[ _f ]
    ax = _df3.plot( figsize=(15 , 1.5) ,
                    color=[ [ *ucp.cc , *ucp.cc ][ _f ] ] )
    ax.set_title( f'{_f}' )
    ax.set_ylabel( 'SRR [%]' )

# %%
_n = 18
less_than = .5
more_than = .05
height_less_than = 1000

funs.plot_target_distance_height_influence( _n , dscc , height_less_than ,
                                            less_than , more_than )

# %%

_n = 18
# %%
mdsc = selfFLP.merged_ds.copy()

# %%
_dscc = dscc.drop( [ co.KMEAN_OBJ , co.CONC , co.CONC_NORMALIZED , co.RL ] )
_dscc = xr.merge( [ mdsc , _dscc ] )
_dscc[ co.CONC ] = _dscc[ co.CONC ].where(
    _dscc[ co.CONC ].sum( [ co.R_CENTER , co.TH_CENTER , co.ZM ] ) > 2e5 )
_dscc[ co.CONC ] = _dscc[ [ co.CONC ] ].resample( releases='H' ).mean()[
    co.CONC ]

# %%
_n = 18
funs.plot_influences( _n , _dscc )

# %%
_n = 18
less_than = .3
more_than = .15
height_less_than = 1000

funs.plot_target_distance_height_influence( _n , _dscc , height_less_than ,
                                            less_than , more_than )

# %%
_ns = [ 0 , 2 , 8 , 9 , 11 , 14 ]

for _nn in _ns :
    funs.plot_hour_influence_targeted( _n , _nn , _dscc , height_less_than ,
                                       less_than , more_than )

# %%
