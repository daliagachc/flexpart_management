# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

from useful_scit.imps import *


def get_plot_save_rect( * , dom='d01' , path , i_reduction=100 , open_sum=True ) :
    dom = dom
    patt = f'*/flxout_{dom}_*.nc'
    i_sparse = i_reduction
    path_patt = os.path.join( path , patt )
    name = f'sum_rect_{dom}.nc'

    dir_path = '/homeappl/home/aliagadi/saltena_2018/flexpart_management' \
               '/flexpart_management/notebooks/run_2019-10-02_13-42-52_/'

    path_out = os.path.join( dir_path , name )

    if open_sum :
        read_sum_save(
            dom , i_sparse , path_patt ,path_out)

    # %%
    ds_sum = xr.open_dataset( path_out )

    # %%
    dc = ds_sum[ 'CONC' ]

    # %%
    center = \
    dc.where( dc == dc.max() ).to_dataframe().dropna().reset_index().iloc[ 0 ]

    # %%
    ds_sum[ 'c_sn' ] = dc[ 'south_north' ] - center[ 'south_north' ]
    ds_sum[ 'c_we' ] = dc[ 'west_east' ] - center[ 'west_east' ]

    # %%
    ds_sum = ds_sum.assign_coords( **{
        'c_sn' : ds_sum[ 'c_sn' ] ,
        'c_we' : ds_sum[ 'c_we' ]
        } )

    # %%
    a_b_square = \
        ds_sum[ 'c_sn' ] ** 2 + ds_sum[ 'c_we' ] ** 2
    r_dis = a_b_square ** (1 / 2)

    # %%
    ds_sum = ds_sum.assign_coords( **{ 'r_dis' : r_dis } )

    # %%
    ds_sc = ds_sum[ 'r_dis' ] ** 2 * ds_sum[ 'CONC' ]

    # %%
    ds_sc.plot()
    ax: plt.Axes = plt.gca()
    ax.scatter( [ center[ 'west_east' ] ] , [ center[ 'south_north' ] ] )


def read_sum_save( dom , i_sparse , path_patt, path_out ) :
    # %%
    list_files = glob.glob( path_patt )
    len( list_files )
    # %%
    files = list_files[ 0 :None :i_sparse ]
    files.sort()
    len( files )
    # %%
    ds = xr.open_mfdataset( files , concat_dim='Time' , combine='nested' )
    ds_sum = ds.sum( [ 'ageclass' , 'bottom_top' , 'releases' , 'Time' ] )
    # %%
    # %%
    ds_sum.to_netcdf( path_out )
