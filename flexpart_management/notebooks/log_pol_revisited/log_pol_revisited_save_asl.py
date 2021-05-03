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
    # %%
    ds = xr.open_dataset(pjoin(co.tmp_data_path, 'new_log_pol_ds_agl.nc'))
    # path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data' \
    #        '/runs/run_2019-10-02_13-42-52_/log_pol_log_pol/*.nc'
    # # %%
    # files = glob.glob(path)
    # files.sort()
    # # %%
    # ds:xr.Dataset = xr.open_mfdataset(files, concat_dim=co.RL, combine='nested')
    # ds = fa.add_lat_lon_corners(ds)
    # ds = fa.add_zmid(ds)
    # ds = ds.swap_dims({co.ZT: co.ZM})
    ds = ds.reset_coords([co.ZT],drop=True)
    ds = ds.reset_coords(['AGE'])

    # %%


    rs = ds[co.R_CENTER]
    ts = ds[co.TH_CENTER]

    r_l = []
    for r in rs[::]:
        t_l = []
        for t in ts[::]:
            print(f't:{t},r:{r}')
            _ds: xr.Dataset = ds.loc[{co.R_CENTER: r, co.TH_CENTER: t}].load().copy()
            shift_ = np.round(_ds[co.TOPO] / 500)
            shift_ = int(shift_.item())
            __ds = _ds = _ds.shift(**{co.ZM:shift_})
            # _ds[co.ZM] = _ds[co.ZM] + shift_ * 500
            _ds = _ds.expand_dims(**{co.R_CENTER: [r], co.TH_CENTER: [t]})
            t_l.append(_ds)
        tds = xr.concat(t_l, dim=co.TH_CENTER)
        r_l.append(tds)
    res = xr.concat(r_l, dim=co.R_CENTER)
    res = res.loc[{co.ZM: slice(0, 15000)}]
    # %%

    fa.compressed_netcdf_save(
        res,
        pjoin(co.tmp_data_path, 'new_log_pol_ds_asl_v01.nc')
    )

    # %%
if __name__ == '__main__':
    main()

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
