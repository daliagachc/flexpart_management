# ---
# jupyter:
#   jupytext:
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

# %%
import xarray
from useful_scit.imps import *
from useful_scit.util import log, zarray

import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
import wrf
# %%
from flexpart_management.modules import constants as co


def wrf_stuff():
    'doesnt do anything '
    wrf_path = '/proj/atm/saltena/runs/run_2019_05_15/wrf'

    ex_name = 'wrfout_d04_2017-12-30_16:00:00'

    ex_path = os.path.join(wrf_path,ex_name)

    ds_path = xr.open_dataset(ex_path)


    da:xr.DataArray = ds_path['W']

    da[{'Time':1,co.SOUTH_NORTH:4}].plot()
    plt.show()

    x_y = wrf.ll_to_xy(ds_path._file_obj.ds,co.CHC_LAT,co.CHC_LON)

# %%

def log_polar_approach():
    # %%

    path_FX_out = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/' \
                  'flexpart_management_data/runs/run_2019-10-02_13-42-52_/' \
                  'log_pol/run_2019-10-02_13-42-52_'

    files = glob.glob(os.path.join(path_FX_out,'d01*.nc'))

    file = files[20]

    ds = xr.open_dataset(file)
    ds = ds.loc[{co.R_CENTER:slice(.1,None)}]

    rl_i = 15
    gridarea_ = (ds[co.GRIDAREA] * 250)
    r_square = np.square(ds[co.R_CENTER])
    da_conc = ds['CONC']
    da_conc.name='CONC'

    da_r_th = da_conc[{co.RL: rl_i}].sum(co.ZT)
    da_r_th.plot(robust=True)
    plt.show()

    ax = fa.get_ax_bolivia()
    fa.logpolar_plot(da_r_th.to_dataset(),ax=ax)
    plt.show()

    da_conc[{co.RL: rl_i}].sum(co.TH_CENTER).plot(
        x=co.R_CENTER,y=co.ZT,robust=True
    )
    plt.show()

    # %%


def open_slice_and_save(filelist, out_path, x, y):
    log.ger.debug('opening big ds')
    ds = xr.open_mfdataset(filelist, concat_dim='Time', combine='nested')
    log.ger.debug('done opening')
    # %%
    WESTG = 'west_east_stag'
    SNSTG = 'south_north_stag'
    BTSTG = 'bottom_top_stag'
    z_range = z0, z1 = 0, 20
    log.ger.debug('starting to slice')
    ds_cut = ds[{
        co.WE: [x - 1, x, x + 1],
        co.SN: [y - 1, y, y + 1],
        WESTG: [x - 2, x - 1, x, x + 1],
        SNSTG: [y - 2, y - 1, y, y + 1],
        co.BT: slice(z0, z1),
        BTSTG: slice(z0, z1 + 1)
    }]
    # %%
    log.ger.debug('starting to save')
    za.compressed_netcdf_save(ds_cut, out_path)
    ds.close()