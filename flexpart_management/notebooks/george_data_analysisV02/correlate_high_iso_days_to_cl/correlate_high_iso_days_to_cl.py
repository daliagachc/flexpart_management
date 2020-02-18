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
from flexpart_management.notebooks.george_data_analysisV02.correlate_high_iso_days_to_cl.correlate_high_iso_days_to_cl_lfc \
    import *


# %%
def main():
    # %%
    # %%
    clus_ts = fa.open_clus_ts()
    iso_ts = fa.open_iso_ts()
    # %%
    geo_ts = fa.import_george_time_periods()
    # %%
    ds = fa.open_temp_ds_clustered_18()

    # %%
    clus_ds = clus_ts.to_xarray().to_array(dim='lab_name', name='srr_pt')
    # %%
    jan_fl = clus_ds[co.RL].dt.month == 1
    all_fl = clus_ds[co.RL].dt.month >= 0
    # UTC time. Subtract 4 to obtain local time.
    nig_fl = (clus_ds[co.RL].dt.hour <= 11) | (clus_ds[co.RL].dt.hour >= 23)
    jan_nig_fl = jan_fl & nig_fl
    george_flag = get_geo_fl(geo_ts, clus_ds)
    jn_no_iso = np.logical_and(jan_nig_fl, ~george_flag)

    # %%
    cases_flag_dic = get_geo_fl_dic(
        geo_ts=geo_ts, clus_ds=clus_ds,
        filter='jan_case'
    )
    # %%

    fls_dic = {
        'high iso'        : george_flag,
        'jan night no iso': jn_no_iso,
        'january night'   : jan_nig_fl,
        'january'         : jan_fl,
        'night'           : nig_fl,
        'all'             : all_fl,
    }

    for k, v in fls_dic.items():
        clus_ds = clus_ds.assign_coords({k: v})

    # %%
    med_ds = xr.open_dataset(pjoin(co.tmp_data_path, 'clus_medeoid_stats.nc'))
    # %%
    # %%
    order = plot_box_plot_ratio(cases_flag_dic, clus_ds, fls_dic)
    # %%
    rr = plot_comparison(clus_ds, med_ds, fls_dic, cases_flag_dic, order=None)
    # %%
    not_so_important_plot(med_ds)
    # %%
    key = 'high iso'

    plt.show()
    # %%
    med_ds.loc[
        {'stat': 'avg', 'lab_name': '02_MR', 'stat_dim': 'ZMID_AGL_stat'}][
        'stat_vals'].plot()
    plt.show()
    # %%
    ds_conc = ds[co.CONC]
    # %%
    agl_ds = get_agl_ds(ds_conc)
    # %%
    agl = False
    res_list = plot_cases_distance(agl, cases_flag_dic, ds_conc, fls_dic)
    # %%
    agl = True
    res_list = plot_cases_distance(agl, cases_flag_dic, ds_conc, fls_dic)
    # %%
    plot_z_per(cases_flag_dic, ds_conc, fls_dic)
    # %%
    plot_z_per(cases_flag_dic, agl_ds, fls_dic, agl=True)

    # %%
    _ser = pd.Series(cases_flag_dic)
    # %%
    f, axs = plt.subplots(
        2, 5, figsize=(12, 12),
        sharey=True, sharex=True)
    for i, (k, v) in enumerate(_ser.items()):
        print(k)
        ax = axs.flatten()[i]
        plot_box_plot_ratio(
            _ser.loc[[k]].to_dict(),
            clus_ds, fls_dic, order=order[::-1],
            ax=ax
        )
        ax.grid(axis='y',linestyle=':')
        ax.set_title(k)
    [ax.set_ylabel('') for ax in axs[:, 1:].flatten()]
    [ax.set_xlabel('') for ax in axs[:-1, :].flatten()]

    f.show()

# %%
if __name__ == '__main__':
    main()

# %%
