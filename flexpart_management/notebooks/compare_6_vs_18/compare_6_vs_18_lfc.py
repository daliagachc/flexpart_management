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
from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

LAB_18_6 = 'lab_18_6'

LAB6 = 'lab_6'
LAB66 = 'lab_18_6_6'
LAB18 = 'lab_18'
LAB = 'lab'
LAB2 = 'lab_2'

plt;

CS = 'CONC_smooth_t_300_z_25_r_100_th_50'
AT = 'above_thre'
SD = 'stack_dim'
CQT = 'CONC_QT'
TOT_CS = 'TOT_CS'


# %%

def trim_ds(*, ds, **kwargs):
    # df = pd.DataFrame
    _bool = ds[AT]
    da: xr.DataArray = ds[CS].where(_bool)
    # %%
    das = da.stack(**{SD: [co.R_CENTER, co.TH_CENTER, co.ZM]})
    # %%
    dat = das.dropna(dim=SD, how='all')
    # %%
    return dat


def add_total_cs(*, dat, **kwargs):
    dat = dat.assign_coords({TOT_CS: dat.sum(co.RL).load()})
    return dat


def getQT(*, dat, **kwargs) -> xr.Dataset:
    dan = xr.zeros_like(dat)
    from sklearn.preprocessing import QuantileTransformer
    qt = QuantileTransformer()
    dat = dat.transpose(co.RL, SD)
    res = qt.fit_transform(dat)
    dan = (dan + res).load()
    dan.name = CQT
    combined_ds = xr.merge([dat, dan])
    return combined_ds


def cluster(*, ds, n_clusters, lab_name, random_state) -> xr.Dataset:
    ds = ds.transpose(SD, co.RL)
    qt = ds[CQT]
    tot = ds[TOT_CS]
    lab = xr.zeros_like(tot, dtype=int)
    # print(ds[TOT_CS].sum())
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=n_clusters,
                init='random',
                random_state=random_state
                )
    res = km.fit_predict(qt.values.copy(), sample_weight=tot.values.copy())
    # print(ds[TOT_CS].sum())
    # print('tot',tot)
    lab = lab + res
    # print(ds[TOT_CS].sum())
    ds = ds.assign_coords({lab_name: lab})
    # print(ds[TOT_CS].sum())
    return ds


def get6(*, ds: xr.Dataset, random_state, **kwargs) -> xr.Dataset:
    ds = cluster(
        ds=ds, n_clusters=6,
        lab_name=LAB6, random_state=random_state
    )
    return ds


def get18(*, ds, random_state, **kwargs) -> xr.Dataset:
    ds = cluster(
        ds=ds, n_clusters=18,
        lab_name=LAB18, random_state=random_state
    )
    return ds


def get_18_6_dic(*, ds: xr.Dataset, **kwargs):
    cqt_ = ds[CQT]
    tot_ = ds[TOT_CS]
    cqt_tot = cqt_ * tot_
    # %%
    lab = LAB18
    # lab = LAB6
    cqt_tot_mean = cqt_tot.groupby(lab).sum()
    tot_mean = tot_.groupby(lab).sum()
    centroids = cqt_tot_mean / tot_mean
    # %%
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=6)
    centroids = centroids.transpose(lab, co.RL)
    lab_18_6 = xr.zeros_like(tot_mean, dtype=int)
    res = km.fit_predict(centroids.values.copy(),
                         sample_weight=tot_mean.values.copy()
                         )
    lab_18_6 = res + lab_18_6
    dic_18_6 = lab_18_6.reset_coords(drop=True).to_dataframe().to_dict()[TOT_CS]
    return dic_18_6


def get_18_6(*, nds2: xr.Dataset, **kwargs):
    dic_18_6 = get_18_6_dic(ds=nds2)

    # %%
    def _dic_fun(l): return dic_18_6[l]

    nds2[LAB_18_6] = xr.apply_ufunc(_dic_fun, nds2[LAB18], vectorize=True)
    nds2 = nds2.set_coords(LAB_18_6)
    return nds2


def get_labeling_abs_sim(*, nds3, lab6_filter, lab18_6_filter, **kwargs):
    _bool = nds3[LAB6] == lab6_filter
    d1 = nds3[TOT_CS].where(_bool)

    _bool = nds3[LAB_18_6] == lab18_6_filter
    d2 = nds3[TOT_CS].where(_bool)

    res_dic = {}

    sum_eq = (d1 + d2 - d2).sum()
    ret = sum_eq / d1.sum()

    res_dic[LAB6] = ret.item()

    sum_eq = (d1 + d2 - d1).sum()
    ret = sum_eq / d2.sum()

    res_dic[LAB_18_6] = ret.item()

    res_dic['mean'] = (res_dic[LAB6] + res_dic[LAB_18_6]) / 2

    return res_dic


def get_6_6_ds(*, nds3: xr.Dataset, **kwargs) -> xr.Dataset:
    dis_dic = {}
    ds_list = []
    for l6 in range(6):
        dic_dic = {}
        for l18 in range(6):
            dis = get_labeling_abs_sim(
                nds3=nds3,
                lab6_filter=l6, lab18_6_filter=l18
            )
            dic_dic[l18] = dis
        dis_dic[l6] = dic_dic
        ds = pd.DataFrame(dic_dic).to_xarray()
        ds = ds.expand_dims(**{'l6': [l6]}).to_array('l18')
        ds_list.append(ds)
    # %%
    ds = xr.concat(ds_list, dim='l6')
    return ds


def get_l6_l18_dic(*, ds66: xr.Dataset, **kwargs):
    max_l6 = ds66.loc[{'index': 'mean'}].max('l6')
    _bool = ds66.loc[{'index': 'mean'}] == max_l6
    _bool.name = 'dic'
    _df = _bool.reset_coords(drop=True).to_dataframe()
    # print(_df)
    drop = _df[_df].dropna().reset_index().drop('dic', axis=1)
    dic = drop.set_index('l18')['l6'].to_dict()
    return dic


def measure_distance_6_18(*, ds, **kwargs):
    return ds


def plot_heatmap_6_66(ds66):
    ds66.loc[{'index': 'mean'}].plot.line(x='l6')
    plt.show()
    # %%
    l6_l18_dic = get_l6_l18_dic(ds66=ds66)
    # %%
    res = xr.apply_ufunc(lambda v: l6_l18_dic[v], ds66['l18'], vectorize=True)
    ds67 = ds66.assign_coords(**{'l186': res}).swap_dims(
        {'l18': 'l186'}).sortby('l186')
    # %%
    mean_ = ds67.loc[{'index': 'mean'}] * 100
    mean_.name = 'mean'
    df_ = mean_.reset_coords(drop=True).to_dataframe()['mean'].unstack()
    f, ax = plt.subplots()
    ax: plt.Axes
    sns.heatmap(df_, linewidths=.5, annot=True, fmt='01.0f',
                cmap='Reds', ax=ax, square=True,
                cbar=False
                )
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    plt.tight_layout()
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    plt.show()


def plot_heatmap_6_vs_18(nds2):
    _df = nds2[CS].sum(co.RL).reset_coords()[[LAB18, LAB6, CS]]
    _df = _df.to_dataframe()
    # _df = _df.reset_index().set_index([LAB6,LAB18])[CS]
    # _df = _df.unstack()
    # %%
    un = _df.groupby([LAB18, LAB6]).sum()[CS].unstack().T
    sns.heatmap(un, square=True, cmap='Reds')
    plt.show()


def weighted_silhouette(*, diss, lab, weight, **kwargs):
    from rpy2.robjects import r
    from rpy2.robjects.packages import importr
    from rpy2.robjects import numpy2ri
    numpy2ri.activate()
    # %%
    wc = importr('WeightedCluster')
    wsr = r['wcSilhouetteObs']
    # %%

    # %%
    nr, nc = diss.shape
    rdiss = r.matrix(diss, nrow=nr, ncol=nc)
    rlab = r.array(lab.values)
    rtot = r.array(weight.values)
    res = np.array(wsr(rdiss, rlab, weights=rtot,measure="ASWw"))
    return res


def plot_sil_weighted_hist(*, lab, ax, nds3, diss, **kwargs):
    lab_ = nds3[lab]
    tot = nds3[TOT_CS]
    sil = xr.zeros_like(lab_)
    res = weighted_silhouette(diss=diss, lab=lab_, weight=tot)
    sil = sil + res

    # %%

    # ax.step()
    ax:plt.Axes
    bins = np.arange(-.4, .9, .025)
    y, x = np.histogram(sil, weights=tot / tot.sum(),
                        # facecolor='none',edgecolor='k',
                        # alpha=.5,
                        bins=bins,
                        # label=lab,
                        # ax=ax
                        )
    x = (x[:-1]+x[1:])/2
    from scipy.ndimage.filters import gaussian_filter1d
    y= gaussian_filter1d(y,1.5,mode='nearest',truncate=4)
    y = y/y.sum()

    pprint.pprint(y)

    ax.plot(x,y,label=lab)
