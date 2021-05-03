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
import shapely
from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
import geopandas

plt;


# %%


def get_ecoregions_gdf():
    shape_file = Path(co.tmp_data_path) / Path(
        'Ecoregions2017/Ecoregions2017.shp')
    # %%
    # %%
    ecoregions_df = geopandas.read_file(str(shape_file))
    # %%
    ecoregions_trimmed = ecoregions_df.cx[-90:-35, -40:0]
    return ecoregions_trimmed


# %%
def get_meow_gdf():
    shape_file = Path(co.tmp_data_path) / Path(
        'MEOW/meow_ecos.shp')

    meow_df = geopandas.read_file(str(shape_file)).cx[-90:-35, -40:0]
    return meow_df


# %%
def get_iho_gdf():
    shape_file = Path(co.tmp_data_path) / Path(
        'World_Seas_IHO_v3/World_Seas_IHO_v3.shp')

    iho_df = geopandas.read_file(str(shape_file)) \
        [['NAME', 'geometry']]
    iho_df = iho_df[iho_df['NAME'] == 'South Pacific Ocean'].copy()
    return iho_df


def RGBtoHex(vals, rgbtype=1):
    """Converts RGB values in a variety of formats to Hex values.

       @param  vals     An RGB/RGBA tuple
       @param  rgbtype  Valid valus are:
                            1 - Inputs are in the range 0 to 1
                          256 - Inputs are in the range 0 to 255

       @return A hex string in the form '#RRGGBB' or '#RRGGBBAA'
  """

    if len(vals) != 3 and len(vals) != 4:
        raise Exception(
            "RGB or RGBA inputs to RGBtoHex must have three or four elements!")
    if rgbtype != 1 and rgbtype != 256:
        raise Exception("rgbtype must be 1 or 256!")

    # Convert from 0-1 RGB/RGBA to 0-255 RGB/RGBA
    if rgbtype == 1:
        vals = [255 * x for x in vals]

    # Ensure values are rounded integers, convert to hex, and concatenate
    return '#' + ''.join(['{:02X}'.format(int(round(x))) for x in vals])


def get_extent(_xx, _yy):
    extent = [
        co.CHC_LON + _xx, co.CHC_LON - _xx,
        co.CHC_LAT + _yy, co.CHC_LAT - _yy,
        ]
    return extent


def plot_ecoregion(ax_, extent, mega1,
                   plot_box=False,
                   xticks=None,
                   yticks=None,
                   xd=-.3,
                   edgecolor='r',
                   left_lab=False,
                   right_lab=False,
                   top_lab=False,
                   botttom_lab=False,
                   red_rect_extent=None,
                   remove_label_inside_box=False,

                   ):
    if yticks is None:
        yticks = [-10, -20, -30]
    if xticks is None:
        xticks = [-80, -70, -60]
    ax = fa.get_ax_bolivia(
        lola_extent=extent,
        fig_args={'figsize': (3.125, 3.125), 'dpi': 300},
        draw_labels=False,
        map_line_alpha=.3,
        plot_cities=False,
        # chc_lp_legend=False,
        ax=ax_,
        xlab_bot=False,
        ylab_left=False,
        grid_alpha=0
    )
    lo2, lo1, la2, la1 = extent
    rec = shapely.geometry.Polygon([
        [lo1, la1],
        [lo1, la2],
        [lo2, la2],
        [lo2, la1],
        [lo1, la1]
    ])

    def _f(p):
        p1: shapely.geometry.MultiPolygon = p['geometry']
        print(p['name'])
        try:
            res = p1.intersection(rec)
        except:
            try:
                res = p1.buffer(.01)
                res = res.intersection(rec)
            except:
                res = np.nan

        return res

    mm = mega1.copy()
    mm['geometry'] = mm.apply(_f, axis=1)
    mm = mm[mm.area > 0]
    mm['rp'] = mm.representative_point()

    ax.legend().remove()
    # plt.show()
    res = mm.plot(
        ax=ax,
        color=mm['color']
    )
    if plot_box:
        add_red_box(ax, edgecolor, red_rect_extent)

    def _lab(r):
        if remove_label_inside_box:
            print('removing')
            if r["inf_index"] in [10, 21, 36, 24]:
                return 'pass'
        t = ax.annotate(
            f'•{r["inf_index"]}',
            [r['rp'].x + r['xd'], r['rp'].y + r['yd']],
            color='k', weight='medium', size=5,
            zorder=100

        )
        # t.set_bbox(dict(
        # facecolor='white', alpha=0.2, edgecolor='none'))
        return t

    mm = mm[mm.area > .5]
    mm = mm[mm['concur_area'] > .1]
    mm['xd'] = xd
    mm['yd'] = 0
    b1 = mm['inf_index'].isin([35, 38])
    mm = mm[~b1]
    mm['lab'] = mm.apply(_lab, axis=1)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    left = left_lab
    right = right_lab
    top = top_lab,
    bottom = botttom_lab
    ax.tick_params(
        labelleft=left,
        left=left,
        labelright=right,
        right=right,
        labeltop=top,
        top=top,
        labelbottom=bottom,
        bottom=bottom,
    )

    # res.set_xlim(-83,-55)
    # res.set_ylim(-32,0)


def add_red_box(ax, edgecolor, red_rect_extent):
    import matplotlib.patches as patches
    p1 = red_rect_extent[1]
    p2 = red_rect_extent[3]
    red_rect_len = red_rect_extent[0] - red_rect_extent[1]
    rect = patches.Rectangle(
        [p1, p2], red_rect_len, red_rect_len,
        zorder=10,
        facecolor='none',
        edgecolor=edgecolor,
        linestyle='-.',
        linewidth=1.5
    )
    ax.add_patch(rect)


def plot_double_ecoregions_map(extent, mega1, la_lo_ext_small):
    s = splot(1, 2, figsize=(7.25, 3.5),
              subplot_kw={'projection': crt.crs.PlateCarree()},
              dpi=300)
    ext_zoom = get_extent(la_lo_ext_small, la_lo_ext_small)
    plot_ecoregion(
        s.axf[0], extent, mega1,
        # p1=ext_zoom[1], p2=ext_zoom[3],
        edgecolor='r',
        right_lab=False,
        left_lab=True
    )
    s.axf[0].set_ylabel(r'latitude [$\degree$]')
    s.axf[0].set_xlabel(r'longitude [$\degree$]')
    ax_zoom = s.axf[1]
    plot_ecoregion(ax_zoom, ext_zoom, mega1,
                   xticks=[-70, -68, -66],
                   yticks=[-16, -18],
                   xd=+.03,
                   right_lab=True,
                   left_lab=False
                   )
    decorate_zoom_ax(ax_zoom)

    fa.add_ax_lab(s.ax[0], 'a')
    fa.add_ax_lab(s.ax[1], 'b')
    return s


def decorate_zoom_ax(ax_zoom,
                     add_chc_lpb=True,
                     zoom_lab=True,
                     ):
    ax_zoom.outline_patch.set_edgecolor('red')
    ax_zoom.outline_patch.set_linewidth(2)
    ax_zoom.outline_patch.set_linestyle('-.')
    if zoom_lab:
        ax_zoom.annotate(
            'zoomed in panel',
            xy=[1, 1.01],
            xytext=[0, 2],
            xycoords='axes fraction',
            textcoords='offset points',
            verticalalignment='bottom',
            horizontalalignment='right',
            zorder=30,
            fontsize=6,
            color='red'
        )
    if add_chc_lpb:
        ax_zoom.annotate(
            'CHC  ', [co.CHC_LON, co.CHC_LAT],
            ha='right',
            va='center',
            size=5
        )
        ax_zoom.annotate(
            'LPB  ', [co.LPB_LON, co.LPB_LAT],
            ha='right',
            va='center',
            size=5
        )


def plot_table_ecoregions(gdf18, mega1, figsize=(7.5, 4.5), min_per=5):
    _m = mega1[['inf_index', 'name', 'geometry', 'typ']]
    _m['nname'] = _m.apply(
        lambda r: f'{r["inf_index"]:2d}.{r["name"]}-{r["typ"]}',
        axis=1
    )
    _m = _m[['nname', 'geometry']]
    _g = gdf18[['geometry']].reset_index().rename({'index': 'clus_name'},
                                                  axis=1)
    # %%
    jo = geopandas.overlay(_m, _g)
    jo['area'] = jo.area
    j1 = jo[['clus_name', 'nname', 'area']]
    ju = j1.set_index(['nname', 'clus_name'])['area'].unstack()
    ju = ju / ju.sum() * 100
    ju = ju[ju > .5]
    b1 = ju.max(axis=1) >= min_per
    s = splot(figsize=figsize, dpi=300)
    sns.heatmap(ju[b1], ax=s.ax, cmap='Reds',
                annot=True, fmt='0.0f',
                linecolor=[.2, .2, .2],
                linewidths=.5,
                cbar=False,
                annot_kws={'size': 6}
                )
    s.ax.tick_params(bottom=False, top=True,
                     labeltop=True, labelbottom=False,
                     # labelrotation=45,
                     labelsize=6
                     )
    s.ax.set_xlabel(None)
    s.ax.set_ylabel(None)
    return s


def add_parameter_to_combined_gdf(all_18_pol, cropped_combined_gdf):
    cropped_combined_gdf[
        'concur_area'] = cropped_combined_gdf.geometry.intersection(
        all_18_pol).area
    cropped_combined_gdf = cropped_combined_gdf.sort_values('concur_area',
                                                            ascending=False). \
        reset_index(drop=True).reset_index()
    cropped_combined_gdf['inf_index'] = cropped_combined_gdf['index'] + 1
    # %%
    cropped_combined_gdf['rp'] = cropped_combined_gdf.representative_point()
    return cropped_combined_gdf


def get_all_18_pol(gdf18):
    _g18 = gdf18.copy()
    _g18['all'] = 1
    all18 = _g18.dissolve(by='all')
    a18 = all18.loc[1, 'geometry']
    return a18


def crop_combined_gdf(combined_gdf, rec):
    def _f(p):
        p1: shapely.geometry.MultiPolygon = p['geometry']
        print(p['name'])
        try:
            res = p1.intersection(rec)
        except:
            try:
                res = p1.buffer(.01)
                res = res.intersection(rec)
            except:
                res = np.nan

        return res

    mega1 = combined_gdf.copy()
    mega1['geometry'] = combined_gdf.apply(_f, axis=1)
    mega1 = mega1[~(mega1.area == 0)]
    mega1: geopandas.GeoDataFrame
    return mega1


def get_rec_pol(extent):
    lo2, lo1, la2, la1 = extent
    rec = shapely.geometry.Polygon([
        [lo1, la1],
        [lo1, la2],
        [lo2, la2],
        [lo2, la1],
        [lo1, la1]
    ])
    return rec


def get_combined_gdf(ext_gdf, mer_gdf, ter_gdf):
    mega = pd.concat([ter_gdf, mer_gdf, ext_gdf])
    mega = mega.reset_index(drop=True)
    # %%
    mega['id_code'] = mega.apply(lambda r: f'{r["typ"]}_{r["code"]:.0f}',
                                 axis=1)
    mega: geopandas.GeoDataFrame
    return mega


def get_extra_gdf(lake_pol, pacific_ocean_pol):
    ex = {
        0: {
            'name'    : 'Lake Titicaca',
            'code'    : 1,
            'geometry': lake_pol,
            'color'   : 'lavender'
        },
        1: {
            'name'    : 'South Pacific Ocean',
            'code'    : 2,
            'geometry': pacific_ocean_pol,
            'color'   : 'lavender'
        },
    }
    ex = pd.DataFrame(ex).T
    ex = geopandas.GeoDataFrame(ex)
    ex['typ'] = 'EXT'
    return ex


def get_ecoregion_gdf(ecoregions_trimmed):
    e1 = ecoregions_trimmed[
        ['ECO_NAME', 'ECO_ID', 'geometry', 'COLOR']
    ]
    e1 = e1.rename({
        'ECO_ID'  : 'code',
        'ECO_NAME': 'name',
        'COLOR'   : 'color'
    }, axis=1)
    e1['typ'] = 'TER'
    return e1


def get_mer_gdf(meow, all_eco):
    le = len(meow)
    cols = sns.color_palette('PuBu', le)
    cols = [RGBtoHex(c) for c in cols]
    cols = pd.Series(cols)
    cols = cols.sample(frac=1, random_state=123) \
        .reset_index(drop=True)
    # %%
    m1 = meow[['ECO_CODE', 'ECOREGION', 'geometry']]
    m1 = m1.rename({'ECO_CODE': 'code', 'ECOREGION': 'name'}, axis=1)
    m1['typ'] = 'MER'
    m1['geometry'] = m1['geometry'].apply(lambda x: x.difference(all_eco))
    m1 = m1.reset_index(drop=True)
    m1['color'] = cols
    return m1


def get_lake_pol(all_eco):
    square_lake = shapely.geometry.Polygon([
        [-71, -15],
        [-68, -15],
        [-68, -17],
        [-71, -17],
        [-71, -15]
    ])
    lake = square_lake.difference(all_eco)
    return lake


def get_pacific_ocean_pol(iho, all_meow):
    po = iho['geometry'].iloc[0]
    # %%
    # all_meow: shapely.geometry.MultiPolygon
    # po: shapely.geometry.MultiPolygon
    # %%
    pacific_ocean = po.difference(all_meow)
    return pacific_ocean


def get_all_eco(ecoregions_trimmed):
    all_eco = ecoregions_trimmed
    all_eco['all'] = 1
    all_eco = all_eco.dissolve(by='all')
    ae = all_eco.loc[1, 'geometry']
    return ae


def get_all_meow(meow):
    meow['all'] = 1
    all_meow = meow.dissolve(by='all')[['geometry']]
    am = all_meow.loc[1, 'geometry']
    return am


def plot_pathways(geo_df,
                  lon_range=15,
                  lat_range=13,
                  centroid_to_plot=None,
                  chc_lp_legend=False,
                  ax_bolivia=True,
                  ax=None,
                  min_font_size=5,
                  labs_to_plot='all',
                  background_alpha=0
                  ):
    npdf = geo_df
    if centroid_to_plot is None:
        centroid_to_plot = ['LR', 'MR']
    if ax is None:
        ucp.set_dpi(300)
        f_width = 7.25
        figsize = (f_width, f_width / 1.6)
        _, ax = plt.subplots(
            subplot_kw=dict(projection=crt.crs.PlateCarree()),
            figsize=figsize
        )
    ax: plt.Axes
    if ax_bolivia:
        fa.get_ax_bolivia(
            ax=ax,
            plot_cities=False,
            map_res='50m',
            lake_face_color='none',
            map_line_alpha=.5,
            chc_lp_legend=chc_lp_legend,
            grid_alpha=0,
            draw_labels=False,
            xlab_top=False,
            xlab_bot=False,
            ylab_left=False,
            ylab_right=False,
        )
    else:
        fa.get_ax_lapaz(
            ax=ax, plot_cities=False, lake_face_color='none',
            map_line_alpha=.5, chc_lp_legend=chc_lp_legend,
            grid_alpha=0,
            draw_labels=False,
            y_left_lab=False
        )

    npdf['text_xy'] = [[[0, 0]]] * len(npdf)
    npdf.loc['07_LR', 'text_xy'] = [[[-5, -12]]]
    npdf.loc['08_LR', 'text_xy'] = [[[-5, 7]]]
    npdf.loc['10_LR', 'text_xy'] = [[[8, 0]]]
    npdf.loc['11_MR', 'text_xy'] = [[[-13, 7]]]
    npdf.loc['02_MR', 'text_xy'] = [[[-10, 7]]]
    npdf.loc['04_MR', 'text_xy'] = [[[-10, 7]]]
    npdf.loc['05_MR', 'text_xy'] = [[[5, 0]]]
    npdf.loc['09_MR', 'text_xy'] = [[[-25, -8]]]
    npdf.loc['08_SM', 'text_xy'] = [[[-25, -10]]]
    npdf.loc['12_SM', 'text_xy'] = [[[-3, 7]]]
    npdf.loc['03_SM', 'text_xy'] = [[[5, -4]]]
    npdf.loc['06_SM', 'text_xy'] = [[[-7, -10]]]
    npdf.loc['11_SR', 'text_xy'] = [[[-10, 7]]]
    npdf.loc['02_SR', 'text_xy'] = [[[-3, 7]]]
    npdf.loc['12_SR', 'text_xy'] = [[[-12, 7]]]
    npdf.loc['04_SR', 'text_xy'] = [[[4, -10]]]
    npdf.loc['07_SR', 'text_xy'] = [[[-17, -12]]]
    npdf.loc['10_SR', 'text_xy'] = [[[-10, 5]]]
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

    if labs_to_plot == 'all':
        lab_lrpdf = lrpdf
    else:
        lab_lrpdf = npdf[npdf['range'].isin(labs_to_plot)]

    for l, r in lab_lrpdf.iterrows():
        ax.annotate(
            r.name,
            xy=r[['lon', 'lat']],
            xytext=r['text_xy'][0],
            textcoords='offset points',
            zorder=12,
            backgroundcolor=[1, 1, 1, background_alpha],
            # bbox=dict(boxstyle="round",
            #           alpha=0,
            #           linewidth=0,
            #           facecolor='w'
            #           ),
            alpha=.5,
            fontsize=min_font_size,
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


def add_centroids_and_range(gdf18):
    # %%
    cen18_df = pd.read_csv(
        pjoin(co.tmp_data_path, 'centroid_18_v3.csv'), index_col=0)
    cen6_df = pd.read_csv(
        pjoin(co.tmp_data_path, 'centroid_6_v3.csv'), index_col=0)
    gdf18 = pd.merge(gdf18, cen18_df, left_index=True, right_index=True)
    gdf18['range'] = co.DIC_186.set_index('18_NC')['range']

    rc = co.range_colors_ser.to_frame('range_color')
    gdf18 = pd.merge(gdf18, rc, left_on='range', right_index=True)

    rc = co.range_markers_ser.to_frame('range_marker')
    gdf18 = pd.merge(gdf18, rc, left_on='range', right_index=True)

    return gdf18


def plot_altiplano_line(axBO, min_fs, annotate=True, topoline=None):
    alt_style = dict(
        transform=crt.crs.PlateCarree(),
        c='brown', linestyle='-', alpha=.3,
        linewidth=1
    )
    if topoline is None:
        seg = get_topoline(zline=3900)
    else:
        seg = topoline

    axBO.plot(
        *seg, **alt_style
    )
    ll = pd.DataFrame(seg.T, columns=['lo', 'la']).sort_values('la').iloc[-1]
    bbox_props = dict(boxstyle="round", fc="w", ec="none", alpha=.9)
    if annotate:
        axBO.annotate('$z=3.9$ km', ll.values,
                      xytext=[-30, 20],
                      textcoords='offset points',
                      zorder=12,
                      alpha=.5,
                      fontsize=min_fs,
                      arrowprops=dict(arrowstyle='->', alpha=.5),
                      bbox=bbox_props,
                      )


def get_topoline(zline=3900):
    import scipy.ndimage

    topo_ds = xr.open_dataset(
        pjoin(co.tmp_data_path, 'etopo1_bedrock.nc'))

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


def plot_label_ecoregion(ax, cropped_combined_gdf, xstarts=None):
    if xstarts is None:
        xstarts = [0, .3, .55, .85]
    df = cropped_combined_gdf[[
        'inf_index',
        'typ',
        'name',
        'color'
    ]][:37]
    dfs = [df[0:10], df[10:20], df[20:30], df[30:]]
    # xstarts = xstarts
    rlen = 10
    xs = xstarts[0]
    df = dfs[0]

    def plot_col(ax, df, rlen, xs):
        for l, (la, r) in enumerate(df.iterrows()):
            size = 5
            bbox = dict(
                alpha=1, linewidth=0, facecolor=r['color'],
                boxstyle='square,pad=0'
            )
            ax.annotate(
                f'   ', (xs, rlen - l),
                bbox=bbox,
                size=size,
                va='center'
            )

            ax.annotate(
                f'   {r["inf_index"]:3d}. '
                f'{r["name"]}-{r["typ"]}',
                (xs, rlen - l),
                size=size,
                va='center'

            )

    for xs, df in zip(xstarts, dfs):
        plot_col(ax, df, rlen, xs)
    ax.set_ylim(0, rlen)
    ax.axis('off')

class FigLayout:
    def __init__(self,
                 combined_gdf: geopandas.GeoDataFrame,
                 topoline,
                 gdf18
                 ):
        self.combined_gdf = combined_gdf
        self.topoline = topoline
        self.gdf18 = gdf18

        self.size_x = 7.25
        self.size_y = self.size_x
        self.f: plt.Figure = plt.figure(
            figsize=(self.size_x, self.size_y), dpi=300)

        h_ratios = [2, 2, .6]
        self.grid = self.f.add_gridspec(3, 2,
                                        height_ratios=h_ratios)

        self.proj = crt.crs.PlateCarree()
        self.axA = self.f.add_subplot(self.grid[0, 0], projection=self.proj)
        self.axB = self.f.add_subplot(self.grid[0, 1], projection=self.proj)
        self.axC = self.f.add_subplot(self.grid[1, 0], projection=self.proj)
        self.axD = self.f.add_subplot(self.grid[1, 1], projection=self.proj)
        self.axE = self.f.add_subplot(self.grid[2, :])

        self.xlab = r'longitude [$\degree$]'
        self.ylab = r'latitude [$\degree$]'

        self.big_xticks = [-80, -70, -60]
        self.big_yticks = [-10, -20, -30]
        self.small_xticks = [-69, -67]
        self.small_yticks = [-16, -18]

        self.la_lo_ext_big = 15
        self.la_lo_ext_small = 2.2
        self.ext_small = get_extent(self.la_lo_ext_small,
                                    self.la_lo_ext_small)
        self.ext_big = get_extent(self.la_lo_ext_big, self.la_lo_ext_big)

        self.plot_axA()
        self.plot_axB()
        self.plot_axC()
        self.plot_axD()
        self.plot_axE()

        fa.add_ax_lab(self.axA, 'a')
        fa.add_ax_lab(self.axB, 'b')
        fa.add_ax_lab(self.axC, 'c')
        fa.add_ax_lab(self.axD, 'd')

        self.f.subplots_adjust(left=.1, right=.9,
                               bottom=.0, top=.95,
                               hspace=.1, wspace=.005)


        # fa.add_ax_lab(self.axE, 'e')

    def plot_axE(self):
        plot_label_ecoregion(
            self.axE,
            self.combined_gdf,
            xstarts=[0, .3, .58, .85]
        )

    def plot_axA(self):
        ax = self.axA
        plot_pathways(
            geo_df=self.gdf18,
            ax=ax,
            lon_range=self.la_lo_ext_big,
            lat_range=self.la_lo_ext_big,
            labs_to_plot=['LR', 'MR'],
            centroid_to_plot=['SR', 'MR', 'SM', 'LR']
        )
        plot_pols(ax,self.gdf18)

        plot_altiplano_line(axBO=ax, min_fs=5, annotate=True,
                            topoline=self.topoline)
        add_red_box(ax=ax, edgecolor='red',
                    red_rect_extent=self.ext_small)
        ax.set_yticks(self.big_yticks)
        ax.set_xticks(self.big_xticks)
        ax.tick_params(
            top=True,
            labeltop=True,
            bottom=False,
            labelbottom=False,
            labelsize=8
        )
        ax: plt.Axes
        ax.set_xlabel(self.xlab, size=8)
        ax.xaxis.set_label_position('top')
        ax.set_ylabel(self.ylab, size=8)

        # plt.Axes.tick_params()

    def plot_axB(self):
        import cartopy.mpl.geoaxes
        ax: cartopy.mpl.geoaxes.GeoAxesSubplot = self.axB
        plot_pathways(geo_df=self.gdf18, ax=ax,
                      lon_range=self.la_lo_ext_small,
                      lat_range=self.la_lo_ext_small,
                      centroid_to_plot=['SR', 'SM']
                      )
        plot_pols(ax,self.gdf18)

        plot_altiplano_line(
            axBO=ax, min_fs=5, annotate=False,
            topoline=self.topoline)
        decorate_zoom_ax(ax, add_chc_lpb=False,
                         zoom_lab=False)

        ax.annotate(
            'CHC',
            xy=[co.CHC_LON - .05, co.CHC_LAT],
            xytext=[20, 0],
            textcoords='offset points',
            zorder=30,
            # alpha = .5,
            fontsize=5,
            arrowprops=dict(arrowstyle='->', alpha=1)

        )
        ax.annotate(
            'LPB',
            xy=[co.LPB_LON, co.LPB_LAT],
            xytext=[-10, -20],
            textcoords='offset points',
            zorder=30,
            # alpha = .5,
            fontsize=5,
            arrowprops=dict(arrowstyle='->', alpha=1)

        )
        ax.set_yticks(self.small_yticks)
        ax.set_xticks(self.small_xticks)
        ax.tick_params(
            top=True,
            labeltop=True,
            bottom=False,
            labelbottom=False,
            right=True,
            labelright=True,
            left=False,
            labelleft=False,
            labelsize=8
        )

    def plot_axC(self):
        ax = self.axC
        plot_ecoregion(
            ax,
            self.ext_big,
            self.combined_gdf,
            xticks=self.big_xticks,
            yticks=self.big_yticks,
            xd=-.3,
            right_lab=False,
            left_lab=True,
            botttom_lab=False,
            top_lab=False,
            red_rect_extent=self.ext_small,
            plot_box=True,
            remove_label_inside_box=True,
        )
        # self.axC:plt.Axes
        ax.set_xticklabels([])
        ax.tick_params(
            labelsize=8
        )

    def plot_axD(self):
        ax = self.axD
        plot_ecoregion(
            ax,
            self.ext_small,
            self.combined_gdf,
            xticks=self.small_xticks,
            yticks=self.small_yticks,
            xd=-.05,
            right_lab=True,
            left_lab=False,
            # red_rect_len=self.la_lo_ext_small
        )
        decorate_zoom_ax(ax_zoom=ax)
        ax.set_xticklabels([])
        ax.tick_params(
            labelsize=8
        )
        ax.plot(*co.lola_la_paz_pol.T, zorder=2,
                linewidth=.5,
                color='k',
                alpha=.2
                )
        # plot_pols(ax,self.gdf18)

    def add_index(self):
        pass

def plot_pols(ax, gdf18):
    for l, r in gdf18.iterrows():
        _g = gdf18.loc[[l]]
        _g.plot(
            ax=ax,
            facecolor=_g['range_color'],
            edgecolor=_g['range_color'],
            alpha=.1,
            hatch=_g['hatch'].item(),
            rasterized=True
        )
        # _g.plot(
        #     ax=ax,
        #     color='None',
        #     edgecolor=_g['range_color'],
        #     alpha=.1,
        #     hatch=_g['hatch'].item()
        # )

def add_hatch(gdf18):
    hs = [
        '////',
        '\\\\\\\\',
        '----',
        '||||',
        'xxxx',
        '....',
        '////',
        '\\\\\\\\',
        '----',
        '||||',
        'xxxx',
        '....',
        '////',
        '\\\\\\\\',
        '----',
        '||||',
        'xxxx',
        '....',
    ]
    gdf18['hatch'] = hs
    gdf18.loc['02_MR', 'hatch'] = '....'
    return gdf18
