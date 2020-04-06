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
import sys
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co

plt;
# %%
import flexpart_management.notebooks.log_pol_revisited as lpr
_DIR = lpr.__path__._path[0]
_data_dir = pjoin(_DIR,'data')

# %%

def get_da(d1, h1):
    h12 = h1.squeeze().drop('Times')
    d12 = xr.merge([d1, h12])
    # %%
    d12 = set_r_th_coords(d12)
    # np.unique(d12[co.TH_CENTER])
    # %%
    d12['LAT'] = d12[co.XLAT].mean(co.WE)
    d12['LON'] = d12[co.XLONG].mean(co.SN)

    la_med = (h1[co.XLAT] - h1[co.XLAT_CORNER])
    lo_med = (h1[co.XLONG] - h1[co.XLONG_CORNER])
    area = np.abs((4*lo_med*la_med))
    d12['G_AREA'] = area

    d12 = d12.reset_coords().set_coords(['LAT', 'LON', 'ZTOP','G_AREA'])
    d12 = d12.swap_dims({co.WE: 'LON', co.SN: 'LAT', co.BT: co.ZT})
    # %%
    # %%
    time_str = d12['Times'].load().item().decode('UTF-8')
    time = pd.to_datetime(time_str, format='%Y%m%d_%H%M%S')
    rl = d12['ReleaseName'].str.decode('UTF-8')
    rl = pd.to_datetime(rl, format='chc%Y%m%d_%H')
    d12[co.RL] = rl
    hour_ = (rl - time).days * 24 + (rl - time).seconds / 3600
    d12['AGE'] = xr.zeros_like(d12[co.RL], dtype=float) + hour_
    d12 = d12.set_coords(
        [co.R_CENTER, co.TH_CENTER,
         'R', 'TH', co.TOPO, co.GA, 'logR', 'deltaR', 'AGE',
         co.XLAT,co.XLONG
         ])
    # %%
    da12 = d12['CONC']
    da12:xr.DataArray = da12.squeeze(['Time', 'ageclass'])[{co.ZT: slice(0, 30)}]
    da12 = da12.expand_dims(**{'Time':[time]})
    return da12


def set_r_th_coords(d12):
    lo = d12[co.XLONG] - co.CHC_LON
    la = d12[co.XLAT] - co.CHC_LAT
    r = np.sqrt(lo ** 2 + la ** 2)
    th = np.arctan2(lo, la)
    d12['R'] = r
    d12['TH'] = th
    d12['logR'] = np.log(r)
    d12['deltaR'] = r * (np.exp(co.ROUND_R_LOG) - 1)
    # d12['DEN'] = d12['CONC']/d12[co.GA]
    log_ = (d12['logR'] / co.ROUND_R_LOG)
    exp = log_.round() * co.ROUND_R_LOG
    d12[co.R_CENTER] = np.exp(exp)
    th_ = round_th(d12,lab='TH')
    d12[co.TH_CENTER] = (np.round(th_,3)*1000).astype(int)/1000
    return d12


def round_th(d12, lab='TH'):
    mod = np.mod(d12[lab], 2 * np.pi)
    th_half = co.ROUND_TH_RAD / 2
    th_ = np.round((mod - th_half) / co.ROUND_TH_RAD)
    th_ = th_ * co.ROUND_TH_RAD + th_half
    return th_



def get_log_pol(da12):
    da12_ = da12.reset_coords([co.TOPO, co.XLONG, co.XLAT, co.GA,'G_AREA'])
    g = da12_.groupby(co.R_CENTER)
    li = []
    for l, _d in g:
        gg = _d[[co.CONC, co.GA, 'G_AREA']].groupby(co.TH_CENTER)
        res = gg.sum()
        res = res.expand_dims(**{co.R_CENTER: [l]})

        gg = _d[[co.XLONG, co.XLAT, co.TOPOGRAPHY]].groupby(co.TH_CENTER)
        res1 = gg.mean()
        res1 = res1.expand_dims(**{co.R_CENTER: [l]})

        _d['ca'] = _d[co.CONC] * _d['AGE']

        gg=_d[[co.CONC,'ca']].groupby(co.TH_CENTER)
        ag = gg.sum()
        ag = ag['ca']/ag[co.CONC]
        ag = ag.expand_dims(**{co.R_CENTER:[l]})
        ag.name = 'AGE'


        num = _d[co.CONC].groupby(co.TH_CENTER).count()
        num = num.expand_dims(**{co.R_CENTER: [l]})
        num = num.min(fa.dc(num,co.R_CENTER))
        res = res.assign_coords(**{'NUM': num})

        res = xr.merge([res, res1,ag])
        if len(res[co.TH_CENTER]) == 36:
            li.append(res)
    nd = xr.concat(li, dim=co.R_CENTER)
    nd = nd.set_coords([co.GA, co.TOPO, co.XLAT, co.XLONG])
    return nd

def get_mid_point(vector):
    i0 = vector[0]
    nlat = [i0.item()]
    for i in range(len(vector) - 1):
        im = vector[i] + (vector[i + 1] - vector[i]) / 2
        nlat.append(im.item())
        nlat.append(vector[i + 1].item())
    return nlat

def increase_res(coarse_da, r_max):
    da = coarse_da
    da = da.loc[{
        'LAT': slice(co.CHC_LAT - r_max, co.CHC_LAT + r_max),
        'LON': slice(co.CHC_LON - r_max, co.CHC_LON + r_max),
    }]
    # %%
    nlat = get_mid_point(da['LAT'])
    nlon = get_mid_point(da['LON'])
    nda = da.interp({'LAT': nlat, 'LON': nlon})
    nda.values = nda.values / 4
    nda[co.GA] = nda[co.GA] / 4
    nda['G_AREA'] = nda['G_AREA']/4
    nda = set_r_th_coords(nda)
    return nda

def get_merged_da_log_pol(d1, d2, h1, h2)->xr.Dataset:
    da22 = get_da(d2, h2)
    nd2 = get_log_pol(da22)
    da12 = get_da(d1, h1)
    nd1 = get_log_pol(da12)
    # %%
    nda = increase_res(da12, 4)
    # nda = increase_res(nda,4)
    nd12 = get_log_pol(nda)
    nda0_4 = increase_res(da22, .4)
    # nda0_4 = increase_res(nda0_4, .4)
    nd0_4 = get_log_pol(nda0_4)
    # %%
    nda0_2 = increase_res(nda0_4, .2)
    # nda0_2 = increase_res(nda0_2, .2)
    nd0_2 = get_log_pol(nda0_2)
    # %%
    nda0_1 = increase_res(nda0_2, .1)
    # nda0_1 = increase_res(nda0_1, .1)
    nd0_1 = get_log_pol(nda0_1)
    # %%
    r0 = .08
    a1 = nd0_1.loc[{co.R_CENTER: slice(r0, None)}]
    r1 = a1[co.R_CENTER][-1]
    a2 = nd0_2.loc[{co.R_CENTER: slice(1.01 * r1, None)}][
        {co.R_CENTER: slice(0, -1)}]
    r2 = a2[co.R_CENTER][-1]
    a3 = nd0_4.loc[{co.R_CENTER: slice(1.01 * r2, None)}][
        {co.R_CENTER: slice(0, -1)}]
    r3 = a3[co.R_CENTER][-1]
    a4 = nd2.loc[{co.R_CENTER: slice(1.01 * r3, None)}][
        {co.R_CENTER: slice(0, -1)}]
    r4 = a4[co.R_CENTER][-1]
    a5 = nd12.loc[{co.R_CENTER: slice(1.01 * r4, None)}][
        {co.R_CENTER: slice(0, -1)}]
    r5 = a5[co.R_CENTER][-1]
    a6 = nd1.loc[{co.R_CENTER: slice(1.01 * r5, None)}]
    aa = xr.concat([a1, a2, a3, a4, a5, a6], dim=co.R_CENTER)
    aa[co.TH_CENTER] = round_th(aa, lab=co.TH_CENTER)
    return aa

# %%

def get_da2(h1, files1):
    d1 = xr.open_mfdataset(files1, concat_dim='Time', combine='nested')
    h1_ = h1.squeeze().drop('Times')
    d12 = xr.merge([d1, h1_])
    # %%
    d12 = set_r_th_coords(d12)
    # np.unique(d12[co.TH_CENTER])
    d12['LAT'] = d12[co.XLAT].mean(co.WE)
    d12['LON'] = d12[co.XLONG].mean(co.SN)
    la_med = (h1[co.XLAT] - h1[co.XLAT_CORNER])
    lo_med = (h1[co.XLONG] - h1[co.XLONG_CORNER])
    area = np.abs((4 * lo_med * la_med))
    d12['G_AREA'] = area
    d12 = d12.reset_coords().set_coords(['LAT', 'LON', 'ZTOP', 'G_AREA'])
    d12 = d12.swap_dims({co.WE: 'LON', co.SN: 'LAT', co.BT: co.ZT})
    # %%
    time_str = d12['Times'].str.decode('UTF-8')
    time = pd.to_datetime(time_str.values, format='%Y%m%d_%H%M%S')
    d12['Time'] = time
    rl = d12['ReleaseName'].str.decode('UTF-8')
    rl = pd.to_datetime(rl, format='chc%Y%m%d_%H')
    d12[co.RL] = rl
    # %%
    time2, rl2 = xr.broadcast(d12['Time'], d12[co.RL])
    hour_ = (rl2 - time2).dt.days * 24 + (rl2 - time2).dt.seconds / 3600
    d12['AGE'] = hour_
    # %%
    d12 = d12.set_coords(
        [co.R_CENTER, co.TH_CENTER,
         'R', 'TH', co.TOPO, co.GA, 'logR', 'deltaR', 'AGE',
         co.XLAT, co.XLONG
         ])
    # %%
    da12 = d12['CONC']
    da12: xr.DataArray = da12.squeeze(['ageclass'])[{co.ZT: slice(0, 30)}]
    return da12


def sum_over_time(da12):
    da = da12.sum(co.TIME)
    dage = (da12 * da12['AGE']).sum(co.TIME) / da
    # dage.load()
    da['AGE'] = dage
    return da

def get_merged_da_log_pol2(da12, da22)->xr.Dataset:
    # da22 = get_da(d2, h2)
    nd2 = get_log_pol(da22)
    # da12 = get_da(d1, h1)
    nd1 = get_log_pol(da12)
    # %%
    nda = increase_res(da12, 4)
    # nda = increase_res(nda,4)
    nd12 = get_log_pol(nda)
    nda0_4 = increase_res(da22, .4)
    # nda0_4 = increase_res(nda0_4, .4)
    nd0_4 = get_log_pol(nda0_4)
    # %%
    nda0_2 = increase_res(nda0_4, .2)
    # nda0_2 = increase_res(nda0_2, .2)
    nd0_2 = get_log_pol(nda0_2)
    # %%
    nda0_1 = increase_res(nda0_2, .1)
    # nda0_1 = increase_res(nda0_1, .1)
    nd0_1 = get_log_pol(nda0_1)
    # %%
    r0 = .08
    a1 = nd0_1.loc[{co.R_CENTER: slice(r0, None)}]
    r1 = a1[co.R_CENTER][-1]
    a2 = nd0_2.loc[{co.R_CENTER: slice(1.01 * r1, None)}][
        {co.R_CENTER: slice(0, -1)}]
    r2 = a2[co.R_CENTER][-1]
    a3 = nd0_4.loc[{co.R_CENTER: slice(1.01 * r2, None)}][
        {co.R_CENTER: slice(0, -1)}]
    r3 = a3[co.R_CENTER][-1]
    a4 = nd2.loc[{co.R_CENTER: slice(1.01 * r3, None)}][
        {co.R_CENTER: slice(0, -1)}]
    r4 = a4[co.R_CENTER][-1]
    a5 = nd12.loc[{co.R_CENTER: slice(1.01 * r4, None)}][
        {co.R_CENTER: slice(0, -1)}]
    r5 = a5[co.R_CENTER][-1]
    a6 = nd1.loc[{co.R_CENTER: slice(1.01 * r5, None)}]
    aa = xr.concat([a1, a2, a3, a4, a5, a6], dim=co.R_CENTER)
    aa[co.TH_CENTER] = round_th(aa, lab=co.TH_CENTER)
    return aa

