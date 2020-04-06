# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import flexpart_management.notebooks.log_pol_revisited. \
    log_pol_revisited_lfc as lfc

from flexpart_management.notebooks.log_pol_revisited. \
    log_pol_revisited_lfc import *


# %%
def main():
    # %%
    path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data' \
           '/runs/run_2019-10-02_13-42-52_/log_pol_log_pol/*.nc'
    # %%
    files = glob.glob(path)
    files.sort()
    # %%
    ds = xr.open_mfdataset(files, concat_dim=co.RL, combine='nested')
    # %%
    f, ax = plt.subplots(dpi=400)
    ax: plt.Axes
    ds[co.CONC].sum([co.RL, co.ZT]).plot(
        x=co.XLONG, y=co.XLAT, ax=ax, cmap='Reds'
    )
    plt.show()
    # %%
    # %%

    # %%
    ds = fa.add_lat_lon_corners(ds)
    ds = fa.add_zmid(ds)
    ds = ds.swap_dims({co.ZT: co.ZM})
    # %%
    fa.compressed_netcdf_save(ds,
                              pjoin(co.tmp_data_path, 'new_log_pol_ds_agl.nc'))

    # %%
    ds_ = ds[{co.ZM: slice(10, None)}]
    conc_ = (ds_[co.CONC] * ds_['AGE']).sum([co.RL, co.ZM])
    conc_ = conc_ / (ds_[co.CONC]).sum([co.RL, co.ZM])
    conc_.load()
    # %%
    ax = fa.get_ax_bolivia()
    conc_.name = 'age'
    conc_: xr.DataArray
    _c = conc_.to_dataset() / 24
    _c = _c.assign_attrs({'long_name': 'age'})
    cmap = plt.get_cmap('Reds', 8)
    fa.logpolar_plot(_c, name='age', ax=ax, perm=0.0, perM=4, cmap=cmap,
                     quantile=False)
    plt.show()
    # %%
    conc_.plot.hist()
    plt.show()


    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%

# %%


# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
