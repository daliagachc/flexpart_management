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
from flexpart_management.notebooks.sulfate_volcano_chc.n02_regressors.n02_regressors_lfc import *

import \
    flexpart_management.notebooks.sulfate_volcano_chc.n02_regressors.n02_regressors_lfc as lfc

# %%
from flexpart_management.notebooks.sulfate_volcano_chc.n02_regressors.n02_regressors_lfc_1 import \
    get_source_fit
from sklearn.preprocessing import QuantileTransformer as QT


# %%
def main():
    # %%
    clus_cols, ts_merged = import_merged_data()
    var = 'Organics'
    ts: pd.Series = ts_merged[var]
    _w = 1
    ts_merged[var] = ts.rolling(
        _w,
        center=True,
        min_periods=1,
        win_type='gaussian'
    ).mean(std=_w)
    get_source_fit(clus_cols=clus_cols,
                   var_name=var,
                   ts_merged_in=ts_merged,
                   orig_interval='1H'
                   )

    # %%
    col_ind: pd.Series = pd.Series(clus_cols).reset_index(name='sn').set_index(
        'sn')
    col_ind = col_ind['index'].apply(lambda i: ucp.cc[i])

    # %%
    # _v=ts_merged['07_SR'].dropna()
    df = ts_merged[clus_cols].unstack()
    df.name = 'val'
    df = df.reset_index()
    bins = np.geomspace(.1, 100, 15)
    bins = [0, *bins[1:]]
    g = sns.FacetGrid(
        data=df, col='level_0', col_wrap=6,
        # sharex=False,
        sharey=False,
    )
    res = g.map(
        sns.distplot,
        'val',
        kde=False,
        norm_hist=False,
        # bins=bins,
        bins=10

    )
    # res.set(xscale='log')
    # res.set(xlim=(.1,100))
    # res.set(ylim=(1, 10000))
    # res.set(yscale='log')
    plt.show()
    # %%
    # %%
    # _v=ts_merged['07_SR'].dropna()
    df_mod = ts_merged[clus_cols].copy()
    from sklearn.preprocessing import PowerTransformer, MinMaxScaler
    pt = PowerTransformer(standardize=True)
    for l in df_mod.columns:
        tr_1 = pt.fit_transform(df_mod[[l]])
        tr2 = MinMaxScaler().fit_transform(tr_1)
        df_mod[l] = tr2
    # %%

    df = df_mod.unstack()
    df.name = 'val'
    df = df.reset_index()
    bins = np.geomspace(.1, 100, 15)
    bins = [0, *bins[1:]]
    g = sns.FacetGrid(
        data=df, col='level_0', col_wrap=6,
        # sharex=False,
        sharey=False,
    )
    res = g.map(
        sns.distplot,
        'val',
        kde=False,
        norm_hist=False,
        # bins=bins,
        bins=10

    )
    # res.set(xscale='log')
    # res.set(xlim=(.1,100))
    # res.set(ylim=(1, 10000))
    # res.set(yscale='log')
    plt.show()
    # %%
    val = ts_merged['Sulfate']
    val = val[val >= 0]
    plot_var_dis_trans(val)
    # %%
    ts_merged: pd.DataFrame
    vars = 'Nitrate', 'Sulfate', 'Ammonium', 'Chloride', 'Organics'
    for var in vars:
        lfc.source_region_plot(clus_cols, col_ind, ts_merged, var,
                               fit_intercept=True
                               )

    # %%
    iso_ts = fa.open_iso_ts()
    iso_ts = iso_ts.resample('1H').mean()
    clus_ts = lfc.get_clust_ts()
    # %%
    # var = 'C4_C5_compounds'
    var = 'BC'
    # var = 'C6_C8_compounds'
    # var ='C9_C13_compounds'
    var_na = iso_ts[var].dropna()
    var_na.resample('H').mean().plot()
    plt.show()
    # %%

    # var_na = var_na[var_na>=0]
    # bc = lfc.minmax(lfc.pt(var_na))
    var_na.name = var

    mtd = pd.merge(clus_ts, var_na, left_index=True, right_index=True)

    lfc.plot_var_dis_trans(var_na)
    plt.show()

    lfc.source_region_plot(
        clus_cols, col_ind, mtd, var,
        fit_intercept=True,
        start=.001,
        max_iter=1e4
    )

    plt.show()

    # %%
    f, ax = plt.subplots()
    ax: plt.Axes
    # ax.scatter(
    #     y=iso_ts['RH_station'],
    #     x=iso_ts['BC'],
    #      marker='o', facecolors='none',
    #     edgecolors='k',
    #     alpha=.5
    # )
    bc_ = iso_ts[['RH_station', 'BC']].copy()
    bc_['BC_log'] = np.log(bc_['BC'])
    sns.kdeplot(
        data = bc_[['RH_station', 'BC_log']],
        # y='RH_station',
        # x='BC',
        # marker='o', facecolors='none',
        # edgecolors='k',
        # alpha=.5
        shade=True,
        ax=ax
    )
    # ax.set_yscale('log')
    # ax.set_ylim(10, 500)
    plt.show()
    # %%

    np_bc_ = ['NP', 'BC']
    _df = np.log(iso_ts[np_bc_].dropna())


    f, ax = plt.subplots()
    ax:plt.Axes
    sns.kdeplot(
        data2=_df['NP'],
        data=_df['BC'],
        ax=ax,
        shade=True
                )

    ax.scatter(
        y=_df['NP'],
        x=_df['BC'],
        alpha=.5,
        marker='.',
        s=1,
        c='k',
    )
    ax.set_xlim(2,8.5)
    ax.set_ylim(10,17)
    plt.show()

    _df:pd.DataFrame
    print(np.power(_df.corr(),2))
    print(np.power(iso_ts[np_bc_].corr(),2))

    sns.jointplot(
        x=_df['NP'],
        y=_df['BC'],
        kind='scatter',
        # marker = ',',
        joint_kws={'s':1,'marker':',','alpha':.5}
    )
    plt.show()


