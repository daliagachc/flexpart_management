# project name: wrf-flexpart-chc
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
# %%

from useful_scit.imps import *

# import constants as co
# from wrf_flexpart_figures.util import map_add_rectangle

import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co
from matplotlib.colors import Normalize

# %%

data_path = '/Users/diego/flexpart_management/flexpart_management/notebooks/paper_map_figure/data'
topo_path = os.path.join(data_path,'etopo1_bedrock.nc')


def map_figure():
    # %%

    PROJ = ccrs.PlateCarree()
    ucp.set_dpi(300)
    f_width = 7.25
    fig = plt.figure(
        figsize=(f_width, f_width / 1.6),
                     )

    ncmap = get_terrain_cmap()

    ax1, ax2, ax3, ax4, cax = create_axes(PROJ, fig)

    xb1 = -93
    xb2 = xb1+60
    yb1 = -35
    yb2 = yb1 + (xb2 - xb1) / 1.5
    lola_extent = [xb1, xb2, yb1, yb2]
    grid_style = ':'
    # lola_extent = [-95, -40, -35, 5]
    lo_len = lola_extent[1] - lola_extent[0]
    la_len = lola_extent[3] - lola_extent[2]
    lo_over_la = lo_len / la_len
    lolo = np.arange(-100, -20, 10)
    lala = np.arange(-50, 20, 10)
    white_grid_color = (.9,.9,.9)

    bar_legend = 'km asl'
    levels = [0,1.5, 3, 4.5, 6, 7.5]
    lon_large_ticks = [-80, -60, -40]
    lat_large_ticks = [-20, 0]
    dark_grid_color = (.5,.5,.5)
    tab10 = plt.get_cmap('tab10')

    ys1 = -17.4
    ys2 = -15.4
    xs1 = -69.6
    xs2 = xs1 + (ys2 - ys1) * lo_over_la
    lolo_lp = np.arange(-70.5, -65, .5)
    lala_lp = np.arange(-18.5, -14, .5)

    topo_ds = xr.open_dataset(topo_path)

    plot_bolivia_elevation(PROJ, ax2, bar_legend, grid_style, lala, levels,
                           lola_extent, lolo, lon_large_ticks, ncmap, topo_ds,
                           white_grid_color)

    plot_bolivia_domains(PROJ, ax1, dark_grid_color, grid_style, lala,
                         lat_large_ticks, lola_extent, lolo, lon_large_ticks)

    plot_lapaz_domains(PROJ, ax3, dark_grid_color, grid_style, lala_lp, lolo_lp,
                       tab10, xs1, xs2, ys1, ys2)

    mappable = plot_lapaz_elevation(PROJ, ax4, bar_legend, grid_style, lala_lp,
                                    levels, lolo_lp, ncmap, tab10, topo_ds,
                                    white_grid_color, xs1, xs2, ys1, ys2)


    plot_elevation_bar(bar_legend, cax, fig, mappable)

    add_indices(ax1, ax2, ax3, ax4)

    fig:plt.Figure
    plt.show()
    fig.savefig(os.path.join(co.paper_fig_path,'map_dom_7_25.pdf'))

    # %%

    # %%


def add_indices(ax1, ax2, ax3, ax4):
    axs = [ax1, ax2, ax3, ax4]
    texts = ['a)', 'b)', 'c)', 'd)']
    for ax, text in zip(axs, texts):
        fa.add_ax_lab(ax, text)


def get_terrain_cmap():
    cmap = plt.get_cmap('terrain')
    colors = cmap(np.linspace(.22, 1, cmap.N))
    ncmap = mpl.colors.LinearSegmentedColormap.from_list('cut_terrain', colors)
    ncmap.set_under(crt.feature.COLORS['water'])
    return ncmap


# noinspection PyUnusedLocal
def plot_elevation_bar(bar_legend, cax, fig, mappable):
    cbar = fig.colorbar(mappable, cax=cax)
    # cbar.set_label(bar_legend)
    cax:plt.Axes
    # cax.set_title(bar_legend,loc='left')
    cax.annotate(bar_legend,
                (0, 1),
                (0, 2),
                xycoords='axes fraction',
                textcoords='offset points',
                horizontalalignment='left',
                verticalalignment='bottom',
                # color=ucp.cc[3]
                )

    # plt.tight_layout()



def plot_lapaz_elevation(PROJ, ax4, bar_legend, grid_style, lala_lp, levels,
                         lolo_lp, ncmap, tab10, topo_ds, white_grid_color, xs1,
                         xs2, ys1, ys2):
    ax = ax4
    fa.get_ax_lapaz(ax=ax, chc_lp_legend=False,
                    plot_cities=False,
                    lalo_extent=[xs1, xs2, ys1, ys2],
                    lola_ticks=[lolo_lp, lala_lp],
                    draw_labels=False,
                    grid_alpha=1,
                    grid_color=white_grid_color,
                    grid_style=grid_style,
                    lake_face_color=crt.feature.COLORS['water']
                    )
    ax.set_xticks([-69, -68, -67], crs=PROJ)
    slice_ = {'lat': slice(ys1, ys2, ), 'lon': slice(xs1, xs2, )}
    band_ = topo_ds['Band1'].loc[slice_] / 1000
    band_.name = bar_legend
    mappable = band_.plot(
        cmap=ncmap,
        ax=ax,
        levels=levels,
        subplot_kws={'transform': PROJ},
        # center=2000,
        norm=Normalize(0, 5),
        add_colorbar=False,
        rasterized=True

    )
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.scatter([co.CHC_LON], [co.CHC_LAT], facecolors='none',
               edgecolors=tab10(0))
    ax.scatter([co.LPB_LON], [co.LPB_LAT], facecolors='none',
               edgecolors=tab10(1))
    return mappable


def plot_lapaz_domains(PROJ, ax3, dark_grid_color, grid_style, lala_lp, lolo_lp,
                       tab10, xs1, xs2, ys1, ys2):
    ax = ax3
    fa.get_ax_lapaz(ax=ax, chc_lp_legend=False,
                    plot_cities=False,
                    lalo_extent=[xs1, xs2, ys1, ys2],
                    lola_ticks=[lolo_lp, lala_lp],
                    draw_labels=False,
                    grid_style=grid_style,
                    grid_color=dark_grid_color,
                    grid_alpha=1
                    )
    # noinspection PyArgumentList
    ax.set_xticks([-69, -68, -67], crs=PROJ)
    ax.set_xlabel(r'longitude [$\degree$]')
    # noinspection PyArgumentList
    ax.set_yticks([-16, -17], crs=PROJ)
    ax:plt.Axes
    ax.set_ylabel(r'latitude [$\degree$]')
    # ax.set_ylabel('abc', rotation=0, fontsize=20, labelpad=20)
    # ax.annotate('latitude',
    #             (0, 1),
    #             (-2, -2),
    #             xycoords='axes fraction',
    #             textcoords='offset points',
    #             horizontalalignment='right',
    #             verticalalignment='top',
    #             # color=ucp.cc[3]
    #             )

    x1, x2, y1, y2 = -69, -67.3, -17.2, -15.6
    map_add_rectangle(ax, x1, x2, y1, y2, color=ucp.cc[3])
    # noinspection PyProtectedMember
    ax.annotate('D04',
                (x1, y1),
                (0, -2),
                xycoords=PROJ._as_mpl_transform(ax),
                textcoords='offset points',
                horizontalalignment='left',
                verticalalignment='top',
                color=ucp.cc[3]
                )
    ax.scatter([co.CHC_LON], [co.CHC_LAT], facecolor=tab10(0))
    ax.scatter([co.LPB_LON], [co.LPB_LAT], facecolor=tab10(1))
    # noinspection PyProtectedMember
    ax.annotate('CHC', [co.CHC_LON, co.CHC_LAT], xytext=[1, 2],
                xycoords=PROJ._as_mpl_transform(ax),
                textcoords='offset points',
                horizontalalignment='right',
                verticalalignment='bottom',
                )
    # noinspection PyProtectedMember
    ax.annotate('LPB', [co.LPB_LON, co.LPB_LAT], xytext=[0, -3],
                xycoords=PROJ._as_mpl_transform(ax),
                textcoords='offset points',
                horizontalalignment='right',
                verticalalignment='top',
                )
    ax: plt.Axes
    # noinspection PyProtectedMember
    ax.annotate('Lake TCC',
                [-69, -16],
                xytext=[2, 4],
                xycoords=PROJ._as_mpl_transform(ax),
                textcoords='offset points',
                horizontalalignment='left',
                verticalalignment='bottom',
                color=crt.feature.COLORS['water']
                )


def add_doms_bolivia(PROJ, ax1):
    x1, x2, y1, y2 = -89.4, -43.2, -0.5, -32.2
    ax = ax1
    map_add_rectangle(ax, x1, x2, y1, y2, color=ucp.cc[0])
    # noinspection PyProtectedMember
    ax.annotate('D01',
                (x1, y1),
                (0, 2),
                xycoords=PROJ._as_mpl_transform(ax),
                textcoords='offset points',
                horizontalalignment='left',
                color=ucp.cc[0]
                )
    x1, x2, y1, y2 = -78.7, -53.9, -26.3, -7.2
    ax = ax1
    map_add_rectangle(ax, x1, x2, y1, y2, color=ucp.cc[1])
    # noinspection PyProtectedMember
    ax.annotate('D02',
                (x2, y2),
                (0, 2),
                xycoords=PROJ._as_mpl_transform(ax),
                textcoords='offset points',
                horizontalalignment='right',
                color=ucp.cc[1]
                )
    x1, x2, y1, y2 = -70.9, -62.0, -20.5, -13.9
    ax = ax1
    map_add_rectangle(ax, x1, x2, y1, y2, color=ucp.cc[2])
    # noinspection PyProtectedMember
    ax.annotate('D03',
                (x1, y1),
                (-2, 0),
                xycoords=PROJ._as_mpl_transform(ax),
                textcoords='offset points',
                horizontalalignment='right',
                verticalalignment='top',
                color=ucp.cc[2]
                )
    x1, x2, y1, y2 = -69, -67.3, -17.2, -15.6
    ax = ax1
    map_add_rectangle(ax, x1, x2, y1, y2, color=ucp.cc[3])


# noinspection PyTypeChecker
def plot_bolivia_domains(PROJ, ax1, dark_grid_color, grid_style, lala,
                         lat_large_ticks, lola_extent, lolo, lon_large_ticks):
    ax = fa.get_ax_bolivia(ax=ax1, chc_lp_legend=False,
                           lola_extent=lola_extent,
                           plot_cities=False,
                           lola_ticks=[lolo, lala],
                           draw_labels=False,
                           grid_style=grid_style,
                           grid_color=dark_grid_color,
                           grid_alpha=1,
                           map_res='110m'
                           )
    ax.set_yticks(lat_large_ticks, crs=PROJ)
    ax.set_ylabel(None)
    ax.set_xticks(lon_large_ticks, crs=PROJ)
    ax.set_xlabel(None)
    add_doms_bolivia(PROJ, ax1)


# noinspection PyTypeChecker
def plot_bolivia_elevation(PROJ, ax2, bar_legend, grid_style, lala, levels,
                           lola_extent, lolo, lon_large_ticks, ncmap, topo_ds,
                           white_grid_color):
    ax = fa.get_ax_bolivia(
        chc_lp_legend=False, ax=ax2, plot_cities=False,
        lola_extent=lola_extent,
        plot_ocean=True,
        lola_ticks=[lolo, lala],
        draw_labels=False,
        grid_style=grid_style,
        grid_color=white_grid_color,
        grid_alpha=1,
        map_res='110m'
    )
    # ax.set_yticks([-20,0],crs=ccrs.PlateCarree())
    ax.set_ylabel(None)
    ax.set_xticks(lon_large_ticks, crs=PROJ)
    ax.set_xlabel(None)
    slice_ = {'lat': slice(None, None, 10), 'lon': slice(None, None, 10)}
    band_ = topo_ds['Band1'][slice_] / 1000
    band_ = band_.where(band_ > 0)
    band_.name = bar_legend
    band_.plot(
        cmap=ncmap,
        ax=ax,
        levels=levels,
        subplot_kws={'transform': PROJ},
        # center=2000,
        norm=Normalize(0, 5, clip=False),
        add_colorbar=False,
        rasterized=True
    )
    ax.set_xlabel(None)
    ax.set_ylabel(None)


def create_axes(PROJ, fig):
    f_len = .37
    f_left_mar = .1
    v_mid_mar = .02
    v_mid = f_left_mar + f_len + v_mid_mar
    f_bot_mar = .1
    h_mid_mar = .1
    h_mid = f_bot_mar + f_len + h_mid_mar
    ax1 = fig.add_axes([f_left_mar, h_mid, f_len, f_len], projection=PROJ)
    ax2 = fig.add_axes([v_mid, h_mid, f_len, f_len], projection=PROJ)
    ax3 = fig.add_axes([f_left_mar, f_bot_mar, f_len, f_len], projection=PROJ)
    ax4 = fig.add_axes([v_mid, f_bot_mar, f_len, f_len], projection=PROJ)
    # cax = fig.add_axes([v_mid + f_len + v_mid_mar, h_mid, .015, f_len])
    cax = fig.add_axes([v_mid + v_mid_mar + f_len, h_mid , .015, f_len*.9])
    return ax1, ax2, ax3, ax4, cax


import urllib.request
from http.cookiejar import CookieJar

from cartopy import crs as ccrs


def login_nasa():
    username = 'daliaga1'
    passwd = '22711253Ed'
    # The user credentials that will be used to authenticate access to the data
    # The url of the file we wish to retrieve
    # url = "http://e4ftl01.cr.usgs.gov/MOLA/MYD17A3H.006/2009.01.01/MYD17A3H.A2009001.h12v05.006.2015198130546.hdf.xml"
    # Create a password manager to deal with the 401 reponse that is returned from
    # Earthdata Login
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, "https://urs.earthdata.nasa.gov",
                                  username, passwd)
    # Create a cookie jar for storing cookies. This is used to store and return
    # the session cookie given to use by the data server (otherwise it will just
    # keep sending us back to Earthdata Login to authenticate).  Ideally, we
    # should use a file based cookie jar to preserve cookies between runs. This
    # will make it much more efficient.
    cookie_jar = CookieJar()
    # Install all the handlers.
    opener = urllib.request.build_opener(
        urllib.request.HTTPBasicAuthHandler(password_manager),
        # urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
        # urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
        urllib.request.HTTPCookieProcessor(cookie_jar))
    urllib.request.install_opener(opener)
    # %%
    # url = 'https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL3.003/2000.02.11/N47E014.SRTMGL3.hgt.zip'
    # Create and submit the request. There are a wide range of exceptions that
    # can be thrown here, including HTTPError and URLError. These should be
    # caught and handled.
    # request = urllib.request.Request(url)
    # response = urllib.request.urlopen(request)
    # Print out the result (not a good idea with binary data!)
    # body = response.read()
    # print(body)


def map_add_rectangle(ax, x1, x2, y1, y2, color='k'):
    ax.plot([x2, x2, x1, x1, x2], [y1, y2, y2, y1, y1],
            transform=ccrs.PlateCarree(), color=color)

# %%




# %%



map_figure()
