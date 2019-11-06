# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
# ---

# %%
import flexpart_management.modules.flx_array as fa

from useful_scit.imps import *
import flexpart_management.modules.constants as co
from sklearn import preprocessing
from sklearn.cluster import KMeans
import sklearn
# from main import dfcc
from flexpart_management.modules.flx_array import weighted_quantile



def plot_general(ds1):
    cl = co.CPer
    c1 = ds1[cl].sum([co.RL, co.ZM])
    c2 = ds1[cl].sum([co.ZM, co.RL, co.TH_CENTER])
    ar = c1 / c2
    # ar = c1
    ar = ar.isel(**{co.R_CENTER: slice(0, -3)})
    ax = fa.get_ax_bolivia(fig_args={'figsize': (5, 5)})
    fa.logpolar_plot(ar, name=co.CPer, ax=ax, perM=.95, perm=.01)
    ax.set_xlim(-75, -60)
    ax.set_ylim(-25, -7)
    return ax

def plot_general_lapaz(ds1):
    cl = co.CPer
    c1 = ds1[cl].sum([co.RL, co.ZM])
    c2 = ds1[cl].sum([co.ZM, co.RL, co.TH_CENTER])
    ar = c1 / c2
    # ar = c1
    ar = ar.isel(**{co.R_CENTER: slice(0, -3)})
    ax = fa.get_ax_lapaz(fig_args={'figsize': (5, 5)})
    fa.logpolar_plot(ar, name=co.CPer, ax=ax, perM=.95, perm=.01)
    # ax.set_xlim(-75, -60)
    # ax.set_ylim(-25, -7)
    return ax


def plot_hist_log(dfcc, cumulative=False, ax=False, nbins=20):
    _fl = dfcc.sum(axis=1).values
    bins = np.logspace(
        np.log10(_fl.max() * 1e-5),
        np.log10(_fl.max()),
        nbins
    )
    bins = [-bins[0], 0, *bins]
    if ax is False:
        f, ax = plt.subplots()
    else:
        ax = ax
        f = ax.figure
    ax.hist(
        _fl,
        bins=bins,
        weights=[100 / len(_fl)] * len(_fl),
        cumulative=cumulative,
        alpha=.5
    )
    ax: plt.Axes
    ax.set_xscale('log')
    ax.set_xlim((bins[2] * .5, bins[-1]))
    ax.set_xlabel('mass*res.time ')
    ax.set_ylabel('%')
    cell_tile = "Sum Values over cell"
    if cumulative is True:
        cell_tile = cell_tile + ' (cumulative)'
    ax.set_title(cell_tile)


def plot_hist_all_log(dfcc, cumulative=False, ax=False):
    _fl = dfcc.values.flatten()

    bins = np.logspace(
        np.log10(dfcc.max().max() * 1e-5),
        np.log10(dfcc.max().max()),
        10
    )
    bins = [-bins[0], 0, *bins]
    if ax is False:
        f, ax = plt.subplots()
    else:
        ax = ax
        f = ax.figure
    ax.hist(
        _fl,
        bins=bins,
        weights=[100 / len(_fl)] * len(_fl),
        cumulative=cumulative,
        alpha=.5
    )
    ax.set_xscale('log')
    ax: plt.Axes
    # ax.set_xscale('symlog')
    ax.set_xlim((bins[2] * .5, bins[-1]))
    ax.set_xlabel('mass*res.time ')
    ax.set_ylabel('%')
    cell_tile = "All Values over cell"
    if cumulative is True:
        cell_tile = cell_tile + ' (cumulative)'
    ax.set_title(cell_tile)


def plot_silhouette_score(
        n_c,
        sample_silhouette_values,
        cluster_labels,
        ax1,
        silhouette_avg
):
    y_lower = 10
    for i in range(n_c):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = [*ucp.cc, *ucp.cc][i]
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples
    # ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_title(str(n_c))
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")
    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    # ax1.axvline(x=sil_avg, color="red", linestyle="-")
    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    # ax1.set_xticks([-0.1, 0, 0.2, 0.4])

# %%

# ax = fa.get_ax_lapaz()
# fa.logpolar_plot(ar,name=co.CPer,ax=ax,perM=.95)


def plot_hist_values(dfcc):
    # global f, axs
    f, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs = axs.flatten()
    plot_hist_log(dfcc, ax=axs[0])
    plot_hist_log(dfcc, cumulative=True, ax=axs[1])
    f: plt.Figure
    f.tight_layout()


def plot_sil_score_grid(dscc):
    fig = plt.figure(figsize=(20, 40))
    for i in range(len(dscc[co.CLUS_LENGTH_DIM])):
        ii = dscc[co.CLUS_LENGTH_DIM][i].item()
        _d = dscc.loc[{co.CLUS_LENGTH_DIM: ii}][
            [co.FLAG, co.SIL_SC, co.SIL_SAMPLE]].stack(
            {co.DUM_STACK: [co.R_CENTER, co.TH_CENTER, co.ZM]})
        if i == 0:
            ax0 = ax = fig.add_subplot(5, 5, i + 1)
        else:
            ax = fig.add_subplot(5, 5, i + 1, sharex=ax0)

        plot_silhouette_score(
            n_c=ii,
            silhouette_avg=_d[co.SIL_SC],
            sample_silhouette_values=_d[co.SIL_SAMPLE].values,
            cluster_labels=_d[co.FLAG].values,
            ax1=ax
        )

def calc_silhouette_scores(dscc):
    _fl = dscc.where(dscc[co.LAB_CLUSTER_THRESHOLD])[
        [co.FLAG, co.CONC_NORMALIZED]].stack(
        {co.DUM_STACK: [co.R_CENTER, co.TH_CENTER, co.ZM]})
    # %%
    _fl = _fl.dropna(co.DUM_STACK)
    # %%
    _cl = _fl[co.CLUS_LENGTH_DIM]
    # %%
    _sil_sc = xr.full_like(dscc[co.CLUS_LENGTH_DIM], np.nan, float)
    _sil_sc.name = co.SIL_SC
    for i, _ in _cl.to_series().iteritems():
        #     print(i)
        _labs = _fl.sel(**{co.CLUS_LENGTH_DIM: i})[co.FLAG]
        _CC = _fl.sel(**{co.CLUS_LENGTH_DIM: [i]})[co.CONC_NORMALIZED]
        _scc = sklearn.metrics.silhouette_score(_CC.T, _labs)
        _sil_sc.loc[{co.CLUS_LENGTH_DIM: i}] = _scc
    # %%
    try:
        dscc = dscc.drop(co.SIL_SC)
    except:
        pass
    dscc = xr.merge([dscc, _sil_sc])
    # %%
    # %%
    _sil_sa = xr.full_like(_fl[co.FLAG], np.nan, float)
    _sil_sa.name = co.SIL_SAMPLE
    for i, _ in _cl.to_series().iteritems():
        print(i)
        _labs = _fl.sel(**{co.CLUS_LENGTH_DIM: i})[co.FLAG]
        _CC = _fl.sel(**{co.CLUS_LENGTH_DIM: [i]})[co.CONC_NORMALIZED]
        _scc = sklearn.metrics.silhouette_samples(_CC.T, _labs)
        _sil_sa.loc[{co.CLUS_LENGTH_DIM: i}] = _scc
    # %%
    try:
        dscc = dscc.drop(co.SIL_SAMPLE)
    except:
        pass
    dscc = xr.merge([dscc, _sil_sa.unstack()])
    return dscc

def plot_bar_charts_for_each_cluster_set(dscc):
    _ser = dscc[co.FLAG].to_series()
    _ser = _ser.groupby(co.CLUS_LENGTH_DIM).value_counts().sort_index()
    # %%
    _s1 = _ser.unstack(co.FLAG).T
    # %%
    _s1.plot.bar(subplots=True, layout=(-1, 4), figsize=(20, 10),
                 legend=False);

def do_clust_multiple(dscc):
    _co = co.CONC_NORMALIZED
    _ser = dscc[_co].where(dscc[co.LAB_CLUSTER_THRESHOLD]).to_dataframe()[
        _co].dropna()
    _ser = _ser.unstack(co.RL)
    # %%
    _co = co.CONC_NORMS
    _wei = dscc[_co].where(dscc[co.LAB_CLUSTER_THRESHOLD]).to_dataframe()[
        _co].dropna()
    _wei = _wei / _wei.median()

    # _wei = _wei.unstack(co.RL)
    # %%
    # %%
    def set_kmeans(n_c, _ser, _wei):
        #     n_c = 30
        kmeans = KMeans(n_c, random_state=388345)
        kmeans.fit(_ser, _wei)
        return kmeans

    # %%
    _dc = dscc[co.CLUS_LENGTH_DIM].to_dataframe()
    _dc[co.KMEAN_OBJ] = _dc.apply(
        lambda r: set_kmeans(r[co.CLUS_LENGTH_DIM], _ser, _wei), axis=1)
    _dc.drop(co.CLUS_LENGTH_DIM, axis=1, inplace=True)
    # %%
    dscc[co.KMEAN_OBJ] = _dc.to_xarray()[co.KMEAN_OBJ]
    # %%
    _kmeans = dscc[co.KMEAN_OBJ].to_series()
    # %%
    _dm = dscc[co.CONC_NORMALIZED].stack(
        {co.DUM_STACK: [co.R_CENTER, co.TH_CENTER, co.ZM]}).T
    # _dm = _dm.isel(dum=slice(None,4))
    _nas = []
    for i, ob in _kmeans.items():
        _na = xr.full_like(_dm, np.nan).sum(co.RL)
        _na.name = co.FLAG
        _na.values = ob.predict(_dm)
        _na = _na.expand_dims(**{co.CLUS_LENGTH_DIM: [i]}).unstack()
        _nas.append(_na)
    # %%
    _na = xr.concat(_nas, dim=co.CLUS_LENGTH_DIM)
    # %%
    try:
        dscc = dscc.drop(co.FLAG)
    except:
        pass
    dscc = xr.merge([dscc, _na])
    return dscc

def plot_sample_of_vectors_norm_used_for_clustering(dscc):
    global _df
    _col = co.CONC_NORMALIZED
    _df = dscc.where(dscc[co.LAB_CLUSTER_THRESHOLD])[_col].to_dataframe()[
        _col].dropna()
    _df = _df.unstack(co.RL)
    # %%
    _sam = _df.sample(frac=.001).T.plot(legend=False, alpha=.7,
                                        figsize=(10, 5))

def plot_cells_used_for_clustering(dscc):
    _ds = dscc[co.LAB_CLUSTER_THRESHOLD].to_dataframe()[
        co.LAB_CLUSTER_THRESHOLD].value_counts()
    _ds = 100 * _ds / _ds.sum()
    ax = _ds.plot.bar()
    ax.set_title('cells used for clustering');

def preprocess_dscc_for_clustering(MAX_LENGTH, dscc):
    co.CLUS_LENGTH_DIM
    dscc = dscc.assign_coords(**{co.CLUS_LENGTH_DIM: range(2, MAX_LENGTH)})
    # %%
    stack_dic = {co.DUM_STACK: [co.R_CENTER, co.TH_CENTER, co.ZM]}
    _norm = dscc[co.CONC].stack(**stack_dic)
    _norm_array, _norm_ret = preprocessing.normalize(_norm,
                                                     return_norm=True,
                                                     axis=0)
    _norm.values = _norm_array
    dscc[co.CONC_NORMALIZED] = _norm.unstack()
    _normed = _norm.mean(co.RL)
    _normed.name = co.CONC_NORMS
    _normed.values = _norm_ret
    _normed = _normed.unstack()
    dscc[co.CONC_NORMS] = _normed
    # dscc[co.CONC_NORMS] = dscc[co.CONC_NORMS].where(dscc[co.LAB_CLUSTER_THRESHOLD])
    # %%
    try:
        dscc = dscc.drop('quantile')
    except:
        pass
    return dscc

def print_percentage_res_time_mass_considered(dscc):
    # %%
    _res = (dscc[co.CONC].where(dscc[co.LAB_CLUSTER_THRESHOLD])).sum() / \
           dscc[co.CONC].sum()
    # %%
    print((100 * _res).item())

def rebuild_the_dscc(dfcc):
    global _df
    _df = dfcc
    dscc = _df[co.CONC].stack().to_xarray()
    dscc.name = co.CONC
    dscc = dscc.to_dataset()
    CLUSTER_THRESHOLD = .4
    co.LAB_CLUSTER_THRESHOLD = 'LAB_CLUSTER_THRESHOLD'
    co.CSUM = 'CONC_SUM'
    # %%
    dscc[co.CSUM] = dscc[co.CONC].sum(co.RL)
    # %%
    dscc[co.LAB_CLUSTER_THRESHOLD] = dscc[co.CSUM] > dscc[co.CSUM].quantile(
        CLUSTER_THRESHOLD)
    return dscc

def plot_hist_all_values(dfcc):
    f, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs = axs.flatten()
    plot_hist_all_log(dfcc, ax=axs[0])
    plot_hist_all_log(dfcc, cumulative=True, ax=axs[1])
    f: plt.Figure
    f.tight_layout()

def get_df_for_plot(_n, dscc):
    _d = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]
    _d = _d.drop([co.KMEAN_OBJ, co.CLUS_LENGTH_DIM])
    # _d = _d.where(_d[FLAG]==_f)
    # %%
    _s = _d[[co.CONC, co.FLAG]].to_dataframe()[[co.CONC, co.FLAG]]
    _ss = _s.groupby([co.RL, co.FLAG]).sum()
    # %%
    _ss1 = _ss.unstack(co.FLAG).resample('4H').mean()
    _ss1 = (100 * _ss1[co.CONC].T / _ss1.T.sum()).T
    # %%
    _ss1.plot(sharex=True, sharey=True, layout=(2, -1), subplots=True,
              figsize=(10, 5), color=ucp.cc);
    # %%
    _ss1.plot.area(legend=False, figsize=(12, 6), color=ucp.cc)
    # %%
    # %%
    _ss1 = _ss.unstack(co.FLAG)
    # %%
    _ss1 = _ss1.resample('m').median()
    # %%
    _ss1 = (100 * _ss1[co.CONC].T / _ss1.T.sum()).T
    return _ss1


def add_lat_lon_to_dscc(dscc, selfFLP):
    lcols = [*co.LL00, 'LON', 'LAT']
    _ds = selfFLP.merged_ds
    _ds = _ds[lcols]
    try:
        dscc = dscc.drop(lcols)
    except:
        pass
    try:
        dscc = xr.merge([dscc, _ds])
    except:
        pass
    # dscc = xr.merge([dscc,_ds])
    return dscc


def plot_hour_influence_targeted(_n, _nn, dscc, height_less_than,
                                 less_than, more_than):
    _ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]
    try: _ds = _ds.drop(co.KMEAN_OBJ)
    except: pass
    _dss = _ds.copy()
    _ds[co.CONC] = _ds[co.CONC].where(dscc[co.R_CENTER] < less_than,
                                      0).where(
        dscc[co.R_CENTER] > more_than, 0).where(
        dscc[co.ZM] < height_less_than, 0)
    _ds1 = _ds[[co.CONC, co.FLAG]]
    _dss1 = _dss[[co.CONC, co.FLAG]]
    _ds2 = _ds1.to_dataframe()
    _dss2 = _dss1.to_dataframe()
    _ds3 = _ds2[[co.CONC, co.FLAG]]
    _dss3 = _dss2[[co.CONC, co.FLAG]]
    _df = _ds3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],
                           drop=True).reset_index().set_index(
        [co.FLAG, co.RL])
    _dff = _dss3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],
                             drop=True).reset_index().set_index(
        [co.FLAG, co.RL])
    _df1 = _df.sort_index().groupby([co.FLAG, co.RL]).sum()
    _dff1 = _dff.sort_index().groupby([co.FLAG, co.RL]).sum()
    _df2 = _df1.unstack(co.FLAG)[co.CONC]
    _dff2 = _dff1.unstack(co.FLAG)[co.CONC]
    _df2 = 100 * (_df2.T / _dff2.T.sum()).T
    # %%
    _df3 = _df2.loc[:, _nn].copy()
    _df3.index = (_df3.index - pd.Timedelta(hours=4)).hour
    ax = _df3.sort_index().reset_index().boxplot(by=co.RL)
    ax.set_ylim(-.01, .5);
    # ax.set_yscale('log')
    # ax.set_title('')

def plot_target_distance_height_influence(_n, dscc, height_less_than,
                                          less_than, more_than):
    _ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]
    try: _ds = _ds.drop(co.KMEAN_OBJ)
    except: pass

    _dss = _ds.copy()
    _ds[co.CONC] = _ds[co.CONC].where(dscc[co.R_CENTER] < less_than,
                                      0).where(
        dscc[co.R_CENTER] > more_than, 0).where(
        dscc[co.ZM] < height_less_than, 0)
    _ds1 = _ds[[co.CONC, co.FLAG]]
    _dss1 = _dss[[co.CONC, co.FLAG]]
    _ds2 = _ds1.to_dataframe()
    _dss2 = _dss1.to_dataframe()
    _ds3 = _ds2[[co.CONC, co.FLAG]]
    _dss3 = _dss2[[co.CONC, co.FLAG]]
    _df = _ds3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],
                           drop=True).reset_index().set_index(
        [co.FLAG, co.RL])
    _dff = _dss3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],
                             drop=True).reset_index().set_index(
        [co.FLAG, co.RL])
    _df1 = _df.sort_index().groupby([co.FLAG, co.RL]).sum()
    _dff1 = _dff.sort_index().groupby([co.FLAG, co.RL]).sum()
    _df2 = _df1.unstack(co.FLAG)[co.CONC]
    _dff2 = _dff1.unstack(co.FLAG)[co.CONC]
    _df2 = 100 * (_df2.T / _dff2.T.sum()).T
    _df2.plot(subplots=True, figsize=(20, 20), sharey=True,
              color=[*ucp.cc, *ucp.cc]);

def plot_influences(_n, dscc):
    _ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]
    try: _ds = _ds.drop(co.KMEAN_OBJ)
    except: pass
    _dss = _ds.copy()
    _ds[co.CONC] = _ds[co.CONC]
    _ds1 = _ds[[co.CONC, co.FLAG]]
    _dss1 = _dss[[co.CONC, co.FLAG]]
    _ds2 = _ds1.to_dataframe()
    _dss2 = _dss1.to_dataframe()
    _ds3 = _ds2[[co.CONC, co.FLAG]]
    _dss3 = _dss2[[co.CONC, co.FLAG]]
    _df = _ds3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],
                           drop=True).reset_index().set_index(
        [co.FLAG, co.RL])
    _dff = _dss3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],
                             drop=True).reset_index().set_index(
        [co.FLAG, co.RL])
    _df1 = _df.sort_index().groupby([co.FLAG, co.RL]).sum()
    _dff1 = _dff.sort_index().groupby([co.FLAG, co.RL]).sum()
    _df2 = _df1.unstack(co.FLAG)[co.CONC]
    _dff2 = _dff1.unstack(co.FLAG)[co.CONC]
    _df2 = 100 * (_df2.T / _dff2.T.sum()).T
    _df2.plot(subplots=True, figsize=(20, 20), sharey=True,
              color=[*ucp.cc, *ucp.cc]);

def plot_dis_height_quantiles_chc(_n, dsF, dscc, axs=False):
    for _f in range(_n):
        plot_dis_height_quantiles_chc_single(_f, _n, dsF, dscc,axs=axs)


def plot_dis_height_quantiles_chc_single(_f, _n, dsF, dscc,axs=False):
    if axs is False:
        _, ax = plt.subplots()
    else:
        if type(axs)== np.ndarray:
            ax = axs[_f]
        else:
            ax = axs


    _cm = fa.get_custom_cmap([*ucp.cc, *ucp.cc, *ucp.cc][_f][:3])

    _ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]

    _ds = _ds.drop(co.KMEAN_OBJ)

    _ds = _ds.sum([co.RL])

    _ds1 = xr.merge([_ds, dsF[[co.TOPO]]]).where(_ds[co.FLAG] == _f)
    _ds1 = _ds1.swap_dims({co.R_CENTER: co.DIS})

    _ds2 = _ds1/dsF[co.ZLM]

    _ds3 = _ds2[co.CONC]
    zmin,zmax = _ds2[co.ZM].quantile([0,1])
    zz = np.arange(zmin,zmax,zmin)

    zl = zz[1]-zz[0]

    _ds4 = _ds3.interp(**{co.ZM:zz})*zl

    ZREAL = 'ZREAL'
    _ds4[ZREAL]=_ds4*0+_ds4[co.ZM]+((_ds4[co.TOPO]/zl).round()*zl)

    _dims = set(_ds4.dims)

    _keep = _dims.union(set([ZREAL]))

    _coor = set(_ds4.coords)

    _drop = list(_coor-_keep)

    _ds5=_ds4.drop(_drop).to_dataframe()

    _ds6 = _ds5.reset_index().groupby([ZREAL,co.DIS,co.TH_CENTER]).sum()[[co.CONC]].to_xarray()

    _ds6.sum(co.TH_CENTER)[co.CONC].plot(xscale='log',vmin=0,ax=ax,cmap=_cm)

    HEIGHT = 'HEIGHT'
    _ds1[HEIGHT] = (_ds1[co.TOPO] + _ds1[co.ZM])

    _dg = _ds1[[HEIGHT, co.CONC]].to_dataframe()[[HEIGHT, co.CONC]]
    _dg = _dg.groupby(co.DIS)

    _dh = (_ds1[co.CONC] * (_ds1[co.TOPO] + _ds1[co.ZM])).mean(
        [co.TH_CENTER, co.ZM])
    _dh = _dh / (_ds1[co.CONC].mean([co.TH_CENTER, co.ZM]))

    ax.set_xlim(10, 2e3)

    _dh = (_ds1[co.CONC] * (_ds1[co.TOPO])).mean([co.TH_CENTER, co.ZM])
    _dh = _dh / (_ds1[co.CONC].mean([co.TH_CENTER, co.ZM]))

    _dh.plot(x=co.DIS, color='k', ax=ax)
    ax.set_xscale('log')

    ax.set_xlim(5, 2e3)
    ax.set_ylim(0, 1.5e4)
    ax.set_title(str(_f))
    ax.set_xlabel('Radial distance from CHC [km]')
    ax.set_ylabel('Height [masl]')
    ax.grid(color='k',alpha=.3,linestyle='--')
    ax.set_axisbelow(False)
    ax.set_facecolor('white')
    ax:plt.Axes = ax
    ax.scatter(5.2,5200, color='red')
    ax.text(6,5200,'CHC')

def add_dis_km_dscc(dscc):
    _km = dscc[co.R_CENTER] * 100
    _km.name = co.DIS
    dscc = dscc.assign_coords(**{co.DIS: _km})
    return dscc

def plot_distance_height_chc(_n, dscc):
    for _f in range(_n):
        # ax = fa.get_ax_bolivia()
        #     ax.set_title(str(_f))
        _ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]
        _ds = _ds.drop(co.KMEAN_OBJ)
        _ds = _ds.where(_ds[co.FLAG] == _f)
        _ds = _ds.sum([co.RL, co.TH_CENTER])

        _ds = _ds[[co.CONC]]

        _cm = fa.get_custom_cmap([*ucp.cc, *ucp.cc, *ucp.cc][_f][:3])

        _km = _ds[co.R_CENTER] * 100

        DIS = 'Distance [km]'
        _km.name = DIS

        _ds = _ds.assign_coords(**{DIS: _km})
        _, ax = plt.subplots()
        _ds[co.CONC].plot(x=DIS, cmap=_cm, ax=ax)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlim(10, 2e3)
        ax.set_ylim(25e1, 2e4)
        ax.set_title(str(_f));

def plot_clust_bolivia_individual(_n, dscc):
    for _f in range(_n):
        ax = fa.get_ax_bolivia()
        ax.set_title(str(_f))
        _ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]
        _ds = _ds.drop(co.KMEAN_OBJ)
        _ds = _ds.where(_ds[co.FLAG] == _f)
        _ds = _ds.sum([co.RL, co.ZM])

        _ds = _ds[[co.CONC]]

        _cm = fa.get_custom_cmap([*ucp.cc, *ucp.cc, *ucp.cc][_f][:3])

        fa.logpolar_plot(_ds, ax=ax, patch_args={'cmap': _cm},
                         colorbar=False)

def plot_clust_in_lapaz(_n, dscc):
    for _f in range(_n):
        ax = fa.get_ax_lapaz()
        ax.set_title(str(_f))
        _ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}][
            {co.R_CENTER: slice(1, 23)}]
        _ds = _ds.drop(co.KMEAN_OBJ)
        _ds = _ds.where(_ds[co.FLAG] == _f)
        _ds = _ds.sum([co.RL, co.ZM])

        _ds = _ds[[co.CONC]]

        _cm = fa.get_custom_cmap([*ucp.cc, *ucp.cc, *ucp.cc][_f][:3])

        if _ds[co.CONC].max().item() != 0:
            fa.logpolar_plot(_ds, ax=ax, patch_args={'cmap': _cm},
                             colorbar=False)
        fa.add_chc_lpb(ax)

def plot_clust_in_bolivia(_n, dscc):
    ax = fa.get_ax_bolivia()
    _f = 2
    for _f in range(_n):
        _ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]
        _ds = _ds.drop(co.KMEAN_OBJ)
        _ds = _ds.where(_ds[co.FLAG] == _f)
        _ds = _ds.sum([co.RL, co.ZM])

        _ds = _ds[[co.CONC]]

        _cm = fa.get_custom_cmap(ucp.cc[_f][:3])

        fa.logpolar_plot(_ds, ax=ax, patch_args={'cmap': _cm},
                         colorbar=False)
