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
from useful_scit import plot
from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
import wrf

from shapely.ops import cascaded_union
from descartes import PolygonPatch

plt, co


# %%


def sh_polygon_from_row(rr, **kwargs):
    from shapely.geometry import Polygon
    # kw = {'closed':True,**kwargs}
    r = np.round(rr, 3)
    pol = Polygon([
        [r[co.LON_00], r[co.LAT_00]],
        [r[co.LON_10], r[co.LAT_10]],
        [r[co.LON_11], r[co.LAT_11]],
        [r[co.LON_01], r[co.LAT_01]],
    ])
    return pol


def n2c(range):
    di = dict(
        SR=ucp.cc[0],
        SM=ucp.cc[1],
        MR=ucp.cc[2],
        LR=ucp.cc[3]
    )
    return di[range]


def n2m(range):
    di = dict(
        SR='o',
        SM='s',
        MR='^',
        LR='p'
    )
    return di[range]


def get_res_quan(dac_sum, lab, _q, conc_name='CONC'):
    dl = dac_sum.where(dac_sum['lab'] == lab).sum(co.ZM)
    _df = dl.to_dataframe().sort_values(conc_name)
    _df['cum'] = _df[conc_name].cumsum() / _df[conc_name].sum()
    _df = _df[_df['cum'] >= (1 - _q)]
    _ds = _df.to_xarray()
    res = dl.where((_ds[conc_name] >= 0))
    res = res.where(~(res > 0), 1)
    _df = res.to_dataframe()
    _df = _df[_df[conc_name] > 0]
    return _df


def plot_pathways(npdf, dac_sum, conc_name, lon_range=15, lat_range=13,
                  centroid_to_plot=['LR', 'MR'], chc_lp_legend=False,
                  q_level=.8, ax_bolivia=True, ax=None, min_fs=5):
    if ax is None:
        ucp.set_dpi(300)
        f_width = 7.25
        figsize = (f_width, f_width / 1.6)
        _, ax = plt.subplots(
            subplot_kw=dict(projection=crt.crs.PlateCarree()),
            figsize=figsize
        )
    f = ax.figure
    ax: plt.Axes
    if ax_bolivia:
        fa.get_ax_bolivia(
            ax=ax, plot_cities=False, map_res='50m', lake_face_color='none',
            map_line_alpha=.5, chc_lp_legend=chc_lp_legend,
            grid_alpha=0,
            draw_labels=False,
        )
    else:
        fa.get_ax_lapaz(
            ax=ax, plot_cities=False, lake_face_color='none',
            map_line_alpha=.5, chc_lp_legend=chc_lp_legend,
            grid_alpha=0,
            draw_labels=False,
            y_left_lab=False
        )
    # gpdf = npdf.groupby('range')
    for l, r in npdf.iterrows():
        _q = q_level
        l = r['cluster_i']

        res = get_res_quan(dac_sum, l, _q, conc_name=conc_name)

        pols = res.apply(lambda r: sh_polygon_from_row(r), axis=1)
        u = cascaded_union(pols)
        patch = PolygonPatch(
            u, alpha=.7,
            facecolor=r['c6_colors'],
            edgecolor=r['c6_colors'],
            linewidth=1,
            zorder=11
        )
        ax.add_patch(patch)
    npdf['text_xy'] = [[[0, 0]]] * len(npdf)
    npdf.loc['07_LR', 'text_xy'] = [[[-5, -12]]]
    npdf.loc['08_LR', 'text_xy'] = [[[-5, 7]]]
    npdf.loc['10_LR', 'text_xy'] = [[[8, 0]]]
    npdf.loc['11_MR', 'text_xy'] = [[[-13, 7]]]
    npdf.loc['02_MR', 'text_xy'] = [[[-10, 7]]]
    npdf.loc['04_MR', 'text_xy'] = [[[-10, 7]]]
    npdf.loc['05_MR', 'text_xy'] = [[[5, -10]]]
    npdf.loc['09_MR', 'text_xy'] = [[[-25, -8]]]
    npdf.loc['08_SM', 'text_xy'] = [[[-23, -15]]]
    npdf.loc['12_SM', 'text_xy'] = [[[-3, 7]]]
    npdf.loc['03_SM', 'text_xy'] = [[[5, -4]]]
    npdf.loc['06_SM', 'text_xy'] = [[[-7, -10]]]
    npdf.loc['11_SR', 'text_xy'] = [[[-10, 7]]]
    npdf.loc['12_SR', 'text_xy'] = [[[-12, 7]]]
    npdf.loc['02_SR', 'text_xy'] = [[[-6, 7]]]
    npdf.loc['04_SR', 'text_xy'] = [[[4, -10]]]
    npdf.loc['07_SR', 'text_xy'] = [[[-17, -12]]]
    npdf.loc['10_SR', 'text_xy'] = [[[-30, 0]]]
    _x = npdf[co.R_CENTER] * np.sin(npdf[co.TH_CENTER])
    _y = npdf[co.R_CENTER] * np.cos(npdf[co.TH_CENTER])
    npdf['lat'] = _y + co.CHC_LAT
    npdf['lon'] = _x + co.CHC_LON
    lrpdf = npdf[npdf['range'].isin(centroid_to_plot)]
    for l, r in lrpdf.iterrows():
        ax.scatter(
            r['lon'], r['lat'],
            s=40,
            c=[r['range_color']],
            marker=r['range_marker'],
            zorder=20,
            edgecolors=['k'],
            linewidth=1
        )
        ax.annotate(
            r.name,
            xy=r[['lon', 'lat']],
            xytext=r['text_xy'][0],
            textcoords='offset points',
            zorder=12,
            # backgroundcolor=[1,1,1,.2],
            # bbox=dict(boxstyle="round",
            #           alpha=0,
            #           linewidth=0,
            #           facecolor='w'
            #           ),
            alpha=.5,
            fontsize=min_fs,
            arrowprops=dict(arrowstyle='-', alpha=.5)

        )
    # ax.set_ylim(-15,15LR)
    import cartopy.mpl.geoaxes
    ax: crt.mpl.geoaxes.GeoAxesSubplot
    _xx, _yy = lon_range, lat_range
    extent = get_extent(_xx, _yy)
    ax.set_extent(extent,
                  crt.crs.PlateCarree())

    # plt.show()

    return ax


def get_extent(_xx, _yy):
    extent = [
        co.CHC_LON + _xx, co.CHC_LON - _xx,
        co.CHC_LAT + _yy, co.CHC_LAT - _yy,
    ]
    return extent


def get_topoline(zline=3900):
    import scipy.ndimage

    topo_ds = xr.open_dataset(
        '/Users/diego/flexpart_management/flexpart_management/tmp_data/etopo1_bedrock.nc')

    ax = fa.get_ax_bolivia()
    band_: xr.DataArray = topo_ds['Band1']
    band_.values = scipy.ndimage.gaussian_filter(
        band_.values,
        sigma=5,
        truncate=10
    )
    res = band_.plot.contour(levels=[0, zline], ax=ax)
    ax.figure.clear()

    segs = res.allsegs[1]
    data_ser = pd.DataFrame(segs, columns=['data'])
    data_ser['l'] = data_ser['data'].apply(lambda l: len(l))
    data_ser = data_ser.sort_values('l', ascending=False).iloc[0]['data']
    seg = data_ser.T
    return seg


def create_combined_plot(
        conc_name, dac_sum, npdf, path_colors, f_width=7.25,
        min_fs=8,
        med_fs=10
):
    seg = get_topoline(zline=3900)
    # %%
    ucp.set_dpi(300)
    f_width = f_width
    figsize = (f_width, f_width / 1.7)
    # figsize = (f_width, f_width / .6)
    f, axs = plt.subplots(
        1, 2,
        subplot_kw=dict(projection=crt.crs.PlateCarree()),
        figsize=figsize
    )
    f: plt.Figure
    lon_range = 2.2
    lat_range = 2.2
    axl = axs.flatten()
    axBO = plot_pathways(
        npdf, dac_sum, conc_name, ax=axl[0],
        lon_range=15,
        lat_range=15,
        min_fs=min_fs

    )
    axBO.plot(
        *seg, transform=crt.crs.PlateCarree(), c='k', linestyle='--',
    )
    ll = pd.DataFrame(seg.T, columns=['lo', 'la']).sort_values('la').iloc[-1]
    bbox_props = dict(boxstyle="round", fc="w", ec="none", alpha=0.5)
    axBO.annotate('$z=3.9$ km', ll.values,
                  xytext=[-30, 20],
                  textcoords='offset points',
                  zorder=12,
                  alpha=.5,
                  fontsize=min_fs,
                  arrowprops=dict(arrowstyle='->', alpha=.5),
                  bbox = bbox_props,
                  )

    import matplotlib.patches as patches
    cc = get_extent(lon_range, lat_range)
    rect = patches.Rectangle(
        [cc[1], cc[3]], 2 * lon_range, 2 * lat_range,
        zorder=10,
        facecolor='none',
        edgecolor='r',
        linestyle='-.',
        linewidth=1.5
    )
    axBO.add_patch(rect)
    # axBO.figure.show()
    axLP = plot_pathways(
        npdf, dac_sum, conc_name, lon_range=lon_range, lat_range=lat_range,
        centroid_to_plot=['MR', 'SM', 'SR'],
        chc_lp_legend=False,
        q_level=.9,
        ax_bolivia=False,
        ax=axl[1],
        min_fs=min_fs
    )
    axLP.plot(*seg, transform=crt.crs.PlateCarree(), c='k', linestyle='--')
    axLP.outline_patch.set_edgecolor('red')
    axLP.outline_patch.set_linewidth(2)
    axLP.outline_patch.set_linestyle('-.')
    axLP.annotate(
        'CHC',
        xy=[co.CHC_LON - .05, co.CHC_LAT],
        xytext=[20, 0],
        textcoords='offset points',
        zorder=30,
        # alpha = .5,
        fontsize=min_fs,
        arrowprops=dict(arrowstyle='->', alpha=1)

    )
    axLP.annotate(
        'LPB',
        xy=[co.LPB_LON, co.LPB_LAT],
        xytext=[-10, -20],
        textcoords='offset points',
        zorder=30,
        # alpha = .5,
        fontsize=min_fs,
        arrowprops=dict(arrowstyle='->', alpha=1)

    )
    axLP.set_xticks([-70, -68, -66], crs=crt.crs.PlateCarree())
    axLP.set_yticks([-16, -18], crs=crt.crs.PlateCarree())
    axLP.yaxis.set_ticks_position('right')
    axBO.set_xticks([-80, -70, -60], crs=crt.crs.PlateCarree())
    axBO.set_yticks([-10, -20, -30], crs=crt.crs.PlateCarree())
    axBO.set_ylabel(r'latitude [$\degree$]')
    axBO.set_xlabel(r'longitude [$\degree$]')
    axLP.annotate(
        'zoomed in panel',
        xy=[1, 1],
        xytext=[0, 2],
        xycoords='axes fraction',
        textcoords='offset points',
        verticalalignment='bottom',
        horizontalalignment='right',
        zorder=30,
        fontsize=min_fs,
        color='red'
    )

    add_pathways_lab(axBO, axLP, min_fs, path_colors, bbox_props)

    fa.add_ax_lab(axBO, 'a)')
    fa.add_ax_lab(axLP, 'b)')
    f.subplots_adjust(
        wspace=.05, hspace=.13,
        top=.97, bottom=.07, left=0.09,
        right=.93
    )
    axLP.figure.show()
    axBO.figure.savefig(pjoin(co.paper_fig_path, 'horizontal_clus_desc_7_25.pdf'))
    # axLP.figure.savefig('/tmp/lp.pdf')


def add_pathways_lab(axBO, axLP, min_fs, path_colors, bbox_props):
    pw_dict = {
        '03_PW': {'c': path_colors[5], 'x': -60.00, 'y': -05.00, 's': True},
        '05_PW': {'c': path_colors[2], 'x': -63.00, 'y': -30.00, 's': True},
        '07_PW': {'c': path_colors[4], 'x': -81.00, 'y': -30.50, 's': True},
        '08_PW': {'c': path_colors[1], 'x': -70.20, 'y': -16.20, 's': False},
        '11_PW': {'c': path_colors[3], 'x': -82.50, 'y': -12.00, 's': True},
        '12_PW': {'c': path_colors[0], 'x': -68.00, 'y': -14.80, 's': False},
    }

    for l, r in pw_dict.items():
        if r['s']:
            axBO.annotate(
                l, xy=[r['x'], r['y']], fontsize=min_fs,
                color=r['c'], fontweight='bold',
                bbox=bbox_props,
                zorder=50
            )
        else:
            axLP.annotate(
                l, xy=[r['x'], r['y']], fontsize=min_fs,
                color=r['c'], fontweight='bold',
                bbox=bbox_props,
                zorder=50
            )
