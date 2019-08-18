# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import matplotlib
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.patches import Polygon
from useful_scit.imps import *
from typing import List
import cartopy
import area
from flexpart_management.modules.constants import *
from useful_scit.util.zarray import compressed_netcdf_save


def import_flex_file(path_file: str):
    ds = xr.open_dataset(path_file)
    return ds


def import_flex_head_file(path_file: str):
    ds = xr.open_dataset(path_file)
    return ds


def get_head_file_from_path(path: str, dom: str = 'd01'):
    pat = os.path.join(path, 'head*' + dom + '*')
    file_list = glob.glob(pat)
    file = file_list[0]
    return file


def import_head_ds(path: str, dom: str) -> xr.Dataset:
    file_path = get_head_file_from_path(path, dom)
    print(file_path)
    head_ds = import_flex_head_file(file_path)
    return head_ds


def convert_ds_time_format(ds: xr.Dataset, var='Times') -> xr.Dataset:
    time_str_sr: pd.Series = ds[[var]].to_dataframe()[var].str.decode('UTF8')
    ts = pd.to_datetime(time_str_sr, format='%Y%m%d_%H%M%S')
    n_ds = ds.copy()
    n_ds[var] = ts
    n_ds = n_ds.assign_coords(Time=n_ds.Times)
    n_ds = n_ds.drop('Times')
    return n_ds


def import_file_ds_list(file_path: str, dom: str) -> List[xr.Dataset]:
    pat = os.path.join(file_path, 'flxout*' + dom + '*')
    file_list = glob.glob(pat)
    file_list.sort()
    ds_list = []
    for f in file_list:
        ds = import_flex_file(f)
        ds = convert_ds_time_format(ds)
        ds_list.append(ds)
    return ds_list


def concat_file_ds_list(ds_list: List[xr.Dataset]):
    ds_con = xr.concat(ds_list, dim='Time')
    return ds_con


# we might not need this function anymore
def decode_bstr(bstr: bytes):
    return bstr.decode('UTF8')


# we might not need this function anymore
def flx_time_to_ts(bstr: bytes):
    flx_time_str = decode_bstr(bstr)
    ts = pd.to_datetime(flx_time_str, format='%Y%m%d_%H%M%S')
    return ts


def join_head(ds_flx: xr.Dataset, ds_head: xr.Dataset, ageclass=slice(0, None), releases=slice(0, None)) -> xr.Dataset:
    new_ds = ds_flx.copy()
    vars2keep = ['TOPOGRAPHY', 'GRIDAREA', 'ZTOP']
    for v in vars2keep:
        new_ds[v] = ds_head[v]
    new_ds = new_ds.isel(ageclass=ageclass, releases=releases)
    new_ds = new_ds.assign_attrs(ds_head.attrs)
    release_start_times = get_releases_start_time(ds_head)
    new_ds = new_ds.assign_coords(**{RL: release_start_times})

    return new_ds


def get_release_start_date(ds_head: xr.Dataset):
    # todo: warning this only works if there is 1 release
    sim_start_date = ds_head.SIMULATION_START_DATE
    sim_start_time = ds_head.SIMULATION_START_TIME
    start_datetime_str = '{0:08d}_{1:06d}'.format(sim_start_date, sim_start_time)
    start_datetime = pd.to_datetime(start_datetime_str, format='%Y%m%d_%H%M%S')
    release_sec = round(int(ds_head.ReleaseTstart_end.isel(releases=0)[0]), -1)
    release_start_date = start_datetime + pd.Timedelta(release_sec, unit='S')
    return release_start_date


def get_releases_start_time(ds_head: xr.Dataset):
    sim_start_dt = '{:08d}'.format(ds_head.SIMULATION_START_DATE) + ' ' + \
                   '{0:06d}'.format(ds_head.SIMULATION_START_TIME)
    sim_start_dt = dt.datetime.strptime(sim_start_dt, '%Y%m%d %H%M%S')
    start_deltas = ds_head.ReleaseTstart_end.values[:, 0].round(-1)

    rel_start = [sim_start_dt + dt.timedelta(seconds=float(s)) for s in start_deltas]
    start_times = pd.to_datetime(rel_start)

    return start_times


def add_release_time_dim(ds_join, ds_head):
    ds_new = ds_join.copy()
    vars_to_add_dim = ['CONC']
    dim_name = 'arrival_time'
    for v in vars_to_add_dim:
        dd = ds_new[v]
        dd = xr.concat([dd], dim_name)
        ds_new[v] = dd
    ts = get_release_start_date(ds_head)
    ds_new = ds_new.assign_coords(release_time=[ts])
    return ds_new


def assign_vars_to_cords(ds_join):
    new_ds = ds_join.copy()
    vars_to_assign = ['ZTOP', 'GRIDAREA', 'TOPOGRAPHY']
    for v in vars_to_assign:
        new_ds = new_ds.assign_coords(**{v: new_ds[v]})
    return new_ds


def add_lat_lot(ds: xr.Dataset):
    ds_new = ds.copy()
    lat = ds_new.XLAT.mean(dim='west_east')
    lon = ds_new.XLONG.mean(dim='south_north')
    ds_new = ds_new.assign_coords(**{LAT: lat, LON: lon})
    return ds_new


def add_zmid(ds: xr.Dataset):
    zl = list(ds.ZTOP.values)
    zl.reverse()
    zl.append(0)
    zl.reverse()
    zm = []
    for i in range(len(zl) - 1):
        zm.append((zl[i] + zl[i + 1]) / 2)
    zmid = ds.ZTOP.copy()
    zmid.values = zm
    zname = 'ZMID'
    zmid.name = zname
    new_ds = ds.assign_coords(**{zname: zmid})
    return new_ds


def add_zbot(ds: xr.Dataset):
    zl = list(ds[ZT].values)
    zl.reverse()
    zl.append(0)
    zl.reverse()
    zm = []
    for i in range(len(zl) - 1):
        zm.append((zl[i]))
    zmid = ds.ZTOP.copy()
    zmid.values = zm
    zname = ZB
    zmid.name = zname
    new_ds = ds.assign_coords(**{zname: zmid})
    return new_ds


def add_zlength_m(ds: xr.Dataset):
    zl = list(ds[ZT].values)
    zl.reverse()
    zl.append(0)
    zl.reverse()
    zm = []
    for i in range(len(zl) - 1):
        zm.append((-zl[i] + zl[i + 1]))
    zmid = ds.ZTOP.copy()
    zmid.values = zm
    zname = ZLM
    zmid.name = zname
    new_ds = ds.assign_coords(**{zname: zmid})
    return new_ds


def add_volume(ds: xr.Dataset):
    new_ds = ds.copy()
    new_ds[VOL] = new_ds[GA] * new_ds[ZM]
    new_ds = new_ds.assign_coords(**{VOL: new_ds[VOL]})
    return new_ds


def add_alt_m(ds: xr.Dataset) -> xr.Dataset:
    new_ds = ds.copy()
    new_ds[ALT] = new_ds[TOPO] + new_ds[ZM]
    new_ds = new_ds.assign_coords(**{ALT: new_ds[ALT]})
    return new_ds


def get_concat_array_values(file_ds_list: list, pnt=False) -> np.ndarray:
    f1 = file_ds_list[0]
    llen = len(file_ds_list)
    vals = np.zeros((llen, *(f1.CONC.shape[1:])), dtype=float)
    for i in range(llen):
        if pnt: print(i)
        ds = file_ds_list[i]
        v = ds['CONC'][0].values
        vals[i] = v
    return vals


def create_concat_ds(file_ds_list, vals):
    dims = list(file_ds_list[0].dims.mapping.mapping.keys())
    time_dim = [ds[TIME] for ds in file_ds_list]
    time_dim = xr.concat(time_dim, dim=TIME)
    ds = xr.Dataset({
        'CONC': (
            dims,
            vals
        )
    })

    ds = ds.assign_coords(**{TIME: time_dim})
    return ds


def ds_swap_dims(ds):
    ds2 = ds
    ds2 = ds2.swap_dims({SN: LAT})
    ds2 = ds2.swap_dims({WE: LON})
    ds2 = ds2.swap_dims({BT: ZM})
    return ds2


def ds_add_ll_dis(ds):
    ds2 = ds
    la_dis = (ds2[LAT] - CHC_LAT)
    lo_dis = (ds2[LON] - CHC_LON)

    ll_dis = np.sqrt(la_dis ** 2 + lo_dis ** 2)
    ds2[LL_DIS] = ll_dis
    return ds2


def fix_releases(ds, prnt=False):
    ds2 = ds
    hours = 96
    rr = range(hours, -1, -1)
    dsn = ds2.isel(**{TIME: slice(None, hours + 1)}).copy()
    dsn = dsn.assign_coords(Time=rr)

    actual_time = dsn[CONC].isel(**{LAT: 0, LON: 0, ZM: 0}).copy()
    vals = actual_time.values
    actual_time.values = np.full_like(vals, np.NaN, dtype=np.datetime64)
    # ACTUAL_TIME = 'ACTUAL_TIME'
    actual_time.name = ACTUAL_TIME

    dsn[ACTUAL_TIME] = actual_time
    for i in range(len(ds2[RL])):
        if prnt: print(i)
        ds1 = ds2.isel(**{RL: i})
        rt = ds1[RL].values

        rend = rt - pd.Timedelta(hours, 'hours')

        ds1 = ds1.sel(**{TIME: slice(rend, rt)})

        old_times = ds1.Time.copy()

        old_times.name = ACTUAL_TIME

        ds1.Time.values = rr
        ds1[ACTUAL_TIME] = old_times
        ds1[ACTUAL_TIME].Time.values = rr

        for v in list(ds1.data_vars):
            if RL in dsn[v].dims:
                dsn[v][{RL: i}] = ds1[v]
    return dsn


def add_chc_lpb(ax):
    ax.scatter(CHC_LON, CHC_LAT, marker='.', color='b', transform=PROJ)
    ax.scatter(LPB_LON, LPB_LAT, marker='.', color='g', transform=PROJ)


def get_ax_bolivia(
        ax=False,
        fig_args={},
        lalo_extent=LALO_BOL
):
    fig_ops = dict(figsize=(15, 10))
    fig_ops = {**fig_ops, **fig_args}
    if ax is False:
        fig = plt.figure(**fig_ops)
        ax = fig.add_subplot(1, 1, 1, projection=PROJ, )

    ax.set_extent(lalo_extent, crs=PROJ)
    ax.add_feature(cartopy.feature.COASTLINE.with_scale('10m'))
    ax.add_feature(cartopy.feature.BORDERS.with_scale('10m'))
    ax.add_feature(cartopy.feature.LAKES.with_scale('10m'), alpha=0.5, linestyle='-')
    ax.add_feature(cartopy.feature.STATES.with_scale('10m'), alpha=0.5, linestyle=':')
    gl = ax.gridlines(crs=PROJ, alpha=0.5, linestyle='--',
                      draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False

    add_chc_lpb(ax)

    return ax


def get_ax_lapaz(ax=False,
                 fig_args={},
                 lalo_extent=LALO_LAPAZ):
    if ax is False:
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(1, 1, 1, projection=PROJ, )

    ax.set_extent(lalo_extent, crs=PROJ)
    ax.add_feature(cartopy.feature.COASTLINE.with_scale('10m'))
    ax.add_feature(cartopy.feature.BORDERS.with_scale('10m'))
    ax.add_feature(cartopy.feature.LAKES.with_scale('10m'), alpha=0.5, linestyle='-')
    ax.add_feature(cartopy.feature.STATES.with_scale('10m'), alpha=0.5, linestyle=':')
    gl = ax.gridlines(crs=PROJ, alpha=0.5, linestyle='--',
                      draw_labels=True)

    gl.xlabels_top = False
    gl.ylabels_right = False

    add_chc_lpb(ax)

    return ax


def red_cmap():
    cmap = plt.get_cmap('Reds')
    my_cmap = cmap(np.arange(cmap.N))

    # Set alpha
    my_cmap[:, -1] = np.linspace(.3, 1, cmap.N)

    my_cmap = ListedColormap(my_cmap)

    return my_cmap


def get_r_dis(ds, lat_center=CHC_LAT, lon_center=CHC_LON):
    la = ds[LAT] - lat_center
    lo = ds[LON] - lon_center
    r = np.sqrt(la ** 2 + lo ** 2)
    return r


def get_th_ang(ds, lat_center=CHC_LAT, lon_center=CHC_LON):
    th = np.arctan2(ds[LAT] - lat_center,
                    ds[LON] - lon_center)
    th = np.mod(-th + np.pi / 2, 2 * np.pi)

    return th


def data_array_to_logpolar(da: xr.DataArray,
                           r_round_log: float,
                           th_round_rad: float,
                           lat_center=CHC_LAT,
                           lon_center=CHC_LON,
                           dim2keep=[],
                           fun='sum'
                           ) -> xr.DataArray:
    nda = da.copy()
    nda[LL_DIS] = get_r_dis(nda, lat_center, lon_center)

    nda[LL_ANG] = get_th_ang(nda, lat_center, lon_center)

    r_log_round_center = (np.round(
        np.log(nda[LL_DIS]) / r_round_log
    ) * r_round_log)

    nda[R_CENTER] = np.e ** r_log_round_center
    # nda[R_FAR] = np.e ** (r_log_round_center + r_round_log/2)
    # nda[R_CLOSE] = np.e ** (r_log_round_center - r_round_log/2)

    th_round_center = np.floor(nda[LL_ANG] / th_round_rad) * th_round_rad
    th_round_center = th_round_center + th_round_rad / 2
    nda[TH_CENTER] = th_round_center

    name = da.name

    df = nda.to_dataframe().reset_index()
    df = df[[R_CENTER, TH_CENTER, name, *dim2keep]]
    df: pd.DataFrame = getattr(df.groupby([R_CENTER, TH_CENTER, *dim2keep]),
                               fun)()
    r_th_da = df.to_xarray()[name]

    r_th_da[LAT] = r_th_to_lat(lat_center, r_th_da[R_CENTER], r_th_da[TH_CENTER])
    r_th_da[LON] = r_th_to_lat(lon_center, r_th_da[R_CENTER], r_th_da[TH_CENTER])

    r_log = np.log(r_th_da[R_CENTER])
    th_cen = r_th_da[TH_CENTER]

    rM = np.e ** (r_log + r_round_log / 2)
    rm = np.e ** (r_log - r_round_log / 2)
    thM = th_cen + th_round_rad / 2
    thm = th_cen - th_round_rad / 2

    val_list = [
        [LAT_00, LON_00, rm, thm],
        [LAT_10, LON_10, rM, thm],
        [LAT_11, LON_11, rM, thM],
        [LAT_01, LON_01, rm, thM],
    ]

    for v in val_list:
        r_th_da[v[0]] = r_th_to_lat(lat_center, v[2], v[3])
        r_th_da[v[1]] = r_th_to_lon(lon_center, v[2], v[3])

    r_th_da = r_th_da.where(~r_th_da.isnull(), 0)
    r_th_da[GA] = get_pol_area(r_th_da)

    return r_th_da


def r_th_to_ll(center, rr, th, fun):
    res = rr * fun(
        th
    ) + center
    return res


def r_th_to_lon(lon_center, rr, th):
    return r_th_to_ll(lon_center, rr, th, np.sin)


def r_th_to_lat(lat_center, rr, th):
    return r_th_to_ll(lat_center, rr, th, np.cos)


def polygon_from_row(r):
    pol = Polygon([
        [r[LON_00], r[LAT_00]],
        [r[LON_10], r[LAT_10]],
        [r[LON_11], r[LAT_11]],
        [r[LON_01], r[LAT_01]],
    ], True)
    return pol


def logpolar_plot(ds,
                  ax=False,
                  name='CONC',
                  perM=.95,
                  perm=0.0,
                  colorbar=True,
                  patch_args={},
                  quantile=True,
                  fig_ops={},
                  drop_zeros=True,
                  ):
    if ax is False:
        fig = plt.figure(**fig_ops)
        ax = fig.add_subplot(1, 1, 1, projection=PROJ, )
    df = ds.to_dataframe()
    if drop_zeros:
        df = df[df[name] > 0]
    pol_key = 'pol'
    df[pol_key] = df.apply(lambda r: polygon_from_row(r), axis=1)
    df = df.dropna()

    if quantile:
        maxc = df[name].quantile(perM)
        minc = df[name].quantile(perm)
    else:
        maxc = perM
        minc = perm
    p = PatchCollection(
        df[pol_key].values,
        **{
            'cmap'     : red_cmap(),
            'transform': PROJ,
            **patch_args
        }
    )
    p.set_array(df[name].values)
    p.set_clim(minc, maxc)
    ax.add_collection(p)
    fig = ax.figure
    if colorbar:
        cb = fig.colorbar(p)
        cb.ax.set_ylabel(PLOT_LABS[name], rotation=90)
    return ax


def get_pol_area(ds):
    df = ds.reset_coords()[LL00].copy().to_dataframe()
    df[GA] = df.apply(lambda r: get_area_from_row(r), axis=1)
    nds = df[GA].to_xarray()

    return nds


def get_area_from_row(r):
    coords = [
        [r[LON_00], r[LAT_00]],
        [r[LON_10], r[LAT_10]],
        [r[LON_11], r[LAT_11]],
        [r[LON_01], r[LAT_01]],
        [r[LON_00], r[LAT_00]], ]
    obj = {'type': 'Polygon', 'coordinates': [coords]}
    ar = area.area(obj)
    return ar


def trim_swap_dim_coord(nds: xr.Dataset, hours: int):
    rel_time = nds[RL].values
    # hours = 96
    rel_time_end = rel_time - pd.Timedelta(hours=hours)

    nds1 = nds.sel(**{TIME: slice(rel_time_end, rel_time)})

    # TH = 'Time_h'

    lt = len(nds1[TIME])
    tr = [i for i in range(-lt + 1, 1, 1)]

    time_h = nds1[TIME].copy()

    time_h.values = tr

    nds1[TH] = time_h

    nds2 = nds1.swap_dims({TIME: TH})
    nds2 = nds2.reset_coords(TIME)

    return nds2


def get_dims_complement(ds, keep):
    coords = set(list(ds.dims))
    if type(keep) is list:
        co_keep = set(keep)
    elif type(keep) is str:
        co_keep = set([keep])
    else:
        print('invalid keep')

    complement = list(coords - co_keep)
    return complement
    # return co_keep


def get_custom_cmap(to_rgb, from_rgb=[1, 1, 1]):
    # from color r,g,b
    r1, g1, b1 = from_rgb

    # to color r,g,b
    r2, g2, b2 = to_rgb

    cdict = {'red'  : ((0, r1, r1),
                       (1, r2, r2)),
             'green': ((0, g1, g1),
                       (1, g2, g2)),
             'blue' : ((0, b1, b1),
                       (1, b2, b2))}

    cmap = LinearSegmentedColormap('custom_cmap', cdict)
    return cmap


def plot_lapaz_rect(ax):
    bl = LALO_LAPAZ[0], LALO_LAPAZ[2]
    w = LALO_LAPAZ[1] - LALO_LAPAZ[0]
    h = LALO_LAPAZ[3] - LALO_LAPAZ[2]
    rect = matplotlib.patches.Rectangle(bl, w, h, linewidth=1, edgecolor='k', facecolor='none')
    ax.add_patch(rect)


def plot_clust_height(ds,
                      ax: plt.Axes,
                      perM,
                      quantile=True,
                      drop_zero=True,
                      par_to_plot=COL):
    ar = ds.copy()
    com = get_dims_complement(ar, [R_CENTER, ZM])

    ar = ar.sum(dim=com)
    if drop_zero:
        ar = ar.where(ar > 0)
    if quantile:
        q = ar.quantile(perM)
    else:
        q = perM
    lab = "km from CHC"
    ar[lab] = ar[R_CENTER] * 100
    ar = ar.swap_dims({R_CENTER: lab})
    try:
        ar.name = PLOT_LABS[par_to_plot]
    except:
        pass
    ar.plot(
        cmap=red_cmap(),
        vmin=0,
        vmax=q,
        ax=ax,
        x=lab,
    )
    ax.set_yscale('log')
    ax.set_ylim(100, 20000)
    ax.set_xscale('log')
    ax.set_xlim(.05 * 100, 30 * 100)
    ax.grid(True, 'major', axis='y')
    ax.grid(True, 'both', axis='x')
    ax.set_ylabel(PLOT_LABS[ZM])


def plot_absolute_height(ds,

                         ax=None,
                         perM=.95,
                         drop_zero=True,
                         par_to_plit=COL
                         ):


    mer = ds.copy()
    # i = 6


    fla = FLAGS
    HC = 'H*CONC'

    ver_area = 'VER_AREA'
    log_center = np.log(mer[R_CENTER])
    dis = log_center - \
          log_center.shift({R_CENTER: 1})
    dis = dis.median()
    l1 = log_center - dis / 2
    l2 = log_center + dis / 2
    l1 = np.e ** l1
    l2 = np.e ** l2
    r_dis = (l2 - l1) * 100000
    zlen = 500
    ar = np.arange(zlen / 2, 20000, zlen)

    mer = mer[[CONC, fla, TOPO]]

    # return merged_ds



    mer['c/v'] = mer[CONC] / mer[VOL]

    mer = mer.interp(**{ZM: ar})

    mer[VOL] = mer[GA] * zlen
    mer[CONC] = mer['c/v'] * mer[VOL]

    mer[H] = mer[TOPO] + mer[ZM]

    mer[HC] = mer[H] * mer[CONC]

    var = [CONC, HC]
    com = get_dims_complement(mer, [R_CENTER, ZM])
    ms = mer[var].sum(com)

    ms[ver_area] = ms[ZLM] * r_dis

    # ms:xr.DataArray = ms/ms[ver_area]

    ms[CONC] = ms[CONC].where(ms[CONC] > 0, 0)

    # ms = ms*zlen*r_dis

    ms[H] = ms[HC] / ms[CONC]


    def find_nearest(value):


        # ar = self.get_zlin()
        array = np.asarray(ar)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    ms[H] = xr.apply_ufunc(find_nearest, ms[H], vectorize=True)

    hs = ms.to_dataframe().groupby([H, R_CENTER]).sum()[CONC].to_xarray()

    lab = "km from CHC"
    hs[lab] = hs[R_CENTER] * 100
    hs = hs.swap_dims({R_CENTER: lab})

    hs1 = hs.interp(**{H: ar})
    hs1 = hs1.combine_first(hs)

    if drop_zero:
        hs1 = hs1.where(hs1 > 0)

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))


    q = hs1.quantile(perM)

    hs1.name = PLOT_LABS[CONC]

    hs1.plot(
        cmap=red_cmap(),
        vmin=0,
        vmax=q,
        ax=ax,
        x=lab,
    )
    ax.set_ylim(100, 20000)
    ax.set_xscale('log')
    ax.set_xlim(.05 * 100, 30 * 100)
    ax.grid(True, 'major', axis='y')
    ax.grid(True, 'both', axis='x')
    ax.set_ylabel(PLOT_LABS[H])
