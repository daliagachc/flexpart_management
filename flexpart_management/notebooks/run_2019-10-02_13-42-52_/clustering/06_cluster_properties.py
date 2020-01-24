# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
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

# %% [markdown]
# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# %%
# %% [markdown]
# imports
# %%
import flexpart_management.modules.clustering_funs as cfuns
from useful_scit.imps import *
# noinspection PyUnresolvedReferences
import matplotlib.colors
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
# noinspection PyUnresolvedReferences
import flexpart_management.modules.flx_array as fa

from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# %%

import cluster_local_funs as loc_funs

# %%


def main():
    # %%

    co.LAB = 'lab'

    # plt.rcParams[ 'figure.facecolor' ] = 'white'

    # %%

    log.ger.setLevel(log.log.DEBUG)

    # %%
    # noinspection PyUnusedLocal,PyShadowingNames
    def open_if_taito():
        # noinspection SpellCheckingInspection
        path = \
            '/homeappl/home/aliagadi/wrk/DONOTREMOVE' \
            '/flexpart_management_data/runs/' \
            'run_2019-10-02_13-42-52_/' \
            'log_pol/run_2019-10-02_13-42-52_'
        # flp = FLP.FlexLogPol(path,concat=True)
        # flp_instance = FLP.FlexLogPol(path,concat=False)
        selfFLP = FlexLogPol.FlexLogPol(
            path,
            # concat=True,
            concat=False,
            get_clusters=False,
            # open_merged=False,
            open_merged=True,
            # merge_ds=False ,
            # merge_ds=True ,
            clusters_avail=False,

            # postprocess set to false since we are opening the re interpolated
            # version
            postprocess=False,

            use_new_merge_fun=True,

            # set to false bc already done in the saved version
            filter_r_min_max=False,
        )
        selfFLP.get_list_datasets_saved()
        # noinspection PyUnresolvedReferences
        ds = selfFLP.open_ds_version('ds_clustered_18.nc')
        return selfFLP, ds

    # %%
    # selfFLP,ds = open_if_taito()
    # path = '/Users/diego/flexpart_management/flexpart_management/tmp_data' \
    #        '/ds_clustered_18.nc'
    ds = xr.open_mfdataset(co.latest_ds_mac, concat_dim=co.RL, combine='nested')
    # ds = xr.open_dataset( path )

    conc_lab = 'CONC_smooth_t_300_z_25_r_100_th_50'
    new_lab_p = 'conc_smooth_p'
    new_lab_p_t = 'conc_smooth_p_t'
    # cfuns.add_total_per_row( ds , conc_lab , new_lab_p )
    # cfuns.add_time_per_row( ds , conc_lab , new_lab_p_t )
    # %%
    zm_topo = 'Z_AG'
    ratio_surf_tot_lab = 'ratio_surf_tot'
    key = 'v01'

    # df_prop = get_and_save_df_prop(
    #     ds , new_lab_p ,
    #     zm_topo=zm_topo , ratio_surf_tot_lab=ratio_surf_tot_lab ,
    #     key=key , df_path=DF_PATH
    #     )
    df_prop = pd.read_hdf(loc_funs.DF_PATH, key=key)
    clock_ = (np.mod(df_prop['clock'] - 1, 12) + 1)
    df_prop['clock'] = clock_.astype(int)
    km_ = 'distance from CHC [km]'
    hg_ = 'height above ground [m]'
    hgk_ = 'height above ground [km]'
    df_prop[km_] = df_prop[co.R_CENTER] * 100
    df_prop[hg_] = df_prop[zm_topo]
    df_prop[hgk_] = df_prop[hg_] / 1000
    ha_ = 'height above sea level [m]'
    hak_ = 'height above sea level [km]'
    # df_prop[ km_ ] = df_prop[co.R_CENTER] * 100
    df_prop[ha_] = df_prop[co.ZM]
    df_prop[hak_] = df_prop[ha_] / 1000
    ratio_lab = 'ratio_lab'
    df_prop[ratio_lab] = df_prop[ratio_surf_tot_lab] * 100

    # %%
    def _get_lab(r):
        cl = int(r["clock"])
        clus_num = r.name
        rn = get_range(clus_num)
        st = f'{cl :0>2d}_{rn}'
        return st

    def get_range(clus_num):
        if clus_num in co.short_range_clusters:
            rn = 'SR'
        if clus_num in co.mid_short_range_clusters:
            rn = 'SM'
        if clus_num in co.mid_range_clusters:
            rn = 'MR'
        if clus_num in co.long_range_clusters:
            rn = 'LR'
        return rn

    short_name = 'short_name'
    df_prop[short_name] = \
        df_prop.apply(lambda r: _get_lab(r), axis=1)

    range_name = 'range'
    df_prop[range_name] = \
        df_prop.apply(lambda r: get_range(r.name), axis=1)

    # %%
    dss = ds[new_lab_p].sum(co.RL).load()
    clus_num = 2

    # %%
    def get_inf_per(ds, dss, clus_num):
        _boo = ds[co.LAB] == clus_num
        res = dss.where(_boo).sum().load().item()
        return res

    inf_per_name = 'inf_per'
    df_prop[inf_per_name] = \
        df_prop.apply(lambda r: get_inf_per(ds, dss, r.name), axis=1)
    srr_inf_name = 'SRR [%]'
    df_prop[srr_inf_name] = df_prop[inf_per_name] / df_prop[inf_per_name].sum() * 100

    # %%

    df_prop: pd.DataFrame
    df_prop = df_prop.sort_values(co.R_CENTER)
    csv_path = '/Users/diego/flexpart_management/' \
               'flexpart_management/tmp_data/prop_df_.csv'
    path = csv_path
    df_prop.to_csv(path)
    # %%
    df_prop.to_dict()

    # %%

    ucp.set_dpi(300)
    # %%

    ax = cfuns.plot_cluster_summary_figure(
        df_prop,
        hgk_,
        km_,
        save_fig=True,
        fig_save_name='dis_vs_hag.pdf',
        xy_locs=([200, .5], [0, 4], [400, 6], [950, 5])
    )

    loc_funs.add_labels_to_cluster_markers(ax, df_prop, hgk_, km_)
    plt.show()
    # print((row[km_], row[hgk_]))
    # ax.text()



    # %%

    cfuns.plot_cluster_summary_figure(
        df_prop,
        hak_,
        km_,
        save_fig=True,
        fig_save_name='dis_vs_hsl.pdf',
        xy_locs=([-10, 5.5], [200, 5.1], [450, 7.5], [950, 7])

    )
    plt.show()

    # %%

    cfuns.plot_cluster_summary_figure(
        df_prop,
        ratio_lab,
        km_,
        save_fig=True,
        fig_save_name='dis_vs_surface_influence.pdf',
        xy_locs=([100, 80], [180, 50], [500, 30], [950, 10]),
        y_label=r'$\frac{\mathrm{SRR}_{<1.5\mathrm{km}}}{\mathrm{SRR}_{\mathrm{total}}}\ [\%]$'

    )
    plt.show()

    # %%

    cfuns.plot_cluster_summary_figure(
        df_prop,
        srr_inf_name,
        km_,
        save_fig=True,
        fig_save_name='dis_vs_srr_influence.pdf',
        xy_locs=([100, 1], [0, 9], [500, 11], [950, 9]),
        y_range=(0, 13),

    )
    plt.show()

# %%
    f,axs = plt.subplots(2,2, sharex=True,
                         figsize=(8,8/1.4))
    axf = axs.flatten()
    ax = axf[0]
    ax = cfuns.plot_cluster_summary_figure(
        df_prop,
        hgk_,
        km_,
        # save_fig=True,
        fig_save_name='dis_vs_hag.pdf',
        xy_locs=([200, .5], [0, 4], [400, 6], [950, 5]),
        ax = ax,
        add_cluster_group_label=False
    )

    loc_funs.add_labels_to_cluster_markers(ax, df_prop, hgk_, km_)
    # plt.show()
    # print((row[km_], row[hgk_]))
    # ax.text()


    cfuns.plot_cluster_summary_figure(
        df_prop,
        hak_,
        km_,
        # save_fig=True,
        fig_save_name='dis_vs_hsl.pdf',
        xy_locs=([-10, 5.5], [200, 5.1], [450, 7.5], [950, 7]),
        ax=axf[1],
        add_cluster_group_label=False

    )
    # plt.show()



    cfuns.plot_cluster_summary_figure(
        df_prop,
        ratio_lab,
        km_,
        # save_fig=True,
        fig_save_name='dis_vs_surface_influence.pdf',
        xy_locs=([100, 80], [180, 50], [500, 30], [950, 10]),
        y_label=r'$\frac{\mathrm{SRR}_{<1.5\mathrm{km}}}{\mathrm{SRR}_{\mathrm{total}}}\ [\%]$',
        ax=axf[2],
        add_vertical_lines=True,
        add_cluster_group_label=True

    )
    # plt.show()


    cfuns.plot_cluster_summary_figure(
        df_prop,
        srr_inf_name,
        km_,
        # save_fig=True,
        fig_save_name='dis_vs_srr_influence.pdf',
        xy_locs=([-30, 5], [0, 9], [500, 11], [950, 9]),
        y_range=(0, 13),
        add_vertical_lines=True,
        add_cluster_group_label=False,
        ax=axf[3]
    )

    loc_funs.add_indices(*axf)

    f:plt.Figure
    f.tight_layout()
    f.savefig(os.path.join(loc_funs.FIG_PATH,'4-panel-cluster-medeoids.pdf'))

    plt.show()


    # %%
    # km_ = 'distance from CHC [km]'

    f, ax = plt.subplots(figsize=(10, 6))
    ax: plt.Axes
    xl = km_
    yl = ha_
    loc_funs.number_marker_plot(df_prop, xl, yl, ax)
    axin = inset_axes(ax, '60%', '40%', loc=4)

    xmin = 0
    xmax = 150
    ymin = 4000
    ymax = 5500

    _boo = (df_prop[yl] > ymin) & (df_prop[yl] < ymax) \
           & (df_prop[xl] > xmin) & (df_prop[xl] < xmax)

    loc_funs.number_marker_plot(df_prop[_boo], xl, yl, axin)
    axin.set(xlim=(xmin, xmax), ylim=(ymin, ymax))

    # number_marker_plot( df_prop , xl , yl , axin )
    # axin.set(xlim=(0,150),ylim=(4000,5500))
    axin.xaxis.set_visible('False')
    axin.yaxis.set_visible('False')
    plt.yticks(visible=False)
    plt.xticks(visible=False)
    axin.set_xlabel(None)
    axin.set_ylabel(None)
    mark_inset(ax, axin, loc1=1, loc2=3, fc="none", ec="0.5")
    # axin.set_xticks( visible=False )
    # axin.set_yticks( visible=False )

    plt.show()

    # %%
    # df_prop.plot.scatter(x=co.R_CENTER,y=ratio_surf_tot_lab)
    # f , ax = plt.subplots()

    ax: plt.Axes

    # km_ = 'distance from CHC [km]'
    ha_ = 'height above sea level [m]'
    # df_prop[ km_ ] = df_prop[co.R_CENTER] * 100
    # df_prop[ha_] = df_prop[co.ZM]
    f, ax = plt.subplots(figsize=(10, 6))
    ax: plt.Axes
    xl = km_
    yl = ratio_lab
    loc_funs.number_marker_plot(df_prop, xl, yl, ax)


    # %%
    df_prop['lat_chc'] = (df_prop[co.R_CENTER] * df_prop[
        'Y']) + co.CHC_LAT
    df_prop['lon_chc'] = (df_prop[co.R_CENTER] * df_prop[
        'X']) + co.CHC_LON

    ax = fa.get_ax_bolivia(
        #     fig_args={'figsize':(8,8)}
    )
    # ax.legend()
    xl = 'lon_chc'
    yl = 'lat_chc'

    def _plot(ax):
        df_prop.plot.scatter(x=xl, y=yl, alpha=1, ax=ax, c='white',
                             s=100)
        for i, r in df_prop.iterrows():
            # print( i )
            # r_km = r[ co.R_CENTER ]
            # ratio_per = r[ y_column ]
            t = ax.text(
                x=r[xl],
                y=r[yl],
                s=i, color='red',
                horizontalalignment='center',
                verticalalignment='center',
                fontdict={'size': 13, 'weight': 'bold'},
                #         backgroundcolor='white', alpha=.5

            )
            t.set_bbox(
                dict(facecolor='white', alpha=0.5, edgecolor='white'))

    _plot(ax)

    # %%
    df_prop['lat_chc'] = (df_prop[co.R_CENTER] * df_prop[
        'Y']) + co.CHC_LAT
    df_prop['lon_chc'] = (df_prop[co.R_CENTER] * df_prop[
        'X']) + co.CHC_LON

    ax = fa.get_ax_lapaz(
        #     fig_args={'figsize':(8,8)}
    )
    # ax.legend()
    xl = 'lon_chc'
    yl = 'lat_chc'

    xmin = -70
    xmax = -66
    ymin = -18
    ymax = -13.5

    _boo = (df_prop[yl] > ymin) & (df_prop[yl] < ymax) \
           & (df_prop[xl] > xmin) & (df_prop[xl] < xmax)

    def _plot(ax):
        df_prop.plot.scatter(x=xl, y=yl, alpha=1, ax=ax, c='white',
                             s=100)
        for i, r in df_prop[_boo].iterrows():
            # print( i )
            # r_km = r[ co.R_CENTER ]
            # ratio_per = r[ y_column ]
            t = ax.text(
                x=r[xl],
                y=r[yl],
                s=i, color='red',
                horizontalalignment='center',
                verticalalignment='center',
                fontdict={'size': 13, 'weight': 'bold'},
                #         backgroundcolor='white', alpha=.5

            )
            t.set_bbox(
                dict(facecolor='white', alpha=0.5, edgecolor='white'))

    _plot(ax)

    # %%
    df_prop.to_excel('/tmp/excel.xls')

    df_prop.to_csv(co.prop_df_path)
    df_prop.to_hdf(os.path.join(co.tmp_data_path, 'prop_df_.nc'), key='v01')

    # %%

    # %%


