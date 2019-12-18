'''functions used when analyzing flexpart output
Examples:
    >>> euristic_import_flexpart(dir_path='path_to_dir', dd=D2)
'''

# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import netCDF4

import matplotlib
import numpy
import xarray
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap , LinearSegmentedColormap
from matplotlib.patches import Polygon
from useful_scit.imps import *
from typing import List
import cartopy
import cartopy.mpl.geoaxes
import area
import flexpart_management.modules.constants as co
from useful_scit.util.zarray import compressed_netcdf_save

from flexpart_management.modules import constants as co


def import_flex_file( path_file: str ) :
    ds = xr.open_dataset( path_file )
    return ds


def import_flex_head_file( path_file: str ) :
    ds = xr.open_dataset( path_file )
    return ds


def get_head_file_from_path( path: str , dom: str = 'd01' ) :
    pat = os.path.join( path , 'head*' + dom + '*' )
    file_list = glob.glob( pat )
    file = file_list[ 0 ]
    return file


def import_head_ds( path: str , dom: str ) -> xr.Dataset :
    file_path = get_head_file_from_path( path , dom )
    # print(file_path)
    head_ds = import_flex_head_file( file_path )
    return head_ds


def convert_ds_time_format( ds: xr.Dataset , var='Times' ) -> xr.Dataset :
    time_str_sr: pd.Series = ds[ [ var ] ].to_dataframe()[ var ].str.decode(
        'UTF8' )
    ts = pd.to_datetime( time_str_sr , format='%Y%m%d_%H%M%S' )
    # n_ds = ds.copy()
    n_ds = ds
    n_ds[ var ] = ts
    n_ds = n_ds.assign_coords( Time=n_ds.Times )
    n_ds = n_ds.drop( 'Times' )
    return n_ds


def import_file_ds_list( file_path: str , dom: str ) -> List[ xr.Dataset ] :
    file_list = get_flx_ds_list( dom , file_path )
    ds_list = create_ds_list_from_files_list( file_list )
    return ds_list


def get_flx_ds_list( dom , file_path ) :
    pat = os.path.join( file_path , 'flxout*' + dom + '*' )
    file_list = glob.glob( pat )
    file_list.sort()
    return file_list


def create_ds_list_from_files_list( file_list ) -> List[ xr.Dataset ] :
    ds_list = [ ]
    for f in file_list :
        try :
            ds = import_flex_file( f )
            ds = convert_ds_time_format( ds )
            ds_list.append( ds )
        except :
            log.ger.error( 'error when opening: %s' , f )
    return ds_list


def trim_flx_ds_list( file_list ) -> List[ str ] :
    '''
    cheks if the files in the list can be opened and return a list with only
    openable files
    :param file_list: List[str]
    :return: List[str]
    '''
    new_list = [ ]
    for f in file_list :
        try :
            log.ger.debug( 'opening:%s' , f )
            with netCDF4.Dataset( f , 'r' ) as ds :
                ds.file_format
                ds.dimensions.keys()
                # ds.close()
                # del ds
            # ds = convert_ds_time_format(ds)
            new_list.append( f )
        except :
            log.ger.error( 'error when opening: %s' , f )
    return new_list


def concat_file_ds_list( ds_list: List[ xr.Dataset ] ) :
    ds_con = xr.concat( ds_list , dim=co.TIME )
    return ds_con


# we might not need this function anymore
def decode_bstr( bstr: bytes ) :
    return bstr.decode( 'UTF8' )


# we might not need this function anymore
def flx_time_to_ts( bstr: bytes ) :
    flx_time_str = decode_bstr( bstr )
    ts = pd.to_datetime( flx_time_str , format='%Y%m%d_%H%M%S' )
    return ts


def join_head( ds_flx: xr.Dataset ,
               ds_head: xr.Dataset ,
               ageclass=slice( 0 , None ) ,
               releases=slice( 0 , None )
               ) -> xr.Dataset :
    new_ds = ds_flx.copy()
    vars2keep = [ co.TOPO , co.GRIDAREA , co.ZT ]
    for v in vars2keep :
        new_ds[ v ] = ds_head[ v ]
    new_ds = new_ds.isel( ageclass=ageclass , releases=releases )
    new_ds = new_ds.assign_attrs( ds_head.attrs )
    release_start_times = get_releases_start_time( ds_head )
    new_ds = new_ds.assign_coords( **{ co.RL : release_start_times } )

    return new_ds


def get_release_start_date( ds_head: xr.Dataset ) :
    # todo: warning this only works if there is 1 release
    log.ger.warning( 'this only works if the is 1 release' )
    sim_start_date = ds_head.SIMULATION_START_DATE
    sim_start_time = ds_head.SIMULATION_START_TIME
    start_datetime_str = '{0:08d}_{1:06d}'.format( sim_start_date ,
                                                   sim_start_time )
    start_datetime = pd.to_datetime( start_datetime_str ,
                                     format='%Y%m%d_%H%M%S' )
    release_sec = round(
        int( ds_head.ReleaseTstart_end.isel( releases=0 )[ 0 ] ) , -1 )
    release_start_date = start_datetime + pd.Timedelta( release_sec , unit='S' )
    return release_start_date


def get_releases_start_time( ds_head: xr.Dataset ) -> pd.DatetimeIndex :
    sim_start_dt = '{:08d}'.format( ds_head.SIMULATION_START_DATE ) + ' ' + \
                   '{0:06d}'.format( ds_head.SIMULATION_START_TIME )
    sim_start_dt = dt.datetime.strptime( sim_start_dt , '%Y%m%d %H%M%S' )
    start_deltas = ds_head.ReleaseTstart_end.values[ : , 0 ].round( -1 )

    rel_start = [ sim_start_dt + dt.timedelta( seconds=float( s ) ) for s in
                  start_deltas ]
    start_times = pd.to_datetime( rel_start )

    return start_times


def add_release_time_dim( ds_join , ds_head ) :
    ds_new = ds_join.copy()
    vars_to_add_dim = [ 'CONC' ]
    dim_name = 'arrival_time'
    for v in vars_to_add_dim :
        dd = ds_new[ v ]
        dd = xr.concat( [ dd ] , dim_name )
        ds_new[ v ] = dd
    ts = get_release_start_date( ds_head )
    ds_new = ds_new.assign_coords( release_time=[ ts ] )
    return ds_new


def assign_vars_to_cords( ds_join ) :
    new_ds = ds_join.copy()
    vars_to_assign = [ 'ZTOP' , 'GRIDAREA' , 'TOPOGRAPHY' ]
    for v in vars_to_assign :
        new_ds = new_ds.assign_coords( **{ v : new_ds[ v ] } )
    return new_ds


def add_lat_lot( ds: xr.Dataset ) :
    ds_new = ds.copy()
    lat = ds_new.XLAT.mean( dim='west_east' )
    lon = ds_new.XLONG.mean( dim='south_north' )
    ds_new = ds_new.assign_coords( **{ co.LAT : lat , co.LON : lon } )
    return ds_new


def add_zmid( ds: xr.Dataset ) :
    '''
    add z mid to the input dataset
    :param ds: input dataset
    :return: the dataset with zmid parameter
    '''
    zl = list( ds.ZTOP.values )
    zl.reverse()
    zl.append( 0 )
    zl.reverse()
    zm = [ ]
    for i in range( len( zl ) - 1 ) :
        zm.append( (zl[ i ] + zl[ i + 1 ]) / 2 )
    zmid: xr.DataArray = ds.ZTOP.copy()
    zmid.values = zm
    zname = 'ZMID'
    zmid.name = zname
    zmid = zmid.assign_attrs( description='MIDDLE OF MODEL LAYER' )
    new_ds = ds.assign_coords( **{ zname : zmid } )
    return new_ds


def add_zbot( ds: xr.Dataset ) :
    '''
    add z bottom to the input dataset
    :param ds: input dataset
    :return: the dataset with zbottom parameter
    '''
    zl = list( ds[ co.ZT ].values )
    zl.reverse()
    zl.append( 0 )
    zl.reverse()
    zm = [ ]
    for i in range( len( zl ) - 1 ) :
        zm.append( (zl[ i ]) )
    zmid = ds.ZTOP.copy()
    zmid.values = zm
    zname = co.ZB
    zmid.name = zname
    new_ds = ds.assign_coords( **{ zname : zmid } )
    return new_ds


def add_zlength_m( ds: xr.Dataset ) :
    '''
    add z length (m) to the input dataset.
    needs to be run after add_zbot and add_zmid
    :param ds: input dataset
    :return: the dataset with zlength (m) parameter
    '''
    zl = list( ds[ co.ZT ].values )
    zl.reverse()
    zl.append( 0 )
    zl.reverse()
    zm = [ ]
    for i in range( len( zl ) - 1 ) :
        zm.append( (-zl[ i ] + zl[ i + 1 ]) )
    zmid = ds.ZTOP.copy()
    zmid.values = zm
    zname = co.ZLM
    zmid.name = zname
    new_ds = ds.assign_coords( **{ zname : zmid } )
    return new_ds


def add_volume( ds: xr.Dataset ) :
    '''
    add volume to the input dataset
    :param ds: input dataset
    :return: the dataset with volume parameter
    '''
    new_ds = ds.copy()
    new_ds[ co.VOL ] = new_ds[ co.GA ] * new_ds[ co.ZM ]
    new_ds = new_ds.assign_coords( **{ co.VOL : new_ds[ co.VOL ] } )
    return new_ds


def add_alt_m( ds: xr.Dataset ) -> xr.Dataset :
    new_ds = ds.copy()
    new_ds[ co.ALT ] = new_ds[ co.TOPO ] + new_ds[ co.ZM ]
    new_ds = new_ds.assign_coords( **{ co.ALT : new_ds[ co.ALT ] } )
    return new_ds


def get_concat_array_values( file_ds_list: list , pnt=False ) -> co.np.ndarray :
    f1 = file_ds_list[ 0 ]
    llen = len( file_ds_list )
    vals = np.zeros( (llen , *(f1.CONC.shape[ 1 : ])) , dtype=float )
    for i in range( llen ) :
        if pnt : print( i )
        ds = file_ds_list[ i ]
        v = ds[ 'CONC' ][ 0 ].values
        vals[ i ] = v
    return vals


def create_concat_ds( file_ds_list , vals ) :
    dims = list( file_ds_list[ 0 ].dims.mapping.mapping.keys() )
    time_dim = [ ds[ co.TIME ] for ds in file_ds_list ]
    time_dim = xr.concat( time_dim , dim=co.TIME )
    ds = xr.Dataset( {
        'CONC' : (
            dims ,
            vals
            )
        } )

    ds = ds.assign_coords( **{ co.TIME : time_dim } )
    return ds


def ds_swap_dims( ds ) :
    ds2 = ds
    ds2 = ds2.swap_dims( { co.SN : co.LAT } )
    ds2 = ds2.swap_dims( { co.WE : co.LON } )
    ds2 = ds2.swap_dims( { co.BT : co.ZM } )
    return ds2


def ds_add_ll_dis( ds ) :
    ds2 = ds
    la_dis = (ds2[ co.LAT ] - co.CHC_LAT)
    lo_dis = (ds2[ co.LON ] - co.CHC_LON)

    ll_dis = np.sqrt( la_dis ** 2 + lo_dis ** 2 )
    ds2[ co.LL_DIS ] = ll_dis
    return ds2


def fix_releases( ds , prnt=False ) :
    # todo: not clear what this function does
    ds2 = ds
    hours = 96
    rr = range( hours , -1 , -1 )
    dsn = ds2.isel( **{ co.TIME : slice( None , hours + 1 ) } ).copy()
    dsn = dsn.assign_coords( Time=rr )

    actual_time = dsn[ co.CONC ].isel(
        **{ co.LAT : 0 , co.LON : 0 , co.ZM : 0 } ).copy()
    vals = actual_time.values
    actual_time.values = np.full_like( vals , np.NaN , dtype=np.datetime64 )
    # ACTUAL_TIME = 'ACTUAL_TIME'
    actual_time.name = co.ACTUAL_TIME

    dsn[ co.ACTUAL_TIME ] = actual_time
    for i in range( len( ds2[ co.RL ] ) ) :
        if prnt : print( i )
        ds1 = ds2.isel( **{ co.RL : i } )
        rt = ds1[ co.RL ].values

        rend = rt - pd.Timedelta( hours , 'hours' )

        ds1 = ds1.sel( **{ co.TIME : slice( rend , rt ) } )

        old_times = ds1.Time.copy()

        old_times.name = co.ACTUAL_TIME

        ds1.Time.values = rr
        ds1[ co.ACTUAL_TIME ] = old_times
        ds1[ co.ACTUAL_TIME ].Time.values = rr

        for v in list( ds1.data_vars ) :
            if co.RL in dsn[ v ].dims :
                dsn[ v ][ { co.RL : i } ] = ds1[ v ]
    return dsn


def add_chc_lpb( ax ) :
    ax.scatter( co.CHC_LON , co.CHC_LAT , marker='.' , color='b' ,
                transform=co.PROJ , label = 'CHC')
    ax.scatter( co.LPB_LON , co.LPB_LAT , marker='.' , color='g' ,
                transform=co.PROJ , label = 'La Paz')
    ax.legend()


GeoAxes = cartopy.mpl.geoaxes.GeoAxes


def get_ax_bolivia(
        ax: GeoAxes = False ,
        fig_args:dict=None ,
        lola_extent: List[ float ] = co.LOLA_BOL
        , proj=co.PROJ) -> GeoAxes :
    """
    returns a geo ax object with the area of bolivia

    Parameters
    ----------
    proj
        projection to use
    ax
        ax to use. if false create a new one
    fig_args
        args passed to the figure
    lola_extent
        extent of the lalo

    Returns
    -------
    cartopy.mpl.geoaxes.GeoAxes
        returns a cartopy geoax
        #todo check this

    """
    if fig_args is None :
        fig_args = { }
    import matplotlib.ticker as m_ticker
    fig_ops = dict( figsize=(15 , 10) )
    fig_ops = { **fig_ops , **fig_args }
    if ax is False :
        fig = plt.figure( **fig_ops )
        ax = fig.add_subplot( 1 , 1 , 1 , projection=proj , )

    ax.set_extent( lola_extent , crs=proj )
    ax.add_feature( cartopy.feature.COASTLINE.with_scale( '10m' ) )
    ax.add_feature( cartopy.feature.BORDERS.with_scale( '10m' ) )
    ax.add_feature(
        cartopy.feature.LAKES.with_scale( '10m' ) , alpha=1 , linestyle='-' )
    ax.add_feature( cartopy.feature.STATES.with_scale( '10m' ) , alpha=0.5 ,
                    linestyle=':' )
    gl = ax.gridlines( crs=proj , alpha=0.5 , linestyle='--' ,
                       draw_labels=True )
    gl.xlabels_top = False
    gl.ylabels_right = False
    lo1 = np.round(lola_extent[0]/5)*5 - 5
    print(lo1)
    lo2 = lola_extent[1] + 5
    la1 = np.round(lola_extent[2]/5)*5 - 5
    la2 = lola_extent[3] + 5
    gl.xlocator = m_ticker.FixedLocator( np.arange( *(lo1 , lo2 , 5 ) ) )
    gl.ylocator = m_ticker.FixedLocator( np.arange( *(la1 , la2 , 5) ) )

    add_chc_lpb( ax )

    # ax.set_xlabel('Longitude')
    # ax.set_ylabel('Latitude')

    return ax


def get_ax_lapaz( ax=False ,
                  fig_args=None ,
                  lalo_extent=co.LOLA_LAPAZ ) :
    if fig_args is None :
        fig_args = { }
    import matplotlib.ticker as mticker
    fig_ops = dict( figsize=(15 , 10) )
    fig_ops = { **fig_ops , **fig_args }
    if ax is False :
        fig = plt.figure( **fig_ops )
        ax = fig.add_subplot( 1 , 1 , 1 , projection=co.PROJ , )

    ax.set_extent( lalo_extent , crs=co.PROJ )
    ax.add_feature( cartopy.feature.COASTLINE.with_scale( '10m' ) )
    ax.add_feature( cartopy.feature.BORDERS.with_scale( '10m' ) )
    ax.add_feature(
        cartopy.feature.LAKES.with_scale( '10m' ) ,
        facecolor='none' , edgecolor='b'
        )
    ax.add_feature( cartopy.feature.STATES.with_scale( '10m' ) , alpha=0.5 ,
                    linestyle=':' )
    gl = ax.gridlines( crs=co.PROJ , alpha=0.5 , linestyle='--' ,
                       draw_labels=True )

    gl.xlabels_top = False
    gl.ylabels_right = False

    add_chc_lpb( ax )
    # ax.set_xlabel('Longitude')
    # ax.set_ylabel('Latitude')
    # ax:plt.Axes
    # ax.text(-.1,-)

    return ax


def red_cmap() :
    cmap = plt.get_cmap( 'Reds' )
    my_cmap = cmap( np.arange( cmap.N ) )

    # Set alpha
    my_cmap[ : , -1 ] = np.linspace( .3 , 1 , cmap.N )

    my_cmap = ListedColormap( my_cmap )

    return my_cmap


def get_r_dis( ds , lat_center=co.CHC_LAT , lon_center=co.CHC_LON ) :
    la = ds[ co.LAT ] - lat_center
    lo = ds[ co.LON ] - lon_center
    r = np.sqrt( la ** 2 + lo ** 2 )
    return r


def get_th_ang( ds , lat_center=co.CHC_LAT , lon_center=co.CHC_LON ) :
    th = np.arctan2( ds[ co.LAT ] - lat_center ,
                     ds[ co.LON ] - lon_center )
    th = np.mod( -th + np.pi / 2 , 2 * np.pi )

    return th


def data_array_to_logpolar( da: xr.DataArray ,
                            r_round_log: float ,
                            th_round_rad: float ,
                            lat_center: float = co.CHC_LAT ,
                            lon_center: float = co.CHC_LON ,
                            dim2keep: List[str] = None ,
                            fun: str = 'sum'
                            ) -> xr.DataArray :
    """
    converts a data array to log polar coordinates

    Parameters
    ----------
    da
        dataset in rectangular coords
    r_round_log
        value to round in log
    th_round_rad
        value to round in radian units
    lat_center
        lat center of the arrival point
    lon_center
        lon center of the arrival point
    dim2keep
        dimensions that should be kept
    fun
        function to join the cells

    Returns
    -------
    DataArray
        the data array in log pol coords
    """
    if dim2keep is None :
        dim2keep = [ ]
    da_array_copy = da.copy()
    da_array_copy[ co.LL_DIS ] = get_r_dis( da_array_copy , lat_center ,
                                            lon_center )

    da_array_copy[ co.LL_ANG ] = get_th_ang( da_array_copy , lat_center ,
                                             lon_center )

    r_log_round_center = (np.round(
        np.log( da_array_copy[ co.LL_DIS ] ) / r_round_log
        ) * r_round_log)

    da_array_copy[ co.R_CENTER ] = np.e ** r_log_round_center
    # da_array_copy[R_FAR] = np.e ** (r_log_round_center + r_round_log/2)
    # da_array_copy[R_CLOSE] = np.e ** (r_log_round_center - r_round_log/2)

    th_round_center = np.floor(
        da_array_copy[ co.LL_ANG ] / th_round_rad ) * th_round_rad
    th_round_center = th_round_center + th_round_rad / 2
    da_array_copy[ co.TH_CENTER ] = th_round_center

    name = da.name

    df: pd.DataFrame = da_array_copy.to_dataframe().reset_index()

    log.ger.debug( df.columns )

    df = df[ [ co.R_CENTER , co.TH_CENTER , name , *dim2keep ] ]

    df: pd.DataFrame = getattr(
        df.groupby( [ co.R_CENTER , co.TH_CENTER , *dim2keep ] ) ,
        fun
        )()

    r_th_da = df.to_xarray()[ name ]

    r_th_da[ co.LAT ] = r_th_to_lat( lat_center , r_th_da[ co.R_CENTER ] ,
                                     r_th_da[ co.TH_CENTER ] )

    r_th_da[ co.LON ] = r_th_to_lat( lon_center , r_th_da[ co.R_CENTER ] ,
                                     r_th_da[ co.TH_CENTER ] )

    r_log = np.log( r_th_da[ co.R_CENTER ] )

    th_cen = r_th_da[ co.TH_CENTER ]

    rM = np.e ** (r_log + r_round_log / 2)
    rm = np.e ** (r_log - r_round_log / 2)

    thM = th_cen + th_round_rad / 2
    thm = th_cen - th_round_rad / 2

    val_list = [
        [ co.LAT_00 , co.LON_00 , rm , thm ] ,
        [ co.LAT_10 , co.LON_10 , rM , thm ] ,
        [ co.LAT_11 , co.LON_11 , rM , thM ] ,
        [ co.LAT_01 , co.LON_01 , rm , thM ] ,
        ]

    for v in val_list :
        r_th_da[ v[ 0 ] ] = r_th_to_lat( lat_center , v[ 2 ] , v[ 3 ] )
        r_th_da[ v[ 1 ] ] = r_th_to_lon( lon_center , v[ 2 ] , v[ 3 ] )

    r_th_da = r_th_da.where( ~r_th_da.isnull() , 0 )
    r_th_da[ co.GA ] = get_pol_area( r_th_da )

    return r_th_da


def r_th_to_ll( center , rr , th , fun ) :
    res = rr * fun(
        th
        ) + center
    return res


def r_th_to_lon( lon_center , rr , th ) :
    return r_th_to_ll( lon_center , rr , th , np.sin )


def r_th_to_lat( lat_center , rr , th ) :
    return r_th_to_ll( lat_center , rr , th , np.cos )


def polygon_from_row( r ) :
    pol = Polygon( [
        [ r[ co.LON_00 ] , r[ co.LAT_00 ] ] ,
        [ r[ co.LON_10 ] , r[ co.LAT_10 ] ] ,
        [ r[ co.LON_11 ] , r[ co.LAT_11 ] ] ,
        [ r[ co.LON_01 ] , r[ co.LAT_01 ] ] ,
        ] , True )
    return pol


def logpolar_plot( ds ,
                   ax=None ,
                   name='CONC' ,
                   perM=.95 ,
                   perm=0.0 ,
                   colorbar=True ,
                   patch_args=None ,
                   quantile=True ,
                   fig_ops=None ,
                   drop_zeros=True ,
                   cb_kwargs=None ,
                   ) -> plt.Axes :
    """
    plots a log polar plot from a dataset that contains the following fields:
    ___.

    Parameters
    ----------
    cb_kwargs
        kwargs for the colorbar
    ds
        dataset to get the information from
    ax
        GeoAxes to plot
    name
        name of the variable to plot
    perM
        quantile max for the colorbar
    perm
        quantile min for the colorbar
    colorbar
        weatherr the colorbar should be added
    patch_args
    quantile
        weather quantiles should be used for the colorbar limits
    fig_ops
        options to be passed to the figure creation
    drop_zeros
        either to drop zero values

    Returns
    -------
    an axes where the plot is drawn
    """

    if cb_kwargs is None :
        cb_kwargs = { }
    if fig_ops is None :
        fig_ops = { }
    if patch_args is None :
        patch_args = { }

    if ax is None :
        fig = plt.figure( **fig_ops )
        ax = fig.add_subplot( 1 , 1 , 1 , projection=co.PROJ , )
    df = ds.to_dataframe()
    if drop_zeros :
        df = df[ df[ name ] > 0 ]
    pol_key = 'pol'
    df[ pol_key ] = df.apply( lambda r : polygon_from_row( r ) , axis=1 )
    df = df.dropna()

    if quantile :
        maxc = df[ name ].quantile( perM )
        minc = df[ name ].quantile( perm )
    else :
        maxc = perM
        minc = perm

    args_ = {
        'cmap'      : red_cmap() ,
        'transform' : co.PROJ ,
        **patch_args
        }

    p = PatchCollection( df[ pol_key ].values , **args_ )
    p.set_array( df[ name ].values )
    p.set_clim( minc , maxc )
    ax.add_collection( p )
    fig = ax.figure
    if colorbar :
        cb = fig.colorbar( p , **cb_kwargs )
        if name in co.PLOT_LABS:
            cb_lab = co.PLOT_LABS[ name ]
        else:
            import xarray.plot.utils
            cb_lab = xarray.plot.utils.label_from_attrs(ds)
        cb.ax.set_ylabel( cb_lab , rotation=90 )
    return ax


def get_pol_area( ds ) :
    df = ds.reset_coords()[ co.LL00 ].copy().to_dataframe()
    df[ co.GA ] = df.apply( lambda r : get_area_from_row( r ) , axis=1 )
    nds = df[ co.GA ].to_xarray()

    return nds


def get_area_from_row( r ) :
    coords = [
        [ r[ co.LON_00 ] , r[ co.LAT_00 ] ] ,
        [ r[ co.LON_10 ] , r[ co.LAT_10 ] ] ,
        [ r[ co.LON_11 ] , r[ co.LAT_11 ] ] ,
        [ r[ co.LON_01 ] , r[ co.LAT_01 ] ] ,
        [ r[ co.LON_00 ] , r[ co.LAT_00 ] ] , ]
    obj = { 'type' : 'Polygon' , 'coordinates' : [ coords ] }
    ar = area.area( obj )
    return ar


def trim_swap_dim_coord( nds: xr.Dataset , hours: int ) :
    rel_time = nds[ co.RL ].values
    # hours = 96
    rel_time_end = rel_time - pd.Timedelta( hours=hours )

    nds1 = nds.sel( **{ co.TIME : slice( rel_time_end , rel_time ) } )

    # TH = 'Time_h'

    lt = len( nds1[ co.TIME ] )
    tr = [ i for i in range( -lt + 1 , 1 , 1 ) ]

    time_h = nds1[ co.TIME ].copy()

    time_h.values = tr

    nds1[ co.TH ] = time_h

    nds2 = nds1.swap_dims( { co.TIME : co.TH } )
    nds2 = nds2.reset_coords( co.TIME )

    return nds2


def get_dims_complement( ds , keep ) :
    coords = set( list( ds.dims ) )
    if type( keep ) is list :
        co_keep = set( keep )
    elif type( keep ) is str :
        co_keep = set( [ keep ] )
    else :
        print( 'invalid keep' )

    complement = list( coords - co_keep )
    return complement
    # return co_keep


def get_custom_cmap( to_rgb , from_rgb=None ) :
    # from color r,g,b
    if from_rgb is None :
        from_rgb = [ 1 , 1 , 1 ]
    r1 , g1 , b1 = from_rgb

    # to color r,g,b
    r2 , g2 , b2 = to_rgb

    cdict = {
        'red'   : ((0 , r1 , r1) ,
                   (1 , r2 , r2)) ,
        'green' : ((0 , g1 , g1) ,
                   (1 , g2 , g2)) ,
        'blue'  : ((0 , b1 , b1) ,
                   (1 , b2 , b2))
        }

    cmap = LinearSegmentedColormap( 'custom_cmap' , cdict )
    return cmap


def plot_lapaz_rect( ax ) :
    bl = co.LOLA_LAPAZ[ 0 ] , co.LOLA_LAPAZ[ 2 ]
    w = co.LOLA_LAPAZ[ 1 ] - co.LOLA_LAPAZ[ 0 ]
    h = co.LOLA_LAPAZ[ 3 ] - co.LOLA_LAPAZ[ 2 ]
    rect = matplotlib.patches.Rectangle( bl , w , h , linewidth=1 ,
                                         edgecolor='k' , facecolor='none' )
    ax.add_patch( rect )


def plot_clust_height( ds ,
                       ax: plt.Axes ,
                       perM ,
                       quantile=True ,
                       drop_zero=True ,
                       par_to_plot=co.COL ) :
    ar = ds.copy()
    com = get_dims_complement( ar , [ co.R_CENTER , co.ZM ] )

    ar = ar.sum( dim=com )
    if drop_zero :
        ar = ar.where( ar > 0 )
    if quantile :
        q = ar.quantile( perM )
    else :
        q = perM
    lab = "km from CHC"
    ar[ lab ] = ar[ co.R_CENTER ] * 100
    ar = ar.swap_dims( { co.R_CENTER : lab } )
    try :
        ar.name = co.PLOT_LABS[ par_to_plot ]
    except :
        pass
    ar.plot(
        cmap=red_cmap() ,
        vmin=0 ,
        vmax=q ,
        ax=ax ,
        x=lab ,
        )
    ax.set_yscale( 'log' )
    ax.set_ylim( 100 , 20000 )
    ax.set_xscale( 'log' )
    ax.set_xlim( .05 * 100 , 30 * 100 )
    ax.grid( True , 'major' , axis='y' )
    ax.grid( True , 'both' , axis='x' )
    ax.set_ylabel( co.PLOT_LABS[ co.ZM ] )


def plot_absolute_height( ds ,

                          ax=None ,
                          perM=.95 ,
                          drop_zero=True ,
                          par_to_plit=co.COL
                          ) :
    mer = ds.copy()
    # i = 6

    fla = co.FLAGS
    HC = 'H*CONC'

    ver_area = 'VER_AREA'
    log_center = np.log( mer[ co.R_CENTER ] )
    dis = log_center - \
          log_center.shift( { co.R_CENTER : 1 } )
    dis = dis.median()
    l1 = log_center - dis / 2
    l2 = log_center + dis / 2
    l1 = np.e ** l1
    l2 = np.e ** l2
    r_dis = (l2 - l1) * 100000
    zlen = 500
    ar = np.arange( zlen / 2 , 20000 , zlen )

    mer = mer[ [ co.CONC , fla , co.TOPO ] ]

    # return merged_ds

    mer[ 'c/v' ] = mer[ co.CONC ] / mer[ co.VOL ]

    mer = mer.interp( **{ co.ZM : ar } )

    mer[ co.VOL ] = mer[ co.GA ] * zlen
    mer[ co.CONC ] = mer[ 'c/v' ] * mer[ co.VOL ]

    mer[ co.H ] = mer[ co.TOPO ] + mer[ co.ZM ]

    mer[ HC ] = mer[ co.H ] * mer[ co.CONC ]

    var = [ co.CONC , HC ]
    com = get_dims_complement( mer , [ co.R_CENTER , co.ZM ] )
    ms = mer[ var ].sum( com )

    ms[ ver_area ] = ms[ co.ZLM ] * r_dis

    # ms:xr.DataArray = ms/ms[ver_area]

    ms[ co.CONC ] = ms[ co.CONC ].where( ms[ co.CONC ] > 0 , 0 )

    # ms = ms*zlen*r_dis

    ms[ co.H ] = ms[ HC ] / ms[ co.CONC ]

    def find_nearest( value ) :
        # ar = self.get_z_lin()
        array = np.asarray( ar )
        idx = (np.abs( array - value )).argmin()
        return array[ idx ]

    ms[ co.H ] = xr.apply_ufunc( find_nearest , ms[ co.H ] , vectorize=True )

    hs = ms.to_dataframe().groupby( [ co.H , co.R_CENTER ] ).sum()[
        co.CONC ].to_xarray()

    lab = "km from CHC"
    hs[ lab ] = hs[ co.R_CENTER ] * 100
    hs = hs.swap_dims( { co.R_CENTER : lab } )

    hs1 = hs.interp( **{ co.H : ar } )
    hs1 = hs1.combine_first( hs )

    if drop_zero :
        hs1 = hs1.where( hs1 > 0 )

    if ax is None :
        fig , ax = plt.subplots( figsize=(10 , 5) )

    q = hs1.quantile( perM )

    hs1.name = co.PLOT_LABS[ co.CONC ]

    hs1.plot(
        cmap=red_cmap() ,
        vmin=0 ,
        vmax=q ,
        ax=ax ,
        x=lab ,
        )
    ax.set_ylim( 100 , 20000 )
    ax.set_xscale( 'log' )
    ax.set_xlim( .05 * 100 , 30 * 100 )
    ax.grid( True , 'major' , axis='y' )
    ax.grid( True , 'both' , axis='x' )
    ax.set_ylabel( co.PLOT_LABS[ co.H ] )


def remove_ageclass( ds: xr.Dataset ) :
    _ds = ds[ { co.AGECLASS : 0 } ]
    return _ds


def weighted_quantile( quantiles , values , sample_weight=None ,
                       values_sorted=False , old_style=False ) :
    """ Very close to numpy.percentile, but supports weights.
    NOTE: quantiles should be in [0, 1]!
    :param values: numpy.array with data
    :param quantiles: array-like with many quantiles needed
    :param sample_weight: array-like of the same length as `array`
    :param values_sorted: bool, if True, then will avoid sorting of
        initial array
    :param old_style: if True, will correct output to be consistent
        with numpy.percentile.
    :return: numpy.array with computed quantiles.
    """
    values = np.array( values )
    quantiles = np.array( quantiles )
    if sample_weight is None :
        sample_weight = np.ones( len( values ) )
    sample_weight = np.array( sample_weight )
    assert np.all( quantiles >= 0 ) and np.all( quantiles <= 1 ) , \
        'quantiles should be in [0, 1]'

    if not values_sorted :
        sorter = np.argsort( values )
        values = values[ sorter ]
        sample_weight = sample_weight[ sorter ]

    weighted_quantiles = np.cumsum( sample_weight ) - 0.5 * sample_weight
    if old_style :
        # To be convenient with numpy.percentile
        weighted_quantiles -= weighted_quantiles[ 0 ]
        weighted_quantiles /= weighted_quantiles[ -1 ]
    else :
        weighted_quantiles /= np.sum( sample_weight )
    return np.interp( quantiles , weighted_quantiles , values )


def swap_xy2lon_lat( nds ) :
    _boo1 = (nds[ co.XLONG ].max( co.SOUTH_NORTH ) - nds[ co.XLONG ].min(
        co.SOUTH_NORTH )).sum().item() == 0
    # %% {"jupyter": {"outputs_hidden": true}}
    _boo2 = (nds[ co.XLAT ].max( co.WEST_EAST ) - nds[ co.XLAT ].min(
        co.WEST_EAST )).sum().item() == 0

    log.ger.debug( '_boo1 is %s' , _boo1 )

    if _boo1 and _boo2 :
        log.ger.debug( 'inside loop' )
        xx = [ co.XLAT , co.XLONG ]
        ww = [ co.WEST_EAST , co.SOUTH_NORTH ]
        vv = [ co.VLAT , co.VLONG ]
        rr = [ co.VLONG , co.VLAT ]
        # %% {"jupyter": {"outputs_hidden": true}}
        for i in range( 2 ) :
            ff = nds[ xx[ i ] ].mean( ww[ i ] )
            ff.name = vv[ i ]
            nds = nds.assign_coords( **{ vv[ i ] : ff } )
        for i in range( 2 ) :
            nds = nds.swap_dims( { ww[ i ] : rr[ i ] } )
    return nds


def get_combined_flx_ds( DD , dir_path , chop_list=None ) :
    # todo where is the docstring for this functions
    _ds_list = get_flx_ds_list( DD , dir_path )
    _ds_list = _ds_list[ :chop_list ]
    # %% {"jupyter": {"outputs_hidden": true}}
    ds_list = trim_flx_ds_list( _ds_list )
    # %% {"jupyter": {"outputs_hidden": true}}
    dsm = xr.open_mfdataset( ds_list , concat_dim=co.TIME , combine='nested' )
    dsm = convert_ds_time_format( dsm )
    dsm = remove_ageclass( dsm )
    # %% {"jupyter": {"outputs_hidden": true}}
    hds = import_head_ds( dir_path , DD )
    hds = hds.drop_dims( [ co.SPECIES , co.RECEPTORS , co.TIME , co.AGECLASS ] )
    # %% {"jupyter": {"outputs_hidden": true}}
    nds = xr.merge( [ hds , dsm ] )
    nds.attrs = hds.attrs.copy()
    nds = add_zmid( nds )
    for v in (set( co.HEAD_VARS ) & set( hds.variables )) :
        nds = nds.assign_coords( **{ v : nds[ v ] } )
    _cr = co.RELEASENAME
    _df = nds[ _cr ].to_pandas().str.decode( "utf-8" )
    _df = pd.to_datetime( _df , format='chc%Y%m%d_%H' )
    nds = nds.assign_coords( **{ co.RELEASE_TIME : _df.to_xarray() } )
    nds = nds.swap_dims( { co.BT : co.ZM } )

    return nds


def euristic_import_flexpart( dir_path , dd=co.D2 ) -> xr.Dataset :
    '''
    directly imports a path into a dataset
    Parameters
    ----------
    dir_path: str
    dd: str
        domain

    Returns
    -------
        dataset
    '''
    nds = get_combined_flx_ds( dd , dir_path )
    nds = swap_xy2lon_lat( nds )
    return nds
    # nds = nds[{co.RL:-1}]


def get_and_tune_flexout_from_ds_and_head( out_dask_ds , head_ds ) :
    flexout_ds = join_head( out_dask_ds , head_ds )
    # flexout_ds = add_release_time_dim(flexout_ds, self.head_ds)
    # noinspection DuplicatedCode
    flexout_ds = assign_vars_to_cords( flexout_ds )
    flexout_ds = add_lat_lot( flexout_ds )
    flexout_ds = add_zmid( flexout_ds )
    flexout_ds = add_zbot( flexout_ds )
    flexout_ds = add_zlength_m( flexout_ds )
    flexout_ds = add_alt_m( flexout_ds )
    flexout_ds = add_volume( flexout_ds )
    return flexout_ds


def join_log_pol_dom_ds( ds01: xr.Dataset ,
                         ds02: xr.Dataset ,
                         threshold: float = 2.5
                         ) -> xr.Dataset :
    """
    combines low res `ds01` and high res `ds02` `xr.Dataset`
    based on the `threshold`

    Parameters
    ----------
    ds01
        low res dataset
    ds02
        high res dataset
    threshold
        limit for the combination in degree radian units (distance from center)
    Returns
    -------
    xr.Dataset
        the combined dataset
    """
    r_vector = ds01[ co.R_CENTER ]
    r_is_big_mask = r_vector >= threshold
    ds01_trimmed = ds01.where( r_is_big_mask , drop=True )

    r_vector = ds02[ co.R_CENTER ]
    r_is_small_mask = (r_vector < threshold) & (r_vector > .01)
    ds02_trimmed = ds02.where( r_is_small_mask , drop=True )

    # noinspection PyTypeChecker
    ds_combined: xr.Dataset = xr.concat( [ ds02_trimmed , ds01_trimmed ] ,
                                         dim=co.R_CENTER )
    return ds_combined