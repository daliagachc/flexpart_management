# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
# ---

# %%
import os

import pandas
import sklearn.metrics
import cartopy.mpl.geoaxes
from matplotlib import colors as mpl_colors, pyplot
from sklearn import preprocessing
from sklearn.cluster import KMeans
# from useful_scit import plot
from useful_scit.imps import *


# from main import dfcc
from flexpart_management.modules import (
    flx_array as fa , constants as co ,
    FlexLogPol as FlexLogPol ,
    )

R_DIS_KM = 'r_dis_km'


def plot_general( ds1 ) :
    cl = co.CPer
    c1 = ds1[ cl ].sum( [ co.RL , co.ZM ] )
    c2 = ds1[ cl ].sum( [ co.ZM , co.RL , co.TH_CENTER ] )
    ar = c1 / c2
    # ar = c1
    ar = ar.isel( **{ co.R_CENTER : slice( 0 , -3 ) } )
    ax = fa.get_ax_bolivia( fig_args={ 'figsize' : (5 , 5) } )
    fa.logpolar_plot( ar , name=co.CPer , ax=ax , perM=.95 , perm=.01 )
    ax.set_xlim( -75 , -60 )
    ax.set_ylim( -25 , -7 )
    return ax


def plot_general_lapaz( ds1 ) :
    cl = co.CPer
    c1 = ds1[ cl ].sum( [ co.RL , co.ZM ] )
    c2 = ds1[ cl ].sum( [ co.ZM , co.RL , co.TH_CENTER ] )
    ar = c1 / c2
    # ar = c1
    ar = ar.isel( **{ co.R_CENTER : slice( 0 , -3 ) } )
    ax = fa.get_ax_lapaz( fig_args={ 'figsize' : (5 , 5) } )
    fa.logpolar_plot( ar , name=co.CPer , ax=ax , perM=.95 , perm=.01 )
    # ax.set_xlim(-75, -60)
    # ax.set_ylim(-25, -7)
    return ax


def plot_hist_log( dfcc , cumulative=False , ax=None , nbins=20 ) :
    _fl = dfcc.sum( axis=1 ).values
    bins = np.logspace(
        np.log10( _fl.max() * 1e-5 ) ,
        np.log10( _fl.max() ) ,
        nbins
        )
    bins = [ -bins[ 0 ] , 0 , *bins ]
    if ax is None :
        f , ax = plt.subplots()
    else :
        ax = ax
    ax.hist(
        _fl ,
        bins=bins ,
        weights=[ 100 / len( _fl ) ] * len( _fl ) ,
        cumulative=cumulative ,
        alpha=.5
        )
    ax: plt.Axes
    ax.set_xscale( 'log' )
    # noinspection PyTypeChecker
    ax.set_xlim( (bins[ 2 ] * .5 , bins[ -1 ]) )
    ax.set_xlabel( 'mass*res.time ' )
    ax.set_ylabel( '%' )
    cell_tile = "Sum Values over cell"
    if cumulative is True :
        cell_tile = cell_tile + ' (cumulative)'
    ax.set_title( cell_tile )


def plot_hist_all_log( dfcc , cumulative=False , ax=None ) :
    _fl = dfcc.values.flatten()

    bins = np.logspace(
        np.log10( dfcc.max().max() * 1e-5 ) ,
        np.log10( dfcc.max().max() ) ,
        10
        )
    bins = [ -bins[ 0 ] , 0 , *bins ]
    if ax is None :
        f , ax = plt.subplots()
    else :
        ax = ax
    ax.hist(
        _fl ,
        bins=bins ,
        weights=[ 100 / len( _fl ) ] * len( _fl ) ,
        cumulative=cumulative ,
        alpha=.5
        )
    ax.set_xscale( 'log' )
    ax: plt.Axes
    # ax.set_xscale('symlog')
    # noinspection PyTypeChecker
    ax.set_xlim( (bins[ 2 ] * .5 , bins[ -1 ]) )
    ax.set_xlabel( 'mass*res.time ' )
    ax.set_ylabel( '%' )
    cell_tile = "All Values over cell"
    if cumulative is True :
        cell_tile = cell_tile + ' (cumulative)'
    ax.set_title( cell_tile )


def plot_silhouette_score(
        n_c ,
        sample_silhouette_values ,
        cluster_labels ,
        ax1 ,
        silhouette_avg
        ) :
    y_lower = 10
    for i in range( n_c ) :
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[ cluster_labels == i ]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[ 0 ]
        y_upper = y_lower + size_cluster_i

        color = [ *ucp.cc , *ucp.cc ][ i ]
        ax1.fill_betweenx( np.arange( y_lower , y_upper ) ,
                           0 , ith_cluster_silhouette_values ,
                           facecolor=color , edgecolor=color , alpha=0.7 )

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text( -0.05 , y_lower + 0.5 * size_cluster_i , str( i ) )

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples
    # ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_title( str( n_c ) )
    ax1.set_xlabel( "The silhouette coefficient values" )
    ax1.set_ylabel( "Cluster label" )
    # The vertical line for average silhouette score of all the values
    ax1.axvline( x=silhouette_avg , color="red" , linestyle="--" )
    # ax1.axvline(x=sil_avg, color="red", linestyle="-")
    ax1.set_yticks( [ ] )  # Clear the yaxis labels / ticks
    # ax1.set_xticks([-0.1, 0, 0.2, 0.4])


# %%

# ax = fa.get_ax_lapaz()
# fa.logpolar_plot(ar,name=co.CPer,ax=ax,perM=.95)


def plot_hist_values( dfcc ) :
    # global f, axs
    f , axs = plt.subplots( 1 , 2 , figsize=(10 , 5) )
    axs = axs.flatten()
    plot_hist_log( dfcc , ax=axs[ 0 ] )
    plot_hist_log( dfcc , cumulative=True , ax=axs[ 1 ] )
    f: plt.Figure
    f.tight_layout()


def plot_sil_score_grid( dscc ) :
    fig = plt.figure( figsize=(20 , 40) )
    for i in range( len( dscc[ co.CLUS_LENGTH_DIM ] ) ) :
        ii = dscc[ co.CLUS_LENGTH_DIM ][ i ].item()
        _d = dscc.loc[ { co.CLUS_LENGTH_DIM : ii } ][
            [ co.FLAG , co.SIL_SC , co.SIL_SAMPLE ] ].stack(
            { co.DUM_STACK : [ co.R_CENTER , co.TH_CENTER , co.ZM ] } )
        if i == 0 :
            ax0 = ax = fig.add_subplot( 5 , 5 , i + 1 )
        else :
            # noinspection PyUnboundLocalVariable
            ax = fig.add_subplot( 5 , 5 , i + 1 , sharex=ax0 )

        plot_silhouette_score(
            n_c=ii ,
            silhouette_avg=_d[ co.SIL_SC ] ,
            sample_silhouette_values=_d[ co.SIL_SAMPLE ].values ,
            cluster_labels=_d[ co.FLAG ].values ,
            ax1=ax
            )


def calc_silhouette_scores( dscc ) :
    _fl = dscc.where( dscc[ co.LAB_CLUSTER_THRESHOLD ] )[
        [ co.FLAG , co.CONC_NORMALIZED ] ].stack(
        { co.DUM_STACK : [ co.R_CENTER , co.TH_CENTER , co.ZM ] } )
    # %%
    _fl = _fl.dropna( co.DUM_STACK )
    # %%
    _cl = _fl[ co.CLUS_LENGTH_DIM ]
    # %%
    # noinspection PyTypeChecker
    _sil_sc = xr.full_like( dscc[ co.CLUS_LENGTH_DIM ] , np.nan , float )
    _sil_sc.name = co.SIL_SC
    for i , _ in _cl.to_series().iteritems() :
        #     print(i)
        _labs = _fl.sel( **{ co.CLUS_LENGTH_DIM : i } )[ co.FLAG ]
        _CC = _fl.sel( **{ co.CLUS_LENGTH_DIM : [ i ] } )[ co.CONC_NORMALIZED ]
        _scc = sklearn.metrics.silhouette_score( _CC.T , _labs )
        _sil_sc.loc[ { co.CLUS_LENGTH_DIM : i } ] = _scc
    # %%
    # noinspection PyBroadException
    try :
        dscc = dscc.drop( co.SIL_SC )
    except :
        pass
    dscc = xr.merge( [ dscc , _sil_sc ] )
    # %%
    # %%
    # noinspection PyTypeChecker
    _sil_sa = xr.full_like( _fl[ co.FLAG ] , np.nan , float )
    _sil_sa.name = co.SIL_SAMPLE
    for i , _ in _cl.to_series().iteritems() :
        print( i )
        _labs = _fl.sel( **{ co.CLUS_LENGTH_DIM : i } )[ co.FLAG ]
        _CC = _fl.sel( **{ co.CLUS_LENGTH_DIM : [ i ] } )[ co.CONC_NORMALIZED ]
        _scc = sklearn.metrics.silhouette_samples( _CC.T , _labs )
        _sil_sa.loc[ { co.CLUS_LENGTH_DIM : i } ] = _scc
    # %%
    # noinspection PyBroadException
    try :
        dscc = dscc.drop( co.SIL_SAMPLE )
    except :
        pass
    dscc = xr.merge( [ dscc , _sil_sa.unstack() ] )
    return dscc


def plot_bar_charts_for_each_cluster_set( dscc ) :
    _ser = dscc[ co.FLAG ].to_series()
    _ser = _ser.groupby( co.CLUS_LENGTH_DIM ).value_counts().sort_index()
    # %%
    _s1 = _ser.unstack( co.FLAG ).T
    # %%
    _s1.plot.bar( subplots=True , layout=(-1 , 4) , figsize=(20 , 10) ,
                  legend=False )


def do_clust_multiple( dscc ) :
    _co = co.CONC_NORMALIZED
    dscc_lab = dscc[ co.LAB_CLUSTER_THRESHOLD ]
    dscc_df = dscc[ _co ].where( dscc_lab ).to_dataframe()
    _ser = dscc_df[ _co ].dropna()
    _ser = _ser.unstack( co.RL )
    # %%
    _co = co.CONC_NORMS
    dscc_df = dscc[ _co ].where( dscc_lab ).to_dataframe()[ _co ]
    _wei = dscc_df.dropna()
    _wei = _wei / _wei.median()

    # _wei = _wei.unstack(co.RL)
    # %%
    # %%
    def set_kmeans( n_c , _ser , _wei ) :
        #     n_c = 30
        kmeans = KMeans( n_c , random_state=388345 )
        kmeans.fit( _ser , _wei )
        return kmeans

    # %%
    _dc = dscc[ co.CLUS_LENGTH_DIM ].to_dataframe()
    _dc[ co.KMEAN_OBJ ] = _dc.apply(
        lambda r : set_kmeans( r[ co.CLUS_LENGTH_DIM ] , _ser , _wei ) ,
        axis=1 )
    _dc.drop( co.CLUS_LENGTH_DIM , axis=1 , inplace=True )
    # %%
    dscc[ co.KMEAN_OBJ ] = _dc.to_xarray()[ co.KMEAN_OBJ ]
    # %%
    _kmeans = dscc[ co.KMEAN_OBJ ].to_series()
    # %%
    _dm = dscc[ co.CONC_NORMALIZED ].stack(
        { co.DUM_STACK : [ co.R_CENTER , co.TH_CENTER , co.ZM ] } ).T
    # _dm = _dm.isel(dum=slice(None,4))
    _nas = [ ]
    for i , ob in _kmeans.items() :
        _na = xr.full_like( _dm , np.nan ).sum( co.RL )
        _na.name = co.FLAG
        _na.values = ob.predict( _dm )
        _na = _na.expand_dims( **{ co.CLUS_LENGTH_DIM : [ i ] } ).unstack()
        _nas.append( _na )
    # %%
    _na = xr.concat( _nas , dim=co.CLUS_LENGTH_DIM )
    # %%
    # noinspection PyBroadException
    try :
        dscc = dscc.drop( co.FLAG )
    except :
        pass
    dscc = xr.merge( [ dscc , _na ] )
    return dscc


# noinspection PyShadowingNames
def plot_sample_of_vectors_norm_used_for_clustering( dscc ) :
    _col = co.CONC_NORMALIZED
    # noinspection PyShadowingNames
    _df = dscc.where( dscc[ co.LAB_CLUSTER_THRESHOLD ] )[ _col ].to_dataframe()[
        _col ].dropna()
    _df = _df.unstack( co.RL )
    # %%
    _sam = _df.sample( frac=.001 ).T.plot( legend=False , alpha=.7 ,
                                           figsize=(10 , 5) )


def plot_cells_used_for_clustering( dscc ) :
    _ds = dscc[ co.LAB_CLUSTER_THRESHOLD ].to_dataframe()[
        co.LAB_CLUSTER_THRESHOLD ].value_counts()
    _ds = 100 * _ds / _ds.sum()
    ax = _ds.plot.bar()
    ax.set_title( 'cells used for clustering' )


def preprocess_dscc_for_clustering( MAX_LENGTH , dscc ) :
    dscc = dscc.assign_coords(
        **{ co.CLUS_LENGTH_DIM : range( 2 , MAX_LENGTH ) } )
    # %%
    stack_dic = { co.DUM_STACK : [ co.R_CENTER , co.TH_CENTER , co.ZM ] }
    _norm = dscc[ co.CONC ].stack( **stack_dic )
    _norm_array , _norm_ret = preprocessing.normalize( _norm ,
                                                       return_norm=True ,
                                                       axis=0 )
    _norm.values = _norm_array
    dscc[ co.CONC_NORMALIZED ] = _norm.unstack()
    _normed = _norm.mean( co.RL )
    _normed.name = co.CONC_NORMS
    _normed.values = _norm_ret
    _normed = _normed.unstack()
    dscc[ co.CONC_NORMS ] = _normed
    # dscc[co.CONC_NORMS] = dscc[co.CONC_NORMS].where(dscc[
    # co.LAB_CLUSTER_THRESHOLD])
    # %%
    # noinspection PyBroadException
    try :
        dscc = dscc.drop( 'quantile' )
    except :
        pass
    return dscc


def print_percentage_res_time_mass_considered( dscc ) :
    # %%
    _res = (dscc[ co.CONC ].where( dscc[ co.LAB_CLUSTER_THRESHOLD ] )).sum() / \
           dscc[ co.CONC ].sum()
    # %%
    print( (100 * _res).item() )


def rebuild_the_dscc( dfcc ) :
    global _df
    _df = dfcc
    dscc = _df[ co.CONC ].stack().to_xarray()
    dscc.name = co.CONC
    dscc = dscc.to_dataset()
    CLUSTER_THRESHOLD = .4
    co.LAB_CLUSTER_THRESHOLD = 'LAB_CLUSTER_THRESHOLD'

    # %%
    dscc[ co.CSUM ] = dscc[ co.CONC ].sum( co.RL )
    # %%
    dscc[ co.LAB_CLUSTER_THRESHOLD ] = dscc[ co.CSUM ] > dscc[
        co.CSUM ].quantile(
        CLUSTER_THRESHOLD )
    return dscc


def plot_hist_all_values( dfcc ) :
    f , axs = plt.subplots( 1 , 2 , figsize=(10 , 5) )
    axs = axs.flatten()
    plot_hist_all_log( dfcc , ax=axs[ 0 ] )
    plot_hist_all_log( dfcc , cumulative=True , ax=axs[ 1 ] )
    f: plt.Figure
    f.tight_layout()


def get_df_for_plot( _n , dscc ) :
    _d = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ]
    _d = _d.drop( [ co.KMEAN_OBJ , co.CLUS_LENGTH_DIM ] )
    # _d = _d.where(_d[FLAG]==_f)
    # %%
    _s = _d[ [ co.CONC , co.FLAG ] ].to_dataframe()[ [ co.CONC , co.FLAG ] ]
    _ss = _s.groupby( [ co.RL , co.FLAG ] ).sum()
    # %%
    _ss1 = _ss.unstack( co.FLAG ).resample( '4H' ).mean()
    _ss1 = (100 * _ss1[ co.CONC ].T / _ss1.T.sum()).T
    # %%
    _ss1.plot( sharex=True , sharey=True , layout=(2 , -1) , subplots=True ,
               figsize=(10 , 5) , color=ucp.cc )
    # %%
    _ss1.plot.area( legend=False , figsize=(12 , 6) , color=ucp.cc )
    # %%
    # %%
    _ss1 = _ss.unstack( co.FLAG )
    # %%
    _ss1 = _ss1.resample( 'm' ).median()
    # %%
    _ss1 = (100 * _ss1[ co.CONC ].T / _ss1.T.sum()).T
    return _ss1


def add_lat_lon_to_dscc( dscc , selfFLP ) :
    lcols = [ *co.LL00 , 'LON' , 'LAT' ]
    _ds = selfFLP.merged_ds
    _ds = _ds[ lcols ]
    # noinspection PyBroadException
    try :
        dscc = dscc.drop( lcols )
    except :
        pass
    # noinspection PyBroadException
    try :
        dscc = xr.merge( [ dscc , _ds ] )
    except :
        pass
    # dscc = xr.merge([dscc,_ds])
    return dscc


# noinspection PyShadowingNames
def plot_hour_influence_targeted( _n , _nn , dscc , height_less_than ,
                                  less_than , more_than ) :
    _ds = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ]
    # noinspection PyBroadException
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
    _df3 = _df2.loc[ : , _nn ].copy()
    _df3.index = (_df3.index - pd.Timedelta( hours=4 )).hour
    ax = _df3.sort_index().reset_index().boxplot( by=co.RL )
    ax.set_ylim( -.01 , .5 )
    # ax.set_yscale('log')
    # ax.set_title('')


# noinspection PyShadowingNames
def plot_target_distance_height_influence( _n , dscc , height_less_than ,
                                           less_than , more_than ) :
    _ds = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ]
    # noinspection PyBroadException
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
    _df2.plot( subplots=True , figsize=(20 , 20) , sharey=True ,
               color=[ *ucp.cc , *ucp.cc ] )


# noinspection PyShadowingNames
def plot_influences( _n , dscc ) :
    _ds = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ]
    # noinspection PyBroadException
    try : _ds = _ds.drop( co.KMEAN_OBJ )
    except : pass
    _dss = _ds.copy()
    _ds[ co.CONC ] = _ds[ co.CONC ]
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
    _df2.plot( subplots=True , figsize=(20 , 20) , sharey=True ,
               color=[ *ucp.cc , *ucp.cc ] )


def plot_dis_height_quantiles_chc( _n , dsF , dscc , axs=False ) :
    for _f in range( _n ) :
        plot_dis_height_quantiles_chc_single( _f , _n , dsF , dscc , axs=axs )


def plot_dis_height_quantiles_chc_single( _f , _n , dsF , dscc , axs=None ) :
    if axs is None :
        _ , ax = plt.subplots()
    else :
        if type( axs ) == np.ndarray :
            ax = axs[ _f ]
        else :
            ax = axs

    _cm = fa.get_custom_cmap( [ *ucp.cc , *ucp.cc , *ucp.cc ][ _f ][ :3 ] )

    _ds = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ]

    _ds = _ds.drop( co.KMEAN_OBJ )

    _ds = _ds.sum( [ co.RL ] )

    _ds1 = xr.merge( [ _ds , dsF[ [ co.TOPO ] ] ] ).where(
        _ds[ co.FLAG ] == _f )
    _ds1 = _ds1.swap_dims( { co.R_CENTER : co.DIS } )

    _ds2 = _ds1 / dsF[ co.ZLM ]

    _ds3 = _ds2[ co.CONC ]
    zmin , zmax = _ds2[ co.ZM ].quantile( [ 0 , 1 ] )
    zz = np.arange( zmin , zmax , zmin )

    zl = zz[ 1 ] - zz[ 0 ]

    _ds4 = _ds3.interp( **{ co.ZM : zz } ) * zl

    ZREAL = 'ZREAL'
    _ds4[ ZREAL ] = _ds4 * 0 + _ds4[ co.ZM ] + (
            (_ds4[ co.TOPO ] / zl).round() * zl)

    _dims = set( _ds4.dims )

    _keep = _dims.union( { ZREAL } )

    # noinspection SpellCheckingInspection
    _coor = set( _ds4.coords )

    _drop = list( _coor - _keep )

    _ds5 = _ds4.drop( _drop ).to_dataframe()

    _ds6 = \
        _ds5.reset_index().groupby( [ ZREAL , co.DIS , co.TH_CENTER ] ).sum()[
            [ co.CONC ] ].to_xarray()

    _ds6.sum( co.TH_CENTER )[ co.CONC ].plot( xscale='log' , vmin=0 , ax=ax ,
                                              cmap=_cm )

    HEIGHT = 'HEIGHT'
    _ds1[ HEIGHT ] = (_ds1[ co.TOPO ] + _ds1[ co.ZM ])

    _dg = _ds1[ [ HEIGHT , co.CONC ] ].to_dataframe()[ [ HEIGHT , co.CONC ] ]
    _dg = _dg.groupby( co.DIS )

    _dh = (_ds1[ co.CONC ] * (_ds1[ co.TOPO ] + _ds1[ co.ZM ])).mean(
        [ co.TH_CENTER , co.ZM ] )
    _dh = _dh / (_ds1[ co.CONC ].mean( [ co.TH_CENTER , co.ZM ] ))

    ax.set_xlim( 10 , 2e3 )

    _dh = (_ds1[ co.CONC ] * (_ds1[ co.TOPO ])).mean( [ co.TH_CENTER , co.ZM ] )
    _dh = _dh / (_ds1[ co.CONC ].mean( [ co.TH_CENTER , co.ZM ] ))

    _dh.plot( x=co.DIS , color='k' , ax=ax )
    ax.set_xscale( 'log' )

    ax.set_xlim( 5 , 2e3 )
    ax.set_ylim( 0 , 1.5e4 )
    ax.set_title( str( _f ) )
    ax.set_xlabel( 'Radial distance from CHC [km]' )
    ax.set_ylabel( 'Height [masl]' )
    ax.grid( color='k' , alpha=.3 , linestyle='--' )
    ax.set_axisbelow( False )
    ax.set_facecolor( 'white' )
    ax: plt.Axes = ax
    ax.scatter( 5.2 , 5200 , color='red' )
    ax.text( 6 , 5200 , 'CHC' )


def add_dis_km_dscc( dscc ) :
    _km = dscc[ co.R_CENTER ] * 100
    _km.name = co.DIS
    dscc = dscc.assign_coords( **{ co.DIS : _km } )
    return dscc


def plot_distance_height_chc( _n , dscc ) :
    for _f in range( _n ) :
        # ax = fa.get_ax_bolivia()
        #     ax.set_title(str(_f))
        _ds = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ]
        _ds = _ds.drop( co.KMEAN_OBJ )
        _ds = _ds.where( _ds[ co.FLAG ] == _f )
        _ds = _ds.sum( [ co.RL , co.TH_CENTER ] )

        _ds = _ds[ [ co.CONC ] ]

        _cm = fa.get_custom_cmap( [ *ucp.cc , *ucp.cc , *ucp.cc ][ _f ][ :3 ] )

        _km = _ds[ co.R_CENTER ] * 100

        DIS = 'Distance [km]'
        _km.name = DIS

        _ds = _ds.assign_coords( **{ DIS : _km } )
        _ , ax = plt.subplots()
        _ds[ co.CONC ].plot( x=DIS , cmap=_cm , ax=ax )
        ax.set_xscale( 'log' )
        ax.set_yscale( 'log' )
        ax.set_xlim( 10 , 2e3 )
        ax.set_ylim( 25e1 , 2e4 )
        ax.set_title( str( _f ) )


def plot_clust_bolivia_individual( _n , dscc ) :
    for _f in range( _n ) :
        ax = fa.get_ax_bolivia()
        ax.set_title( str( _f ) )
        _ds = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ]
        _ds = _ds.drop( co.KMEAN_OBJ )
        _ds = _ds.where( _ds[ co.FLAG ] == _f )
        _ds = _ds.sum( [ co.RL , co.ZM ] )

        _ds = _ds[ [ co.CONC ] ]

        _cm = fa.get_custom_cmap( [ *ucp.cc , *ucp.cc , *ucp.cc ][ _f ][ :3 ] )

        fa.logpolar_plot( _ds , ax=ax , patch_args={ 'cmap' : _cm } ,
                          colorbar=False )


def plot_clust_in_lapaz( _n , dscc ) :
    for _f in range( _n ) :
        ax = fa.get_ax_lapaz()
        ax.set_title( str( _f ) )
        _ds = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ][
            { co.R_CENTER : slice( 1 , 23 ) } ]
        _ds = _ds.drop( co.KMEAN_OBJ )
        _ds = _ds.where( _ds[ co.FLAG ] == _f )
        _ds = _ds.sum( [ co.RL , co.ZM ] )

        _ds = _ds[ [ co.CONC ] ]

        _cm = fa.get_custom_cmap( [ *ucp.cc , *ucp.cc , *ucp.cc ][ _f ][ :3 ] )

        if _ds[ co.CONC ].max().item() != 0 :
            fa.logpolar_plot( _ds , ax=ax , patch_args={ 'cmap' : _cm } ,
                              colorbar=False )
        fa.add_chc_lpb( ax )


def plot_clust_in_bolivia( _n , dscc ) :
    ax = fa.get_ax_bolivia()
    _f = 2
    for _f in range( _n ) :
        _ds = dscc.loc[ { co.CLUS_LENGTH_DIM : _n } ]
        _ds = _ds.drop( co.KMEAN_OBJ )
        _ds = _ds.where( _ds[ co.FLAG ] == _f )
        _ds = _ds.sum( [ co.RL , co.ZM ] )

        _ds = _ds[ [ co.CONC ] ]

        _cm = fa.get_custom_cmap( ucp.cc[ _f ][ :3 ] )

        fa.logpolar_plot( _ds , ax=ax , patch_args={ 'cmap' : _cm } ,
                          colorbar=False )


def plot_log_custom( d_sum ,
                     v_max ,
                     v_min ,
                     map_fun=fa.get_ax_bolivia ) :
    ax = map_fun( fig_args={ 'figsize' : (10 , 8) } )
    p_args_ = {
        'norm' : mpl_colors.LogNorm( vmin=v_min , vmax=v_max )
        }
    fa.logpolar_plot( d_sum , ax=ax , perM=v_max , perm=v_min ,
                      quantile=False ,
                      patch_args=p_args_ ,
                      drop_zeros=False ,
                      )


def get_con_norm_r_with_mask_over_threshold(
        ds: xr.Dataset ,
        conc_label ,
        mask_threshold: float = .85 ,
        ) -> xr.DataArray :
    # da_conc: xr.DataArray = ds[ co.CONC ]
    # non_r_dims = [ co.RL , co.ZM , co.TH_CENTER ]
    # da_conc_sum_rad = da_conc.sum( non_r_dims )
    # conc_norm_r = 'conc_norm_r'
    # da_conc = da_conc.assign_coords( **{ conc_norm_r : da_conc_sum_rad } )
    # da_ = da_conc / da_conc[ conc_norm_r ]
    # da_.name = 'CONC_norm_r'
    # conc_sum = da_.sum( co.RL )
    # con_sum_rl = 'conc_sum_rl'
    # da_ = da_.assign_coords( **{ con_sum_rl : conc_sum } )
    # %%
    ds_sum = ds[ conc_label ].sum( [ co.RL ] )
    da_conc_df = ds_sum.reset_coords( drop=True ).to_dataframe()
    # %%
    da_conc_df_sorted = da_conc_df.sort_values( conc_label )
    conc_tot = da_conc_df_sorted.sum().iloc[ 0 ]
    rl_ = da_conc_df_sorted[ conc_label ]
    conc_cum_per = 'conc_cum_per'
    da_conc_df_sorted[ conc_cum_per ] = rl_.cumsum() / conc_tot
    per_bool_ = da_conc_df_sorted[ conc_cum_per ] > 1 - mask_threshold
    print(per_bool_.value_counts())
    above_thre = co.above_thre_label
    da_conc_df_sorted[ above_thre ] = per_bool_
    len_da = len( da_conc_df_sorted )
    i_per = 'i_per'
    da_conc_df_sorted[ i_per ] = np.linspace( 0 , 1 , len_da )
    va_co_ = da_conc_df_sorted[ above_thre ].value_counts()
    log.ger.warning( f'values counts are:\n{va_co_}' )
    # da_conc_df_sorted
    da_conc_df_sorted = da_conc_df_sorted.sort_index()
    da_above_thre_mask = da_conc_df_sorted[ above_thre ].to_xarray()
    # %%
    ds = ds.assign_coords( **{ above_thre : da_above_thre_mask } )
    return ds


def plot_conc_norm_r( da ) :
    f , ax = plt.subplots()
    f: plt.Figure
    ax: plt.Axes
    da.sum( [ co.RL , co.ZM ] ).plot( ax=ax )
    ax.set_yscale( 'log' )
    ax.set_title( da.name )
    plt.show()


def multi_smooth_plot( CONC_norm_r , df_ , ds ) :
    _ls = list( df_[ 'name_col' ] )
    ds_l: xr.Dataset = ds[ _ls ]
    ds_l = ds_l.sum( [ co.RL , co.ZM ] )
    da: xr.DataArray = ds_l.to_array( 'smooth' , name=CONC_norm_r )
    # %%
    da_plot = da.plot( col='smooth' , col_wrap=3 ,
                       figsize=(12 , 10) ,
                       add_colorbar=True , yscale='log'
                       )
    # f = plt.gcf()
    # plt.show()
    for a , l in zip( da_plot.axes.flat , da_plot.col_names ) :
        a.set_title( l[ -25 : ] )
    plt.show()


def print_mask_true_false( da_ ) :
    threshold__sum = da_.where( da_[ co.above_thre_label ] ).sum()
    log.ger.debug( f'vals true {threshold__sum}' )
    threshold__sum_false = da_.where( ~da_[ co.above_thre_label ] ).sum()
    log.ger.debug( f'vals false {threshold__sum_false}' )


def multi_smoothing(
        ds ,
        r_var=None ,
        th_var=None ,
        z_var=None ,
        t_var=None ,
        con_var='CONC_norm_r' ,
        truncate=4
        ) :
    if t_var is None :
        t_var = [ 3 ]
    if z_var is None :
        z_var = [ .5 ]
    if th_var is None :
        th_var = [ 0 , .5 , 1 ]
    if r_var is None :
        r_var = [ 0 , .5 , 1 , ]
    import itertools
    def _get_new_conc_smooth_name(
            * , smooth_pars_ , name='name' ,
            ) :
        string = f'{name}_smooth'
        smooth_pars_round = { k : int( 100 * v ) for k , v in
                              smooth_pars_.items() }
        for k , v in smooth_pars_round.items() :
            string = string + f'_{k}_{v}'
        return string

    var_ = (r_var , th_var , t_var , z_var)
    col_ = [ 'r' , 'th' , 't' , 'z' ]
    r_th_list = \
        list( itertools.product( *var_ ) )
    df_ = pd.DataFrame( r_th_list , columns=col_ )
    # df_[ 't' ] = 3
    # df_[ 'z' ] = .5
    df_[ 'dic' ] = df_.apply(
        lambda r_ : dict(
            t=r_[ 't' ] , z=r_[ 'z' ] ,
            r=r_[ 'r' ] , th=r_[ 'th' ]
            ) ,
        axis=1 )
    df_[ 'name_col' ] = df_.apply(
        lambda r_ : _get_new_conc_smooth_name(
            smooth_pars_=r_[ 'dic' ] , name=con_var
            ) ,
        axis=1
        )

    # noinspection PyShadowingNames
    def __fun( r_ , ds ) :
        res = FlexLogPol.smooth_col(
            ds[ con_var ] , **r_[ 'dic' ] , truncate=truncate
            )

        ds[ r_[ 'name_col' ] ] = res

    df_.apply( __fun , axis=1 , args=(ds ,) )
    return df_ , ds


def plot_sum_hist_df( _df1 ) :
    df__sum = _df1.sum( axis=1 )
    df__sum.plot.hist()
    plt.show()
    return df__sum


def plot_distplot_scaled_v2( _dft ) :
    f , ax1 = plt.subplots()
    ax1: plt.Axes
    for i in range( 0 , len( _dft ) , 10 ) :
        vals = _dft[ i ]
        # vals = np.log( vals )
        # vals = vals[vals>-16]
        ax1.plot( vals , alpha=.1 , color='k' )
    # ax.set_yscale('log')
    # ax.set_ylim(1e-3,None)
    ax1.set_xlim( 200 , 600 )
    plt.show()


def plot_distplot_scaled_vectors( _dft ) :
    f , ax1 = plt.subplots()
    ax1: plt.Axes
    for i in range( 0 , len( _dft ) , 10 ) :
        vals = _dft[ i ]
        # vals = np.log( vals )
        # vals = vals[vals>-16]
        sns.distplot( vals ,
                      # bins=np.linspace(0,.5e-4,40),
                      hist=False ,
                      kde=True ,
                      norm_hist=False ,
                      ax=ax1 )
    # ax.set_yscale('log')
    # ax.set_ylim(1e-3,None)
    ax1.set_xlim( -1 , 2 )
    plt.show()


def from_agl_to_asl(
        ds ,
        ds_var='conc_norm' ,
        delta_z=500 ,
        z_top=15000 ,
        ds_var_name_out=None
        ) :
    log.ger.warning(
        f'this will only work if ds z levels are constant' )
    import wrf
    t_list = [ co.ZM , co.R_CENTER , co.TH_CENTER ]
    d3d = ds[ ds_var ]  # .sum( [ co.RL ] )
    d3d_attrs = d3d.attrs
    d3d = d3d.transpose(
        co.RL , *t_list , transpose_coords=True
        )
    dz = d3d[ co.TOPO ] + np.round( d3d[ co.ZM ] / delta_z ) * delta_z
    d3d = d3d.reset_coords( drop=True )
    dz = dz.transpose( *t_list , transpose_coords=True )
    dz = dz.reset_coords( drop=True )
    # %%
    # print( d3d.shape )
    # print( dz.shape )
    # %%
    z_lev = np.arange( delta_z / 2 , z_top , delta_z )
    da_interp = wrf.interplevel( d3d , dz , z_lev )
    da_reinterp = da_interp.rename( level=co.ZM )

    # %%
    ds_chop = ds.isel( { co.ZM : slice( 0 , len( da_reinterp[ co.ZM ] ) ) } )
    for coord in list( ds.coords ) :
        da_reinterp = da_reinterp.assign_coords(
            **{ coord : ds_chop[ coord ] } )
    if ds_var_name_out is not None :
        da_reinterp.name = ds_var_name_out

    # we do this in order to avoid the problem of setting attributes
    # to none that cannot be saved using to netcdf.
    da_reinterp.attrs = d3d_attrs

    ds_reinterp = da_reinterp.to_dataset()
    # todo: check that concentrations are the same after resampling
    return ds_reinterp


def get_r_length( ds ) :
    r_c = ds[ co.R_CENTER ]
    mld = np.log( r_c ).diff( co.R_CENTER ).mean().item()
    """mean log distance"""
    lmin = np.log( r_c ) - mld / 2
    lmax = np.log( r_c ) + mld / 2
    r_length = np.exp( lmax ) - np.exp( lmin )
    return r_length


def plot_conc_over_distance( ds , conc_lab=co.CONC ,
                             ax_ops=None ,
                             ax: plt.Axes = None ) :
    if ax_ops is None :
        ax_ops = { }

    ax_was_none = False
    if ax is None :
        ax_was_none = True
        f , ax = plt.subplots()
    r_length = get_r_length( ds )
    R_LENGTH = 'R_LENGTH'
    ds = ds.assign_coords( **{ R_LENGTH : r_length } )
    sum_dims = [ co.RL , co.ZM , co.TH_CENTER ]
    conc__sum = ds[ conc_lab ].sum( sum_dims )
    sum_r = conc__sum / ds[ R_LENGTH ]
    (sum_r / sum_r.mean()).plot(
        label='sum conc / r_length [norm]' ,
        ax=ax
        )
    (conc__sum / conc__sum.mean()).plot(
        label='sum conc [norm]' ,
        ax=ax
        )
    # ax: plt.Axes = plt.gca()
    if ax_was_none :
        ax.legend()
        ax.set( **ax_ops )
        fig: plt.Figure = plt.gcf()
        fig.suptitle( conc_lab )
        plt.show()


def re_interpolate_merged_processed_ds_and_save( selfFLP ) :
    ds = selfFLP.merged_ds
    # %%
    ds_reinterp = \
        from_agl_to_asl( ds , ds_var=co.CONC , ds_var_name_out=co.CONC )
    # %%
    _ds = ds_reinterp.copy()
    # _ds[ co.CONC ] = _ds[ co.CONC ].where( ~(_ds[ co.CONC ].isnull()) , 0 )
    # %%
    name = 'ds_above_sea_level.nc'
    path = os.path.join( selfFLP.datasets_path , name )
    info = {
        'smoothed'        : 0 ,
        'above_sea_level' : 1 ,
        'z delta'         : 500 ,
        'z levels'        : 30 ,
        'orig_name'       : name ,
        }
    ds_reinterp = ds_reinterp.assign_attrs( **info )
    fa.compressed_netcdf_save( ds_reinterp , path=path )
    return ds


def clus_plot(
        i_lab , ds: xr.Dataset ,
        conc_lab=None ,
        ds_lab=None ,
        figure_size=15 ,
        dpi=400 ,
        fig_title: str = None,
        conc_lab_ts = None,
        df_prop = None
        ) :
    if conc_lab is None :
        conc_lab = ds.attrs[ 'chosen_smooth' ]
    if conc_lab_ts is None:
        conc_lab_ts = conc_lab

    r_dis_km: xr.DataArray = ds[ co.R_CENTER ] * 100
    r_dis_km = r_dis_km.assign_attrs( {
        'units'     : 'km' ,
        'long_name' : 'radial distance from CHC'
        } )
    # return r_dis_km
    ds = ds.assign_coords( **{ R_DIS_KM : r_dis_km } )

    if ds_lab is None :
        ds_lab = ds[[conc_lab_ts,conc_lab]].where( ds[ 'lab' ] == i_lab )
    ds_lab = ds_lab.assign_coords( **{ R_DIS_KM : r_dis_km } )
    # print(ds_lab.attrs)
    cols = 10
    rows = 10
    f_len = figure_size
    f: plt.Figure = plt.figure(
        figsize=(f_len , cols / rows * f_len) ,
        dpi=dpi
        )
    xn = 2
    yn = 4
    xp = .07
    yp = .05
    ww = (1-xp*3)/xn
    hh = (1-yp*5)/yn
    # yy = .29
    # xx = .4
    # xxL = .55
    # ypos = .35
    l_lpb       = ((2*xp)+ww, (2*yp)+hh    , .8*ww    , hh)
    l_bol       = ((2*xp)+ww, yp       , .8*ww    , hh)
    l_ts        = (xp , 1-yp-hh    , 1-2*xp     , hh)
    l_per_inf   = (xp , (3*yp) + (2*hh)      , ww    , hh)
    l_far       = (xp , yp       , 1.2*ww   , hh)
    l_zoom      = (xp , 2*yp + hh    , 1.2*ww   , hh)

    ax_vertical_far_:plt.Axes = f.add_axes( l_far )
    da_lab = ds_lab[conc_lab]
    da_lab.load()
    plot_vertical_ax( ax_vertical_far_ , conc_lab , ds , da_lab )
    ax_vertical_far_.scatter(0,5240,c='blue',label='CHC')
    ax_vertical_far_.legend()
    ax_vertical_far_.grid(True)
    ax_vertical_far_.set_axisbelow(False)

    ax_vertical_zoom = f.add_axes( l_zoom )
    plot_vertical_ax( ax_vertical_zoom , conc_lab , ds , da_lab ,
                      xlim=(0 , 200) )
    ax_vertical_zoom.scatter(0,5240,c='blue',label='CHC')
    ax_vertical_zoom.legend()
    ax_vertical_zoom.grid( True )
    ax_vertical_zoom.set_axisbelow(False)

    carree = crt.crs.PlateCarree()

    ax_lpb: cartopy.mpl.geoaxes.GeoAxesSubplot = \
        f.add_axes( l_lpb , projection=carree )

    cc_ = da_lab.sum( [ co.RL , co.ZM ] , keep_attrs=True )
    ax_lpb = fa.get_ax_lapaz( ax=ax_lpb )
    print(cc_.attrs)
    fa.logpolar_plot( cc_ , name=conc_lab , ax=ax_lpb )

    ax_bol = f.add_axes( l_bol , projection=carree )
    lo_la_bol_range = 15
    lo_la_limits = [
        co.CHC_LON - lo_la_bol_range ,
        co.CHC_LON + lo_la_bol_range ,
        co.CHC_LAT - lo_la_bol_range ,
        co.CHC_LAT + lo_la_bol_range ,
        ]
    ax_bol = fa.get_ax_bolivia( ax=ax_bol , lola_extent=lo_la_limits )

    fa.logpolar_plot( cc_ , name=conc_lab , ax=ax_bol )

    # noinspection PyUnusedLocal
    ax_ts = f.add_axes( l_ts )

    plot_lab_time_series( da_lab=ds_lab[conc_lab_ts] , ax_ts=ax_ts )

    ax_per_inf = f.add_axes( l_per_inf )
    if df_prop is not None:
        plot_cluster_summary_figure(
            df_prop,
            'SRR [%]',
            'distance from CHC [km]',
            # save_fig=True,
            fig_save_name='dis_vs_srr_influence.pdf',
            xy_locs=([-30, 5], [0, 9], [500, 11], [950, 9]),
            y_range=(0, 13),
            add_vertical_lines=True,
            add_cluster_group_label=False,
            ax=ax_per_inf
        )
        y = df_prop.set_index('cluster_i')['SRR [%]'][i_lab]
        x = df_prop.set_index('cluster_i')['distance from CHC [km]'][i_lab]
        # ax_per_inf.scatter(x,y,c='k',s=10,marker='o')
        ax_per_inf.scatter(x, y, s=200, marker='o', facecolors='none', edgecolors='k')

    #todo fix this
    else:
        plot_concentration_influence_div_by_cluster(
        ds=ds , conc_lab=conc_lab , i_lab=i_lab ,
        ax=ax_per_inf
        )

    plt.show()
    if fig_title is None :
        f.suptitle( f'cluster: {i_lab}' ,y=.95)
    else :
        f.suptitle( fig_title ,y=1)
    f.tight_layout()
    log.ger.debug('show plot')
    f.show()
    return f


def plot_vertical_ax( ax_vertical , conc_lab , ds , ds_lab ,
                      xlim=(0 , 2000)
                      ) :
    lab_sum_zm = ds_lab.sum( [ co.RL , co.TH_CENTER ] , keep_attrs=True )
    lab_sum_zm.plot(
        x=R_DIS_KM , y=co.ZM ,
        # xscale='log' ,
        ax=ax_vertical , ylim=(0 , 15e3) ,
        cmap=plt.get_cmap( 'Reds' )
        )
    lab_topo = ds_lab.sum( [ co.RL , co.ZM ] ) * ds_lab[ co.TOPO ]
    lab_topo_sum = lab_topo.sum( co.TH_CENTER )
    lab_sum_th = ds_lab.sum( [ co.TH_CENTER , co.RL , co.ZM ] )
    plot_threshold = lab_sum_th.max() * .05
    weighted_topo = lab_topo_sum / lab_sum_th
    w_topo_filtered = weighted_topo[ lab_sum_th > plot_threshold ]
    # print(w_topo_filtered)
    w_topo_filtered.plot( ax=ax_vertical , color='k' , x=R_DIS_KM )
    long_name = ds[ R_DIS_KM ].attrs[ 'long_name' ]
    units = ds[ R_DIS_KM ].attrs[ 'units' ]
    ax_vertical.set(
        xlabel=f'{long_name} [{units}]' ,
        ylabel='height above sea level [m]' ,
        xlim=xlim
        )


def plot_lab_time_series( da_lab , ax_ts: plt.Axes = None ) :
    if ax_ts is None :
        _ , ax_ts = plt.subplots()
    dim_complement = fa.get_dims_complement( da_lab , co.RL )
    ds_sum:xr.DataArray = da_lab.sum( dim_complement ,keep_attrs=True)
    ds_sum_rolling_mean = ds_sum.rolling( **{ co.RL : 24 * 30 } , min_periods=24 * 15 ,
                           center=True ).mean()
    ds_sum_rolling_mean.plot( ax=ax_ts , label = 'monthly running mean')
    ds_sum.plot( ax=ax_ts , label = 'hourly values')
    ax_ts.set( xlabel='arrival time' )
    ax_ts.legend()
    # return ds_sum


def plot_concentration_influence_div_by_cluster(
        ds: xr.Dataset , i_lab=None , conc_lab='CONC' ,
        ax: plt.Axes = None ,
        ) -> None :
    if ax is None :
        _ , ax = plt.subplots()
    ds_sum: xr.DataArray = ds[ conc_lab ].sum( co.RL , keep_attrs=True)
    ds_sum = ds_sum.assign_coords( **{ 'lab' : ds[ 'lab' ] } )
    ds_con_lab = ds_sum.reset_coords()[ [ conc_lab , 'lab' ] ]
    df = ds_con_lab.to_dataframe()
    df = df.reset_index( drop=True )

    df_sum = df.groupby( 'lab' ).sum()
    tot = df_sum.sum()
    mean = (df_sum.mean() / tot * 100).iloc[ 0 ]
    df_sum = df_sum / tot * 100
    # _ , ax = plt.subplots()
    _bool = df_sum.index == i_lab
    df_i = df_sum.copy()
    df_i[ ~_bool ] = 0
    df_i = df_i.rename( str , columns={ conc_lab : f'clus: {i_lab}' } )
    df_sum = df_sum.rename(str,columns={conc_lab:'all clusters'})
    df_sum.plot.bar( color='k' , ax=ax )
    df_i.plot.bar( ax=ax )
    ax: plt.Axes
    ax.axhline(
        mean , color='k' , alpha=.5 , linestyle='-.' ,
        label='mean'
        )
    import xarray.plot.utils
    ax.set(
        xlabel='cluster label' ,
        ylabel= xarray.plot.utils.label_from_attrs(ds_sum)
        )
    ax.legend()
    # return mean


def add_total_per_row( ds , conc_lab , new_lab ,
                       long_name = "source receptor relationships (SRR)" ,
                       ) :
    da = ds[ conc_lab ]
    da_tot = da.sum()
    da_per = da / da_tot * 100
    da_per.name = new_lab
    attr_dict = {
        'long_name' : long_name ,
        'total'     : da_tot.load().item() ,
        'units'     : '% of total'
        }
    da_per = da_per.assign_attrs( attr_dict )
    ds[ new_lab ] = da_per


def add_time_per_row( ds , conc_lab , new_lab ,
                      long_name = "source receptor relationships (SRR)",
                      ) :

    da = ds[ conc_lab ]
    da_tot = da.sum(fa.get_dims_complement(da,co.RL))
    da_per = da / da_tot * 100
    # return da_tot
    da_per.name = new_lab
    attr_dict = {
        'long_name' : long_name ,
        # 'total'     : da_tot.item() ,
        'units'     : '% over time step'
        }
    da_per = da_per.assign_attrs( attr_dict )
    ds[ new_lab ] = da_per


def plot_cluster_summary_figure(
        df_prop, y_var, x_var,
        xy_locs=([150, .5], [0, 4], [400, 6], [950, 5]),
        range_name='range',
        figsize=(4, 3),
        y_range=None,
        save_fig=False,
        fig_save_name='dis_vs_hag.pdf',
        fig_save_dir='/Users/diego/flexpart_management/flexpart_management/victoria_trento/figures/',
        ax=None,
        y_label=None,
        add_vertical_lines=False,
        add_cluster_group_label = True,
        y_ticks = None
):
    if ax is None:
        f, ax = plt.subplots(figsize=figsize)
    else:
        ax = ax
        f = ax.figure
    ax: plt.Axes
    xl = x_var
    yl = y_var
    # number_marker_plot( df_prop , xl , yl , ax )
    # df_prop.plot.scatter(x=xl,y=yl, ax=ax)
    # sns.scatterplot(x=xl,y=yl,data=df_prop,style=range_name, hue=range_name)
    # add_zoom_plot(ax, df_prop, xl, yl)
    ranges = ['SR', 'SM', 'MR', 'LR']
    shapes = ['o', 's', '^', 'D']
    texts = ['short\nrange', 'short-medium\nrange',
             'medium\nrange', 'long\nrange']
    xys = xy_locs
    i_range = range(4)
    for i, r, s, t, xy in zip(i_range, ranges, shapes, texts, xys):
        _df: pd.DataFrame = df_prop[df_prop[range_name] == r]

        if add_vertical_lines:
            ax.vlines(_df[xl],ymin=0,ymax=_df[yl],colors=[ucp.cc[i]], alpha=.3)

        _df.plot.scatter(
            x=xl, y=yl, ax=ax, marker=s, c=[ucp.cc[i]],
            edgecolor='w', s=30, linewidths=.2
        )
        if add_cluster_group_label:
            ax.annotate(
                t, xy, xycoords='data', c=ucp.cc[i])


    ax.grid(False)
    if y_range is not None:
        ax.set_ylim(y_range)
    if y_label is not None:
        ax.set_ylabel(y_label)

    if y_ticks is not None:
        ax.set_yticks(y_ticks)

    plt.tight_layout()
    f: plt.Figure

    fig_dir = fig_save_dir
    # plt.show()
    if save_fig:
        f.savefig(os.path.join(fig_dir, fig_save_name))
    return ax