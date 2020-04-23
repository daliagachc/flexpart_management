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
from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

# %%
ZGL = 'ZGL_all'
CLK_DIR = 'clock_dir_all'
ZSL = 'ZSL_all'
RDIS = 'R_DIS_all'

STACK = 'stack'

N6 = 'lab_nc06'

N18 = 'lab_nc18'

NORM = 'normalized'

ZCOL = 'z_column'

NRL = [co.ZM,co.TH_CENTER,co.R_CENTER]

CALL = 'conc_all'
AALL = 'age_all'

CO = 'CONC'

SURF = 'BL'

LEV0 = 'LEV0'

AGE = 'AGE'

ALL = 'ALL'

CL6 = 'conc_lab_nc06'

CL18 = 'conc_lab_nc18'

AG6 = 'age_lab_nc06'

AG18 = 'age_lab_nc18'

orig = {NORM:False,ZCOL:ALL}

slice_surf = {co.ZM: slice(0, 3)}

slice_lev0 = {co.ZM: [0]}

plt;
# %%

def get_dcc():
    ds = fa.open_temp_ds('ds_clustered_18_agl.nc')
    dsn = xr.open_mfdataset(pjoin(co.tmp_data_path, 'new_log_pol_ds_agl.nc'),
                            combine='nested', concat_dim=co.RL)
    slice_ = {co.R_CENTER: slice(0, 30), co.RL:0}
    dsn[N18] = ds['lab_name'][slice_]
    dsn[N18].values = ds['lab_name'][slice_].values
    dsn[N6] = ds[N6][slice_]
    dsn[N6].values = ds[N6][slice_].values

    dsn = dsn.set_coords([N18,N6])

    return dsn

def get_lab_ser(NN, ds):
    dst = ds[[CO]].stack({STACK: NRL})
    n18 = list(set(np.unique(dst[NN])) - {'nan'})
    labs = []
    for lab in n18:
        _boo = dst[NN] == lab
        nd = (dst[{STACK: _boo}] ).sum(STACK)
        nd = nd.expand_dims(**{NN: [lab], NORM: [False], ZCOL: [ALL]})
        nd = nd.rename({co.CONC: f'conc_{NN}'})

        labs.append(nd)
    ss = xr.concat(labs, dim=NN)
    # big_ds = xr.merge([big_ds, ss])
    return ss


def get_lab_ser_surf(NN, ds,
                     slice_s=slice_surf, s=SURF):
    dst = ds[[CO]].stack({STACK: NRL})
    n18 = list(set(np.unique(dst[NN])) - {'nan'})
    labs = []
    dsu = dst.unstack()
    dsu = dsu[slice_s]
    dst = dsu.stack({STACK:[co.R_CENTER,co.TH_CENTER,co.ZM]})
    for lab in n18:
        _boo = dst[NN] == lab
        nd = (dst[{STACK: _boo}]).sum(STACK)
        nd = nd.expand_dims(**{NN: [lab], NORM: [False], ZCOL: [s]})
        nd = nd.rename({co.CONC: f'conc_{NN}'})

        labs.append(nd)
    ss = xr.concat(labs, dim=NN)
    return ss
# %%

def get_lab_clk(NN, ds):
    # %%

    dst = ds[[CO]].stack({STACK: NRL})
    n18 = list(set(np.unique(dst[NN])) - {'nan'})
    labs = []
    # %%

    for lab in n18:
        _boo = dst[NN] == lab
        nd = dst[{STACK: _boo}]

        nd = nd.unstack()
        # return nd
        con = nd[CO].sum(NRL)

        x = nd[CO] * np.sin(nd[co.TH_CENTER])
        x = x.sum(NRL)
        y = nd[CO] * np.cos(nd[co.TH_CENTER])
        y = y.sum(NRL)
        nd = np.mod(np.arctan2(x, y), 2 * np.pi) * 6 / np.pi

        # ang_clock_all.name = CLK_DIR
        # ang_clock_all_all = ang_clock_all.expand_dims({ZCOL: [ALL]})

        nd = nd.expand_dims(**{NN: [lab], ZCOL: [ALL]})
        nd.name = f'clk_{NN}'
        nd = nd.where(con>0)
        labs.append(nd)
    ss = xr.concat(labs, dim=NN)
    # big_ds = xr.merge([big_ds, ss])
    return ss

def get_lab_clk_surf(NN, ds, slice_s=slice_surf,s = SURF):
    # %%

    dst = ds[[CO]].stack({STACK: NRL})
    n18 = list(set(np.unique(dst[NN])) - {'nan'})
    dsu = dst.unstack()
    dsu = dsu[slice_s]
    dst = dsu.stack({STACK:[co.R_CENTER,co.TH_CENTER,co.ZM]})
    labs = []
    # %%

    for lab in n18:
        _boo = dst[NN] == lab
        nd = dst[{STACK: _boo}]

        nd = nd.unstack()
        # return nd
        con = nd[CO].sum(NRL)

        x = nd[CO] * np.sin(nd[co.TH_CENTER])
        x = x.sum(NRL)
        y = nd[CO] * np.cos(nd[co.TH_CENTER])
        y = y.sum(NRL)
        nd = np.mod(np.arctan2(x, y), 2 * np.pi) * 6 / np.pi

        # ang_clock_all.name = CLK_DIR
        # ang_clock_all_all = ang_clock_all.expand_dims({ZCOL: [ALL]})

        nd = nd.expand_dims(**{NN: [lab], ZCOL: [s]})
        nd.name = f'clk_{NN}'
        nd = nd.where(con>0)
        labs.append(nd)
    ss = xr.concat(labs, dim=NN)
    # big_ds = xr.merge([big_ds, ss])
    return ss

# %%

def get_co_all(ds):
    dsc: xr.Dataset = ds[[CO]].sum(NRL)
    dsc = dsc.rename({CO: CALL})
    dsc = dsc.expand_dims({NORM: [False], ZCOL: [ALL]})
    big_ds = dsc
    # %%
    surf: xr.DataArray = ds[slice_surf][CO].sum(NRL)
    surf = surf.expand_dims({NORM: [False], ZCOL: [SURF]})
    surf.name = CALL

    surf0: xr.DataArray = ds[slice_lev0][CO].sum(NRL)
    surf0 = surf0.expand_dims({NORM: [False], ZCOL: [LEV0]})
    surf0.name = CALL

    big_ds = xr.merge([big_ds, surf,surf0])
    # %%
    # norm = big_ds / big_ds[CALL].loc[{ZCOL: ALL, NORM: False}]
    # norm[NORM] = [True]
    # big_ds = xr.merge([big_ds, norm])
    return big_ds


# %%
def _loop_cluster_weighted_mean(NN, dst, n18, val, prefix, zcol):
    labs = []
    for lab in n18:
        _boo = dst[NN] == lab
        nd = dst[{STACK: _boo}]
        con = nd[CO].sum(STACK)
        age = (nd[val] * nd[CO]).sum(STACK)
        nd = age / con
        nd = nd.expand_dims(**{NN: [lab], ZCOL: [zcol]})
        nd.name = f'{prefix}_{NN}'
        labs.append(nd)
    ss = xr.concat(labs, dim=NN)
    return ss


def get_lab_wei(NN, ds, val=AGE,prefix='age'):
    dst = ds.stack({STACK: NRL})
    n18 = list(set(np.unique(dst[NN])) - {'nan'})
    ss = _loop_cluster_weighted_mean(NN, dst, n18, val, prefix, ALL)
    return ss

def get_lab_wei_surf(NN, ds, val=AGE, prefix='age', slice_s=slice_surf, s=SURF):
    dst = ds.stack({STACK: NRL})
    n18 = list(set(np.unique(dst[NN])) - {'nan'})
    dsu = dst.unstack()
    dsu = dsu[slice_s]
    dst = dsu.stack({STACK:[co.R_CENTER,co.TH_CENTER,co.ZM]})
    ss = _loop_cluster_weighted_mean(NN, dst, n18,val,prefix, s)
    return ss

def get_lab_age(NN,ds):
    return get_lab_wei(NN,ds,val=AGE,prefix = 'age')

def get_lab_age_surf(NN,ds, slice_s=slice_surf, s=SURF):
    return get_lab_wei_surf(NN,ds,val=AGE,prefix = 'age', slice_s=slice_surf, s=SURF)

def get_lab_rdis(NN,ds):
    return get_lab_wei(NN,ds,val=co.R_CENTER,prefix = 'r_dis')

def get_lab_rdis_surf(NN,ds, slice_s=slice_surf, s=SURF):
    return get_lab_wei_surf(NN,ds,val=co.R_CENTER,prefix = 'r_dis',
                            slice_s=slice_surf, s=SURF)

def get_lab_zsl(NN,ds):
    dzl = ds
    dzl[ZSL] = ds[co.ZM] + ds[co.TOPO]
    return get_lab_wei(NN,dzl,val=ZSL,prefix = 'zsl')

def get_lab_zsl_surf(NN,ds, slice_s=slice_surf, s=SURF):
    dzl = ds
    dzl[ZSL] = ds[co.ZM] + ds[co.TOPO]
    return get_lab_wei_surf(NN,dzl,val=ZSL,prefix = 'zsl', slice_s=slice_surf, s=SURF)

def get_lab_zgl(NN,ds):
    return get_lab_wei(NN,ds,val=co.ZM,prefix = 'zgl')

def get_lab_zgl_surf(NN,ds, slice_s=slice_surf, s=SURF):
    return get_lab_wei_surf(NN,ds,val=co.ZM,prefix = 'zgl', slice_s=slice_surf, s=SURF)


def get_all_weight(ds, weight_mean, name):
    all_age: xr.DataArray = (ds[CO] * ds[weight_mean]).sum(NRL) / ds[CO].sum(NRL)
    all_age.name = name
    all_age = all_age.expand_dims({ZCOL: [ALL]})
    dsurf = ds[slice_surf]
    all_age_s: xr.DataArray = (dsurf[CO] * dsurf[weight_mean]).sum(NRL) / dsurf[CO].sum(
        NRL)
    all_age_s.name = name
    all_age_s = all_age_s.expand_dims({ZCOL: [SURF]})

    dsurf0 = ds[slice_lev0]
    all_age_s0: xr.DataArray = (dsurf0[CO] * dsurf0[weight_mean]).sum(NRL) / dsurf0[CO].sum(
        NRL)
    all_age_s0.name = name
    all_age_s0 = all_age_s0.expand_dims({ZCOL: [LEV0]})


    all_age = xr.merge([all_age, all_age_s,all_age_s0])
    return all_age

def get_all_age(ds):
    return get_all_weight(ds,weight_mean=AGE, name = AALL)


def get_all_r(ds):
    return get_all_weight(ds, weight_mean=co.R_CENTER, name =RDIS)

def get_all_zsl(ds):
    dzl = ds
    dzl[ZSL] = ds[co.ZM] + ds[co.TOPO]

    return get_all_weight(dzl, weight_mean=ZSL, name =ZSL)

def get_all_zgl(ds):

    return get_all_weight(ds, weight_mean=co.ZM, name =ZGL)

def get_clock_dir_all(ds):
    x = ds[CO] * np.sin(ds[co.TH_CENTER])
    x = x.sum(NRL)
    y = ds[CO] * np.cos(ds[co.TH_CENTER])
    y = y.sum(NRL)
    ang_clock_all = np.mod(np.arctan2(x, y), 2 * np.pi) * 6 / np.pi
    ang_clock_all.name = CLK_DIR
    ang_clock_all_all = ang_clock_all.expand_dims({ZCOL:[ALL]})

    ds = ds[slice_surf]

    x = ds[CO] * np.sin(ds[co.TH_CENTER])
    x = x.sum(NRL)
    y = ds[CO] * np.cos(ds[co.TH_CENTER])
    y = y.sum(NRL)
    ang_clock_all = np.mod(np.arctan2(x, y), 2 * np.pi) * 6 / np.pi
    ang_clock_all.name = CLK_DIR
    ang_clock_all_surf = ang_clock_all.expand_dims({ZCOL:[SURF]})

    ds = ds[slice_lev0]

    x = ds[CO] * np.sin(ds[co.TH_CENTER])
    x = x.sum(NRL)
    y = ds[CO] * np.cos(ds[co.TH_CENTER])
    y = y.sum(NRL)
    ang_clock_all = np.mod(np.arctan2(x, y), 2 * np.pi) * 6 / np.pi
    ang_clock_all.name = CLK_DIR
    ang_clock_all_lev0 = ang_clock_all.expand_dims({ZCOL:[LEV0]})

    return xr.merge([ang_clock_all_all,ang_clock_all_surf,ang_clock_all_lev0])

def plt_diag(all_age, all_dis, all_ds, all_zsl, ang_clock_all):
    _row = 7
    s = splot(_row, 1, sharex=True, figsize=(10, _row * 2), dpi=300)
    all_ds[CALL].loc[orig].plot(ax=s.axf[0])
    all_age[AALL].loc[{ZCOL: ALL}].plot(ax=s.axf[1])
    all_dis[RDIS].loc[{ZCOL: ALL}].plot(ax=s.axf[2])
    all_zsl[ZSL].loc[{ZCOL: ALL}].plot(ax=s.axf[3])
    (all_ds[CALL].loc[{ZCOL: SURF}] / all_ds[CALL].loc[{ZCOL: ALL}]).plot(
        ax=s.axf[4])
    ang_clock_all[CLK_DIR].loc[{ZCOL: ALL}].plot(ax=s.axf[5], linewidth=0,
                                                 marker='.')
    ang_clock_all[CLK_DIR].loc[{ZCOL: SURF}].plot(ax=s.axf[6], linewidth=0,
                                                  marker='.')
    for ax in s.axf:
        ax.grid()
    s.f.tight_layout()
    plt.show()

def merge_all(*,all_age, all_age_18, all_age_6, all_dis, all_ds, all_ds18,
              all_ds6, all_zsl, dsMAX_theory,
              surf_age_18,
              surf_age_6,
              surf_ds18,
              surf_ds6,
              all_zgl,
              ang_clock_all,
              surf_rdis_18  ,
              surf_rdis_6   ,
              surf_zsl_18   ,
              surf_zsl_6    ,
              surf_zgl_18   ,
              surf_zgl_6    ,
              all_rdis_18    ,
              all_rdis_6     ,
              all_zsl_18     ,
              all_zsl_6      ,
              all_zgl_18     ,
              all_zgl_6      ,
              all_clk_18,
              surf_clk_18,
              all_clk_6,
              surf_clk_6,

              surf0_age_18,
              surf0_age_6,
              surf0_ds18,
              surf0_ds6,
              surf0_rdis_18,
              surf0_rdis_6,
              surf0_zsl_18,
              surf0_zsl_6,
              surf0_zgl_18,
              surf0_zgl_6,
              surf0_clk_18,
              surf0_clk_6,

              ):
    mega_ds = xr.merge([all_ds, all_age, all_dis, all_zsl,
                        all_zgl, ang_clock_all,
                        all_ds18, all_ds6,
                        surf_ds6, surf_ds18,
                        all_age_18, all_age_6,
                        surf_age_18, surf_age_6,
                        all_rdis_18,
                        surf_rdis_18,
                        all_rdis_6,
                        surf_rdis_6,
                        all_zsl_18,
                        surf_zsl_18,
                        all_zsl_6,
                        surf_zsl_6,
                        all_zgl_18,
                        surf_zgl_18,
                        all_zgl_6,
                        surf_zgl_6,
                        all_clk_18,
                        surf_clk_18,
                        all_clk_6,
                        surf_clk_6,
                        surf0_age_18,
                        surf0_age_6,
                        surf0_ds18,
                        surf0_ds6,
                        surf0_rdis_18,
                        surf0_rdis_6,
                        surf0_zsl_18,
                        surf0_zsl_6,
                        surf0_zgl_18,
                        surf0_zgl_6,
                        surf0_clk_18,
                        surf0_clk_6,




                        ])
    norm = mega_ds[[CALL, CL6, CL18]] / dsMAX_theory
    norm[NORM] = [True]
    mega_ds = xr.merge([mega_ds, norm])
    return mega_ds

from shapely.geometry import Polygon
from shapely.ops import cascaded_union, unary_union
def get_pol2(r):
    # rr = int(8/r[co.R_CENTER])

    rm = int(np.round(np.log10(r['rm'])))
    rM = int(np.round(np.log10(r['rM'])))
    # print(rm)
    # print(rM)
    RR = 4
    p1 = r[[co.LON_00, co.LAT_00]].round(RR-rm)
    p2 = r[[co.LON_01, co.LAT_01]].round(RR-rm)
    p3 = r[[co.LON_11, co.LAT_11]].round(RR-rM)
    p4 = r[[co.LON_10, co.LAT_10]].round(RR-rM)

    po = Polygon([p1, p2, p3, p4])
    return po

def get_boundary_pol(ds1, lab, labtype, var2keep,*, threshold):
    dsl: xr.Dataset = ds1.where(ds1[labtype] == lab)
    dsl = dsl.unstack().sum(co.ZM).stack({STACK: [co.TH_CENTER, co.R_CENTER]})
    # %%
    dsl1: xr.Dataset = dsl.sortby(CO, ascending=False)
    dsl1['cum'] = dsl1[CO].cumsum()
    tot = dsl1[CO].sum().item()
    THRE = threshold
    dsl2 = dsl1.where(dsl1['cum'] < tot * THRE).dropna(STACK)
    df = dsl2.unstack().reset_coords()[var2keep].to_dataframe().dropna(axis=0)
    # %%
    # %%
    df: pd.DataFrame
    pols = df.apply(get_pol2, axis=1)
    # %%
    pol = unary_union(pols)
    return pol

import shapely
def get_pol_df(ds1, labtype, var2keep,threshold):
    labs = set(np.unique(ds1[labtype])) - set(['nan'])
    # print(labs)
    pol18 = {}
    for lab in labs:
        pol = get_boundary_pol(ds1, lab, labtype, var2keep, threshold=threshold)
        if type(pol) == shapely.geometry.multipolygon.MultiPolygon:
            pol = [p for p in pol.geoms]
        else:
            pol = [pol]

        pdf = pd.DataFrame(pol,columns=['pol'])
        pdf['area'] = pdf['pol'].apply(lambda p: p.area)
        pdf = pdf.set_index('area')
        ma = pdf.index.max()
        print(pdf)
        pol = pdf.loc[ma]

        pol18[lab] = pol



    df18 = pd.DataFrame(pol18).T
    # %%
    df18['x'] = df18['pol'].apply(lambda r: r.exterior.xy[0])
    df18['y'] = df18['pol'].apply(lambda r: r.exterior.xy[1])
    return df18

import simplekml

def make_pol(kml:simplekml.kml.Kml,r,col,alpha=200):
    points = [z for z in zip(r['x'],r['y'])]
    mg:simplekml.MultiGeometry = kml.newmultigeometry(name=r.name)
    pol = mg.newpolygon(
        name=str(r.name),
        outerboundaryis=points,
        altitudemode=simplekml.AltitudeMode.clamptoground
    )


    # alpha = (255 / max_col) * r[co.CPer]
    # alpha = min(int(alpha), 255)
    # if full:
    #     alpha = 255

    c = (np.array(col)*255).astype(int)

    pol.style.polystyle.color = simplekml.Color.rgb(*c,alpha)
    pol.style.polystyle.outline = 1
    mg.style.polystyle.color= simplekml.Color.rgb(*c,alpha)

    po:simplekml.Point = mg.newpoint(name=r.name)
    x,y = r['pol'].centroid.xy
    po.coords = [(x[0],y[0])]
    po.style.labelstyle.color = simplekml.Color.rgb(*c,alpha)

c45 = 'C4_C5_compounds'
c68 = 'C6_C8_compounds'
c91 = 'C9_C13_compounds'
bc  =  'BC'

r1 = 'c6_8/c4_5'
r2 = 'c9_13/c4_5'
r3 = 'BC/c4_5'
r4 = 'c4_5'


def import_time_series():
    data_path = pjoin(co.tmp_data_path, 'data_george_cc.xlsx')
    # df_ft = pd.read_excel(data_path)
    df_ts = pd.read_excel(data_path, sheet_name=1, skiprows=1)
    # %%
    df_ts = df_ts.set_index(pd.to_datetime(df_ts['time_utc']))
    df_ts = df_ts.drop('time_utc', axis=1)
    return df_ts