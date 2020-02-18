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
from flexpart_management.modules import constants as co
from flexpart_management.modules import flx_array as fa
plt;
# %%
def import_merged_data():
    path = 'CHC_QACSM.xlsx'
    path = pjoin(co.tmp_data_path, path)
    acsm = pd.read_excel(path)
    acsm = acsm.set_index('Date UTC')
    acsm = acsm[1:]
    # acsm = acsm['2018-04-01':]
    acsm = acsm.resample('1H').median()
    acsm.index.name = co.RL
    # %%
    clus_ts = pd.read_csv(pjoin(co.tmp_data_path, 'conc_ts_cluster.csv'))
    clus_ts = clus_ts.set_index(co.RL)
    # %%
    clus_cols = clus_ts.columns
    # %%
    ts_merged = pd.merge(clus_ts, acsm, left_index=True, right_index=True)
    ts_merged = ts_merged[~ts_merged['Sulfate'].isna()]
    return clus_cols, ts_merged

# %%
def get_clus_norm(clus_cols, ts_merged):
    ts_merge_clus = ts_merged[clus_cols]
    ts_merge_clus = ts_merge_clus / ts_merge_clus.mean()
    return ts_merge_clus

    # %%
import sklearn.preprocessing as pre
def sqrt_norm(val_ser):
    n_val = np.sqrt(np.abs(val_ser))
    # n_val = pre.StandardScaler()
    n_val_ser = pd.Series(n_val,index=val_ser.index)
    return n_val_ser

def non_log(val_ser):
    mmin = val_ser[val_ser>0].min()
    n_val = val_ser.copy()
    n_val[n_val>=mmin] =  mmin
    n_val = np.sqrt(np.abs(val_ser))
    # n_val = pre.StandardScaler()
    n_val_ser = pd.Series(n_val,index=val_ser.index)
    return n_val_ser

def stnd(val_ser):
    resh = val_ser.values.reshape(-1,1)
    n_val = pre.StandardScaler().fit_transform(resh)
    # print(n_val)
    n_val_ser = pd.Series(n_val[:,0],index=val_ser.index)
    return n_val_ser

def qt(val_ser):
    resh = val_ser.values.reshape(-1,1)
    n_val = pre.QuantileTransformer().fit_transform(resh)
    # print(n_val)
    n_val_ser = pd.Series(n_val[:,0],index=val_ser.index)
    return n_val_ser
# %%
def qtn(val_ser):
    resh = val_ser.values.reshape(-1,1)
    n_val = pre.QuantileTransformer(
        output_distribution='normal').fit_transform(resh)
    # print(n_val)
    n_val_ser = pd.Series(n_val[:,0],index=val_ser.index)
    return n_val_ser

def pt(val_ser):
    resh = val_ser.values.reshape(-1,1)
    n_val = pre.PowerTransformer().fit_transform(resh)
    # print(n_val)
    n_val_ser = pd.Series(n_val[:,0],index=val_ser.index)
    return n_val_ser

# %%
def minmax(val_ser):
    resh = val_ser.values.reshape(-1,1)
    n_val = pre.MinMaxScaler().fit_transform(resh)
    # print(n_val)
    n_val_ser = pd.Series(n_val[:,0],index=val_ser.index)
    return n_val_ser

def robust(val_ser):
    resh = val_ser.values.reshape(-1,1)
    n_val = pre.RobustScaler().fit_transform(resh)
    # print(n_val)
    n_val_ser = pd.Series(n_val[:,0],index=val_ser.index)
    return n_val_ser

# %%
def plot_var_dis_trans(val:pd.Series):
    f, axs = plt.subplots(
        3, 3, sharex=True
    )
    axf = axs.flatten()
    funs = dict(
        none=lambda x: x,
        non_log=non_log,
        sqrt_norm=sqrt_norm,
        stnd=stnd,
        qt=qt,
        qtn=qtn,
        pt=pt,
        minmax=minmax,
        robust=robust

    )
    for ax, (k, fun) in zip(axf, funs.items()):
        sns.distplot(
            minmax(fun(val.dropna())),
            ax=ax,
        )
        ax.set_title(k)
        ax.set_xlabel(None)
        ax.set_xlim(0, 1)
        # ax.set_yscale('log')
    f:plt.Figure
    f.suptitle(val.name,y=.999)
    # f.tight_layout(pad=100)

    plt.show()

# %%

def reverse_legend(ax):
    leg_han = ax.get_legend_handles_labels()
    [l.reverse() for l in leg_han]
    ax.legend(*leg_han)

def source_region_plot(clus_cols,
                       col_ind, ts_merged,
                       var,
                       fit_intercept=True,
                       start=.001,
                       max_iter=1000
                       ):
    merged = ts_merged[ts_merged[var] > 0]
    pt_ts = merged.apply(pt).apply(minmax)
    pt_ts[[var]].plot()
    plt.show()

    import sklearn.linear_model as lm
    from scipy.optimize import nnls
    one = pd.DataFrame(data=1, index=pt_ts.index, columns=['one'])
    fit_dic = {}
    area_df = pd.DataFrame()
    # a = .0001
    a_list = np.geomspace(start, 1, 60)
    a_list = [*a_list]
    for a in a_list:
        md = lm.Lasso(
            alpha=a, positive=True, fit_intercept=fit_intercept,
            max_iter=max_iter

        )
        md.fit(pt_ts[clus_cols], pt_ts[var])
        r_2 = md.score(pt_ts[clus_cols], pt_ts[var])
        coef = md.coef_
        ser = pd.Series(coef, index=clus_cols, name=a)
        area_df[a] = ser
        fit_dic[a] = dict(r_2=r_2, coef=coef)
    f, ax = plt.subplots()
    ax: plt.Axes
    index = area_df.sum(axis=1).sort_values(ascending=False).index
    # index = index[::-1]
    _df = area_df.loc[index].T
    _df = _df[_df.sum(axis=1) > 0]
    _df = (_df.T / _df.sum(axis=1)).T
    # _df = _df /_df.sum(axis=0)
    bool = area_df.sum(axis=1) > 0
    _df.loc[:, bool].plot.area(ax=ax, legend=True, color=col_ind.loc[index])
    reverse_legend(ax)

    ax.set_xscale('log')
    ax.set_title(var)
    ax.set_ylim(0, 1)
    ax.set_xlabel('alpha')
    ax.set_ylabel('Cluster [%]')
    rdf = pd.DataFrame(fit_dic).T['r_2']
    rdf = rdf[rdf > 0]
    axt = ax.twinx()
    rdf.plot(ax=axt, color='k')
    axt.set_ylim(0, axt.get_ylim()[1])
    axt.set_ylabel('$R^2$')
    plt.show()
    # return lm, pt_ts

def get_clust_ts():
    clus_ts = pd.read_csv(pjoin(co.tmp_data_path, 'conc_ts_cluster.csv'))
    clus_ts = clus_ts.set_index(co.RL)
    clus_ts.index = pd.to_datetime(clus_ts.index)
    return clus_ts
