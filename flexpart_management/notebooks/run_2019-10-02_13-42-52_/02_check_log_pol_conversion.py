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
import flexpart_management.modules.FLEXOUT as FO
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co


# %% [markdown]
##Functions
# %%
def plot_combined_log_pol_coords( ds01 , ds02 , r_distance_limit=2.5 ) :
    f , ax = plt.subplots()
    limit_ = { co.R_CENTER : slice( 0 , r_distance_limit ) }
    _ds2_sliced = ds02.loc[ limit_ ]
    qmesh = plot_th_r( ds01 , ax )
    qmesh = plot_th_r( _ds2_sliced , ax )
    f: plt.Figure
    f.colorbar( qmesh , ax=ax )
    ax: plt.Axes
    ax.set_title( 'combined domain log pol coords' )
    plt.show()
    return ax

def plot_r_z_combined_log_pol_coords( ds01 , ds02 , r_distance_limit=2.5 ) :
    f , ax = plt.subplots()
    slice___ = { co.R_CENTER : slice( 0 , r_distance_limit ) }
    _ds2_sliced = ds02.loc[ slice___ ]
    qmesh = plot_r_z( ds01 , ax )
    qmesh = plot_r_z( _ds2_sliced , ax )
    f: plt.Figure
    f.colorbar( qmesh , ax=ax )
    ax: plt.Axes
    ax.set_title( 'combined domain log pol coords' )
    ax.set_xlim(0,30)
    plt.show()
    return ax


def plot_th_r( ds , ax ) :
    sum_geo_ = [ co.ZT , co.RL ]
    plot_threshold = 1e2
    qmesh = plot_qmesh( ds , ax , plot_threshold , sum_geo_ )
    return qmesh


def plot_r_z( ds , ax ) :
    sum_geo_ = [ co.TH_CENTER , co.RL ]
    plot_threshold = 1e2
    qmesh = plot_qmesh( ds , ax ,
                        plot_threshold ,
                        sum_geo_ ,
                        x=co.R_CENTER ,
                        y=co.ZM,
                        yscale='linear',
                        ylim_m=250,
                        ylim_M=30000
                        )
    return qmesh


def plot_qmesh( ds , ax ,
                plot_threshold ,
                sum_dims ,
                x=co.TH_CENTER ,
                y=co.R_CENTER ,
                yscale='log' ,
                ylim_m=.2 ,
                ylim_M=20 ) :
    vmin = 1e1
    vmax = 1e5
    cmap = plt.get_cmap( 'Reds' )
    conc__sum: xr.DataArray = ds[ co.CONC ].sum( sum_dims )
    conc__sum = conc__sum.where( conc__sum > plot_threshold )
    qmesh = conc__sum.plot( ax=ax ,
                            add_colorbar=False ,
                            vmin=vmin ,
                            vmax=vmax ,
                            cmap=cmap ,
                            x=x ,
                            y=y
                            )
    ax: plt.Axes
    ax.set_ylim( ylim_m , ylim_M )
    ax.set_yscale( yscale )
    return qmesh


def get_ds_dom_file( dom01_pat , path , i_file=10 ) :
    files = glob.glob( os.path.join( path , dom01_pat ) )
    files.sort()
    file = files[ i_file ]
    print(file)
    ds = xr.open_dataset( file )
    ds = fa.add_zmid( ds )
    return ds


# %%
def main() :
    # %%
    path = '/homeappl/home/aliagadi/wrk/' \
           'DONOTREMOVE/flexpart_management_data' \
           '/runs/run_2019-10-02_13-42-52_/log_pol' \
           '/run_2019-10-02_13-42-52_/'

    # %%
    dom01_pat = '*d01*.nc'
    ds01 = get_ds_dom_file( dom01_pat , path, i_file=10 )
    dom02_pat = '*d02*.nc'
    ds02 = get_ds_dom_file( dom02_pat , path, i_file=10 )

    # %%
    ucp.set_dpi( 150 )
    ax = plot_combined_log_pol_coords(
        ds01 , ds02,
        r_distance_limit=2.5
        )
    # %%
    ax = plot_r_z_combined_log_pol_coords(
        ds01 , ds02,
        r_distance_limit=2.5)
    # %%


main()
