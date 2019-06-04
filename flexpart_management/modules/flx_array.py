# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
from matplotlib.colors import ListedColormap
from useful_scit.imps import *
from typing import List
import cartopy

PROJ = cartopy.crs.PlateCarree()

TIME = 'Time'
WE = 'west_east'
SN = 'south_north'
TOPO = 'TOPOGRAPHY'
ZM = 'ZMID'
ALT = 'ALT'
BT = 'bottom_top'
RL = 'releases'
VOL = 'VOL'
GA = 'GRIDAREA'
CONC = 'CONC'
LAT = 'LAT'
LON = 'LON'
LL_DIS = 'LL_DIS'
ACTUAL_TIME = 'ACTUAL_TIME'

CHC_LAT = -16.350427
CHC_LON = -68.131335

LPB_LAT = -16.507125
LPB_LON = -68.129299



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
    new_ds=new_ds.assign_attrs(ds_head.attrs)
    release_start_times = get_releases_start_time(ds_head)
    new_ds = new_ds.assign_coords(**{RL:release_start_times})

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

def get_releases_start_time(ds_head:xr.Dataset):
    sim_start_dt = '{:08d}'.format(ds_head.SIMULATION_START_DATE) + ' ' +\
                   '{0:06d}'.format(ds_head.SIMULATION_START_TIME)
    sim_start_dt = dt.datetime.strptime(sim_start_dt, '%Y%m%d %H%M%S')
    start_deltas = ds_head.ReleaseTstart_end.values[:,0].round(-1)

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
    zl = list(ds.ZTOP.values)
    zl.reverse()
    zl.append(0)
    zl.reverse()
    zm = []
    for i in range(len(zl) - 1):
        zm.append((zl[i]))
    zmid = ds.ZTOP.copy()
    zmid.values = zm
    zname = 'ZBOT'
    zmid.name = zname
    new_ds = ds.assign_coords(**{zname: zmid})
    return new_ds


def add_zlength_m(ds: xr.Dataset):
    zl = list(ds.ZTOP.values)
    zl.reverse()
    zl.append(0)
    zl.reverse()
    zm = []
    for i in range(len(zl) - 1):
        zm.append((-zl[i] + zl[i + 1]))
    zmid = ds.ZTOP.copy()
    zmid.values = zm
    zname = 'ZLEN_M'
    zmid.name = zname
    new_ds = ds.assign_coords(**{zname: zmid})
    return new_ds


def add_volume(ds: xr.Dataset):
    new_ds = ds.copy()
    new_ds[VOL] = new_ds[GA] * new_ds[ZM]
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
    ds2=ds
    hours=96
    rr= range(hours,-1,-1)
    dsn = ds2.isel(**{TIME:slice(None,hours+1)}).copy()
    dsn = dsn.assign_coords(Time=rr)
    
    actual_time = dsn[CONC].isel(**{LAT:0,LON:0,ZM:0}).copy()
    vals = actual_time.values
    actual_time.values = np.full_like(vals,np.NaN,dtype=np.datetime64)
    # ACTUAL_TIME = 'ACTUAL_TIME'
    actual_time.name = ACTUAL_TIME
    
    dsn[ACTUAL_TIME]=actual_time
    for i in range(len(ds2[RL])):
        if prnt: print(i)
        ds1 = ds2.isel(**{RL:i})
        rt = ds1[RL].values

        rend = rt - pd.Timedelta(hours,'hours')
    
        ds1 = ds1.sel(**{TIME:slice(rend,rt)})
    
        old_times = ds1.Time.copy()
    
        old_times.name = ACTUAL_TIME
    
        ds1.Time.values = rr
        ds1[ACTUAL_TIME] = old_times
        ds1[ACTUAL_TIME].Time.values = rr
    
        for v in list(ds1.data_vars):
            if RL in dsn[v].dims:
                dsn[v][{RL:i}]=ds1[v]
    return dsn


def get_ax_bolivia():
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ, )

    ax.set_extent([-89.14205, -43.063545, -31.979277, -0.333519], crs=PROJ)
    ax.add_feature(cartopy.feature.COASTLINE.with_scale('10m'))
    ax.add_feature(cartopy.feature.BORDERS.with_scale('10m'))
    ax.add_feature(cartopy.feature.LAKES.with_scale('10m'), alpha=0.5, linestyle='-')
    ax.add_feature(cartopy.feature.STATES.with_scale('10m'), alpha=0.5, linestyle=':')
    gl=ax.gridlines(crs=PROJ,alpha=0.5, linestyle='--',
                 draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False

    add_chc_lpb(ax)

    return ax


def add_chc_lpb(ax):
    ax.scatter(CHC_LON, CHC_LAT, marker='.', color='b', transform=PROJ)
    ax.scatter(LPB_LON, LPB_LAT, marker='.', color='g', transform=PROJ)


def get_ax_lapaz():
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ, )

    ax.set_extent([-69, -67, -17, -15], crs=PROJ)
    ax.add_feature(cartopy.feature.COASTLINE.with_scale('10m'))
    ax.add_feature(cartopy.feature.BORDERS.with_scale('10m'))
    ax.add_feature(cartopy.feature.LAKES.with_scale('10m'), alpha=0.5, linestyle='-')
    ax.add_feature(cartopy.feature.STATES.with_scale('10m'), alpha=0.5, linestyle=':')
    ax.gridlines(crs=PROJ,alpha=0.5, linestyle='--',
                 draw_labels=True)

    add_chc_lpb(ax)

    return ax

def red_cmap():
    cmap = plt.get_cmap('Reds')
    my_cmap = cmap(np.arange(cmap.N))

    # Set alpha
    my_cmap[:,-1] = np.linspace(.3, 1, cmap.N)

    my_cmap = ListedColormap(my_cmap)

    return my_cmap