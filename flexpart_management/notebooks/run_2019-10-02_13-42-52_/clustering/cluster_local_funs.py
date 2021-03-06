# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from useful_scit.imps import *

from flexpart_management.modules import flx_array as fa, constants as co

DF_PATH = '/Users/diego/flexpart_management/' \
          'flexpart_management/tmp_data' \
          '/prop_df.nc'
N_CLUSTERS = 18

FIG_PATH = '/Users/diego/flexpart_management/flexpart_management/victoria_trento/figures'

def get_weighted_mean(ds_lab, new_lab_p, weighted_lab):
    dims = list(ds_lab[weighted_lab].dims)
    if len(dims) is not 1:
        raise AttributeError
    dim = dims[0]
    ds_lab: xr.DataArray
    ds_lab = ds_lab.swap_dims({dim: weighted_lab})
    complement = fa.get_dims_complement(ds_lab, weighted_lab)
    da = ds_lab[new_lab_p].sum(
        complement)
    da_sum = (da * da[weighted_lab]).sum()
    da_tot = da.sum()
    res = da_sum / da_tot
    return res


def weightin_over_dic(df_prop, ds_lab_dic, new_lab_p, weighted_lab):
    df_prop[weighted_lab] = np.nan
    for ci in range(18):
        ds_lab = ds_lab_dic[ci]
        res = get_weighted_mean(ds_lab, new_lab_p, weighted_lab)
        df_prop.loc[ci, weighted_lab] = res


def number_marker_plot(df_prop, x_column,
                       y_column, ax=None, color='red'):
    if ax is None:
        f, ax = plt.subplots()
    df_prop.plot.scatter(x=x_column, y=y_column, alpha=0, ax=ax)
    for i, r in df_prop.iterrows():
        # print( i )
        # r_km = r[ co.R_CENTER ]
        # ratio_per = r[ y_column ]
        ax.text(
            x=r[x_column],
            y=r[y_column],
            s=i, color=color,
            horizontalalignment='center',
            verticalalignment='center',

        )


def get_and_save_df_prop(ds, new_lab_p,
                         zm_topo='Z_AG',
                         ratio_surf_tot_lab='ratio_surf_tot',
                         df_path=DF_PATH,
                         key='v01',
                         ):
    ds_lab_dic = {}
    for ci in range(N_CLUSTERS):
        ds_lab = ds[[new_lab_p]].where(ds[co.LAB] == ci).copy()
        ds_lab_dic[ci] = ds_lab.copy()
    # %%
    x = np.sin(ds[co.TH_CENTER])
    x.name = 'X'
    # x.plot()
    # plt.show()
    y = np.cos(-ds[co.TH_CENTER])
    y.name = 'Y'
    # y.plot()
    # plt.show()
    # %%
    # ds_lab_dic = { }
    for ci in range(N_CLUSTERS):
        # ds_lab = ds[ [ new_lab_p ] ].where( ds[ co.LAB ] == ci ).copy()
        ds_lab = ds_lab_dic[ci].copy()
        ds_lab_dic[ci] = ds_lab.assign_coords(**{'X': x, 'Y': y})
    # %%
    # %%
    df_prop = pd.DataFrame(range(N_CLUSTERS), columns=['cluster_i'])
    df_prop = df_prop.set_index('cluster_i')
    # %%
    # %%
    surface_limit = 1500
    # ratio_surf_tot_lab = ratio_surf_tot_lab
    df_prop[ratio_surf_tot_lab] = np.nan
    for ci in range(N_CLUSTERS):
        ds_lab = ds_lab_dic[ci]
        _boo = (ds_lab[co.ZM] - ds_lab[co.TOPO]) < surface_limit
        ds_surf = ds_lab.where(_boo)
        ds_surf_sum = ds_surf[new_lab_p].sum()
        ds_tot_sum = ds_lab[new_lab_p].sum()
        ratio_surf_tot = ds_surf_sum / ds_tot_sum
        #     print(ratio_surf_tot)
        df_prop.loc[ci, ratio_surf_tot_lab] = ratio_surf_tot
    # %%
    weighted_lab = co.R_CENTER
    weightin_over_dic(df_prop, ds_lab_dic, new_lab_p, weighted_lab)
    # %%
    weighted_lab = 'X'
    weightin_over_dic(df_prop, ds_lab_dic, new_lab_p, weighted_lab)
    weighted_lab = 'Y'
    weightin_over_dic(df_prop, ds_lab_dic, new_lab_p, weighted_lab)
    # %%
    weighted_lab = co.ZM
    df_prop[weighted_lab] = np.nan
    for ci in range(N_CLUSTERS):
        # print(ci)
        ds_lab = ds_lab_dic[ci].copy()
        res = get_weighted_mean(ds_lab, new_lab_p, weighted_lab)
        # print(res)
        df_prop.loc[ci, weighted_lab] = res
    # %%
    # zm_topo = zm_toppo
    weighted_lab = zm_topo
    ds_zm_topo = ds[co.ZM] - ds[co.TOPO]
    df_prop[weighted_lab] = np.nan
    for ci in range(N_CLUSTERS):
        #     print( ci )
        ds_lab = ds_lab_dic[ci].copy()
        ds_lab = ds_lab.assign_coords(**{weighted_lab: ds_zm_topo})
        da = ds_lab[new_lab_p].sum(co.RL)
        da_sum = (da * da[weighted_lab]).sum()
        da_tot = da.sum()
        res = da_sum / da_tot
        #     print( res )
        df_prop.loc[ci, weighted_lab] = res
    # %%
    x = df_prop['X']
    y = df_prop['Y']
    th = np.arctan2(x, y)
    df_prop[co.TH_CENTER] = th
    # %%
    clock = 'clock'
    cl = df_prop[co.TH_CENTER] * 12 / (2 * np.pi)
    cl: pd.DataFrame = cl.round()
    cl = cl.astype(int)
    df_prop[clock] = cl
    # %%
    # df_path = df_path
    df_prop.to_hdf(df_path, key=key)
    return df_prop


def add_zoom_plot(ax, df_prop, xl, yl):
    axin = inset_axes(ax, '80%', '20%', loc=4)
    xmin = 0
    xmax = 70
    ymin = 100
    ymax = 1800
    _boo = (df_prop[yl] > ymin) & (df_prop[yl] < ymax) \
           & (df_prop[xl] > xmin) & (df_prop[xl] < xmax)
    number_marker_plot(df_prop[_boo], xl, yl, axin)
    axin.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    axin.xaxis.set_visible('False')
    axin.yaxis.set_visible('False')
    plt.yticks(visible=False)
    plt.xticks(visible=False)
    axin.set_xlabel(None)
    axin.set_ylabel(None)
    mark_inset(ax, axin, loc1=2, loc2=3, fc="none", ec="0.5")


def add_labels_to_cluster_markers(ax, df_prop, hgk_, km_):
    df_prop['hgk_xy'] = [[(6, 6)]] * len(df_prop)
    df_prop.loc[0, 'hgk_xy'] = [[[-23, 3]]]
    df_prop.loc[1, 'hgk_xy'] = [[[5, 6]]]
    df_prop.loc[2, 'hgk_xy'] = [[[-10, 15]]]
    df_prop.loc[3, 'hgk_xy'] = [[[10, -10]]]
    df_prop.loc[4, 'hgk_xy'] = [[[-10, -8]]]
    df_prop.loc[5, 'hgk_xy'] = [[[-17, 30]]]
    df_prop.loc[6, 'hgk_xy'] = [[[12, -7]]]
    df_prop.loc[7, 'hgk_xy'] = [[[-16, -8]]]
    df_prop.loc[8, 'hgk_xy'] = [[[-16, -8]]]
    df_prop.loc[9, 'hgk_xy'] = [[[0, -10]]]
    df_prop.loc[10, 'hgk_xy'] = [[[-5, 15]]]
    df_prop.loc[11, 'hgk_xy'] = [[[10, -1]]]
    df_prop.loc[12, 'hgk_xy'] = [[[4, 8]]]
    df_prop.loc[13, 'hgk_xy'] = [[[5, -15]]]
    df_prop.loc[14, 'hgk_xy'] = [[[10, 0]]]
    df_prop.loc[15, 'hgk_xy'] = [[[6, -8]]]
    df_prop.loc[16, 'hgk_xy'] = [[[8, 4]]]
    df_prop.loc[17, 'hgk_xy'] = [[[-25, 0]]]


    for l, row in df_prop.iterrows():
        ax.annotate(
            row['short_name'],  # + str(l),
            (row[km_], row[hgk_]),
            fontsize=5,
            horizontalalignment='left',
            verticalalignment='center',
            xytext=row['hgk_xy'][0],
            textcoords='offset points',
            # color = 'blue',
            alpha=.5,
            arrowprops={'arrowstyle': '-', 'alpha': .1}

        )


def add_labels_to_cluster_markers_height(ax, df_prop, km_):
    # df_prop['hgk_xy'] = [[(6, 6)]] * len(df_prop)
    # df_prop.loc[0, 'hgk_xy'] = [[[-23, 3]]]
    # df_prop.loc[1, 'hgk_xy'] = [[[5, 6]]]
    # df_prop.loc[2, 'hgk_xy'] = [[[-23, 0]]]
    # df_prop.loc[3, 'hgk_xy'] = [[[10, -10]]]
    # df_prop.loc[4, 'hgk_xy'] = [[[-10, -8]]]
    # df_prop.loc[5, 'hgk_xy'] = [[[-17, 30]]]
    # df_prop.loc[6, 'hgk_xy'] = [[[12, -7]]]
    # df_prop.loc[7, 'hgk_xy'] = [[[-16, -8]]]
    # df_prop.loc[8, 'hgk_xy'] = [[[-16, -8]]]
    # df_prop.loc[9, 'hgk_xy'] = [[[0, -10]]]
    # df_prop.loc[10, 'hgk_xy'] = [[[-5, 15]]]
    # df_prop.loc[11, 'hgk_xy'] = [[[10, -1]]]
    # df_prop.loc[12, 'hgk_xy'] = [[[4, 8]]]
    # df_prop.loc[13, 'hgk_xy'] = [[[5, -15]]]
    # df_prop.loc[14, 'hgk_xy'] = [[[10, 0]]]
    # df_prop.loc[15, 'hgk_xy'] = [[[6, -8]]]
    # df_prop.loc[16, 'hgk_xy'] = [[[8, 4]]]
    # df_prop.loc[17, 'hgk_xy'] = [[[-35, -15]]]

    _df:pd.DataFrame = df_prop.set_index('short_name').copy()
    markers = ['12_SM','03_SM','02_SR']
    _df = _df.loc[markers]
    _df.loc['02_SR','hgk_xy'] = [[[10,15]]]
    _df.loc['12_SM','hgk_xy'] = [[[10,10]]]
    _df.loc['03_SM','hgk_xy'] = [[[10,0]]]

    hasl = 'height above sea level [km]'
    for l, row in _df.iterrows():
        ax.annotate(
            l,  # + str(l),
            (row[km_], row[hasl]),
            fontsize=5,
            horizontalalignment='left',
            verticalalignment='center',
            xytext=row['hgk_xy'][0],
            textcoords='offset points',
            # color = 'blue',
            alpha=.5,
            arrowprops={'arrowstyle': '-', 'alpha': .1}

        )


def add_ax_lab(ax, text):
    ax.annotate(text,
                [0, 1],
                xytext=[2, 2],
                xycoords='axes fraction',
                textcoords='offset points',
                horizontalalignment='left',
                verticalalignment='bottom',
                color='k'
                )

def add_indices(ax1, ax2, ax3, ax4):
    axs = [ax1, ax2, ax3, ax4]
    texts = ['a', 'b', 'c', 'd']
    for ax, text in zip(axs, texts):
        fa.add_ax_lab(ax, text)