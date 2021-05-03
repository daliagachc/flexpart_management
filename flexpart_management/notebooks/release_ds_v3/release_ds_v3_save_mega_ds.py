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
import flexpart_management.notebooks.release_ds_v3.release_ds_v3_lfc as lfc
from flexpart_management.notebooks.release_ds_v3.release_ds_v3_lfc import *


# %%


def main():
    # %%
    ds = get_dcc().load()
    # %%
    big_ds = xr.Dataset()
    all_ds = get_co_all(ds)
    # %%
    dsMAX = all_ds.max()
    dsMAX_theory = (24 * 4 * 3600)
    # %%
    all_age = get_all_age(ds)
    # %%
    all_dis = get_all_r(ds) * 100
    # %%
    all_zsl = get_all_zsl(ds)
    # %%
    all_zgl = get_all_zgl(ds)
    # %%
    ang_clock_all = get_clock_dir_all(ds)

    # %%
    all_ds18 = get_lab_ser(N18, ds)
    all_ds6 = get_lab_ser(N6, ds)
    surf_ds18 = get_lab_ser_surf(N18, ds)
    surf_ds6 = get_lab_ser_surf(N6, ds)

    surf0_ds18 = get_lab_ser_surf(N18, ds, slice_s=slice_lev0, s=LEV0)
    surf0_ds6 = get_lab_ser_surf(N6, ds, slice_s=slice_lev0, s=LEV0)
    # %%
    all_age_18 = get_lab_age(N18, ds)
    all_age_6 = get_lab_age(N6, ds)
    surf_age_18 = get_lab_age_surf(N18, ds)
    surf_age_6 = get_lab_age_surf(N6, ds)
    surf0_age_18 = get_lab_age_surf(N18, ds, slice_s=slice_lev0, s=LEV0)
    surf0_age_6 = get_lab_age_surf(N6, ds, slice_s=slice_lev0, s=LEV0)

    # %%
    all_rdis_18 = get_lab_rdis(N18, ds)
    all_rdis_6 = get_lab_rdis(N6, ds)
    surf_rdis_18 = get_lab_rdis_surf(N18, ds)
    surf_rdis_6 = get_lab_rdis_surf(N6, ds)
    surf0_rdis_18 = get_lab_rdis_surf(N18, ds, slice_s=slice_lev0, s=LEV0)
    surf0_rdis_6 = get_lab_rdis_surf(N6, ds, slice_s=slice_lev0, s=LEV0)

    # %%
    all_zsl_18 = get_lab_zsl(N18, ds)
    all_zsl_6 = get_lab_zsl(N6, ds)
    surf_zsl_18 = get_lab_zsl_surf(N18, ds)
    surf_zsl_6 = get_lab_zsl_surf(N6, ds)
    surf0_zsl_18 = get_lab_zsl_surf(N18, ds, slice_s=slice_lev0, s=LEV0)
    surf0_zsl_6 = get_lab_zsl_surf(N6, ds, slice_s=slice_lev0, s=LEV0)
    # %%
    all_zgl_18 = get_lab_zgl(N18, ds)
    all_zgl_6 = get_lab_zgl(N6, ds)
    surf_zgl_18 = get_lab_zgl_surf(N18, ds)
    surf_zgl_6 = get_lab_zgl_surf(N6, ds)
    surf0_zgl_18 = get_lab_zgl_surf(N18, ds, slice_s=slice_lev0, s=LEV0)
    surf0_zgl_6 = get_lab_zgl_surf(N6, ds, slice_s=slice_lev0, s=LEV0)

    # %%
    all_clk_18 = get_lab_clk(N18, ds)
    all_clk_6 = get_lab_clk(N6, ds)
    surf_clk_18 = get_lab_clk_surf(N18, ds)
    surf_clk_6 = get_lab_clk_surf(N6, ds)

    surf0_clk_18 = get_lab_clk_surf(N18, ds, slice_s=slice_lev0, s=LEV0)
    surf0_clk_6 = get_lab_clk_surf(N6, ds, slice_s=slice_lev0, s=LEV0)
    # %%
    mega_ds = merge_all(
        all_age=all_age,
        all_age_18=all_age_18,
        all_age_6=all_age_6,
        all_dis=all_dis,
        all_ds=all_ds,
        all_ds18=all_ds18,
        all_ds6=all_ds6,
        all_zsl=all_zsl,
        all_zgl=all_zgl,
        dsMAX_theory=dsMAX_theory,
        surf_age_18=surf_age_18,
        surf_age_6=surf_age_6,
        surf_ds18=surf_ds18,
        surf_ds6=surf_ds6,
        ang_clock_all=ang_clock_all,
        all_rdis_18=all_rdis_18,
        surf_rdis_18=surf_rdis_18,
        all_rdis_6=all_rdis_6,
        surf_rdis_6=surf_rdis_6,
        all_zsl_18=all_zsl_18,
        surf_zsl_18=surf_zsl_18,
        all_zsl_6=all_zsl_6,
        surf_zsl_6=surf_zsl_6,
        all_zgl_18=all_zgl_18,
        surf_zgl_18=surf_zgl_18,
        all_zgl_6=all_zgl_6,
        surf_zgl_6=surf_zgl_6,
        all_clk_18=all_clk_18,
        surf_clk_18=surf_clk_18,
        all_clk_6=all_clk_6,
        surf_clk_6=surf_clk_6,
        surf0_age_18=surf0_age_18,
        surf0_age_6=surf0_age_6,
        surf0_ds18=surf0_ds18,
        surf0_ds6=surf0_ds6,
        surf0_rdis_18=surf0_rdis_18,
        surf0_rdis_6=surf0_rdis_6,
        surf0_zsl_18=surf0_zsl_18,
        surf0_zsl_6=surf0_zsl_6,
        surf0_zgl_18=surf0_zgl_18,
        surf0_zgl_6=surf0_zgl_6,
        surf0_clk_18=surf0_clk_18,
        surf0_clk_6=surf0_clk_6,

    )
    mega_ds
    # %%
    desc_df = pd.read_csv(
        pjoin(co.tmp_data_path, 'description_cluster_series_v3.csv'),
        index_col='name')
    desc_dic = desc_df.T.to_dict()
    for l, d in desc_dic.items():
        mega_ds[l] = mega_ds[l].assign_attrs(d)

    # %%
    mega_ds[NORM] = mega_ds[NORM].astype(int)
    fa.compressed_netcdf_save(
        mega_ds,
        pjoin(co.tmp_data_path, 'cluster_series_v3.nc')
    )


if __name__ == '__main__':
    main()
