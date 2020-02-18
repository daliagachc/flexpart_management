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
from flexpart_management.notebooks.george_data_analysisV02.correlate_isoprene_clusters_lfc import *

# local functions and constants


# %%
from flexpart_management.notebooks.george_data_analysisV02.correlate_isoprene_clusters_lfc import \
    log_his_series


def main():
    # %%
    ds = fa.open_temp_ds('ds_clustered_18.nc')
    ts = pd.read_excel(pjoin(co.tmp_data_path, 'data_george_cc.xlsx'),
                       sheet_name=1, skiprows=1)
    # %%
    cs = pd.read_csv(pjoin(co.tmp_data_path, 'conc_ts_cluster.csv')).set_index(
        'releases')
    utc = 'time_utc'
    cs.index.name = utc
    # %%
    # %%

    c9, c6, c4 = 'C9_C13_compounds', 'C6_C8_compounds', 'C4_C5_compounds'
    c46 = 'c4/c6'
    ts[c46] = ts[c4] / ts[c6]

    ts.loc[ts[c9] < 1e4, c9] = 1e4

    # %%
    ts['jan'] = ts[utc].dt.month == 1
    day_bool = \
        (ts[utc].dt.hour > 12) \
        & (ts[utc].dt.hour <= 23)
    ts['night'] = day_bool
    ts['jan night'] = ts['night'] & ts['jan']
    ts['all'] = True

    # %%
    cols = [c4, c6, c9]
    cc = c4
    plot_row(c4, ts)
    # %%
    plot_row(c6, ts, bmin=2e4, bmax=3e7)

    # %%
    plot_row(c9, ts, bmin=2e4, bmax=2e7)

    # %%

    interactive_plot(c4, c46, c6, c9, ts)

    # %%
    tsr = ts.copy()

    tsr = tsr.set_index(utc)
    # tsrl: pd.DataFrame = np.log(tsr[cols])
    tsrl: pd.DataFrame = tsr[cols]
    tsrl[c46] = tsr[c46]
    tsrl = tsrl.resample('1H').mean()
    # %%
    tsm = pd.merge(tsrl, cs, left_index=True, right_index=True)
    tsm.dropna(axis=1, how='any')
    tsm: pd.DataFrame
    # %%
    corr = tsm.corr(method='spearman')

    f, ax = plt.subplots(figsize=(15, 5))
    sns.heatmap(
        corr.loc[tsrl.columns, cs.columns],
        ax=ax, square=True, annot=True,
        cmap='RdBu_r', center=0)

    for item in ax.get_yticklabels():
        item.set_rotation(0)
    ax.figure.tight_layout()
    x1, x2 = ax.get_xlim()
    ax.set_xlim(x1 - .5, x2 + .5)
    x1, x2 = ax.get_ylim()
    ax.set_ylim(x1 + .5, x2 - .5)
    plt.show()
    # %%

    _boo = (tsm >= 0).all(axis=1) & (tsm < np.inf).all(axis=1)
    # %%

    for c in cs.columns:
        com_cols = [c4, c46, c6, c9, c]
        sns.pairplot(tsm[_boo][com_cols][:])
        plt.show()
    # %%
    import scipy.optimize.nnls as nnls
    tsm_boo = tsm[_boo]
    # noinspection PyCallingNonCallable
    res,err = nnls(
        tsm_boo[cs.columns],
        tsm_boo[c4], #- tsm_boo[c4].min(),
        maxiter = 10 * tsm_boo.shape[1]

    )
    nn = pd.Series(res,index=cs.columns)/res.sum()
    nn = pd.DataFrame(nn,columns=['res'])
    nn['tot'] = tsm_boo.mean()
    nn['tot'] = nn['tot']/nn['tot'].sum()
    nn['mult'] = nn['tot']*nn['res']
    nn['mult'] = nn['mult']/nn['mult'].sum()

    # %%
    nn.plot.barh()
    plt.show()
    # %%
    tsm_boo['mod_c4']=(nn['res'] * tsm_boo[cs.columns]).sum(axis=1)
    # %%
    tsm_boo.plot.scatter(x=c4,y='mod_c4')
    plt.show()
    # %%
    wmr = 'water mixing ratio'
    # wmr = 'BC'
    interactive_plot_bok(df = ts, col=wmr,
                         time_col=utc, fig_kw={'y_axis_type': 'linear'})
    # %%
    _ts = ts.set_index(utc)[[wmr]].resample('10T').mean()
    _ts.plot(figsize=(10, 5))
    plt.tight_layout()
    plt.show()
    # %%
    tm_wmr = pd.merge(cs, ts.set_index(utc)[wmr], left_index=True, right_index=True)
    tm_wmr = tm_wmr.dropna()
    ccols = cs.columns
    res,err = nnls(tm_wmr[ccols],tm_wmr[wmr])
    res = pd.Series(res,index=ccols)
    res = pd.DataFrame(res,columns=['res'])
    # %%
    res['mult'] = (res['res']*tm_wmr[ccols]).sum()
    res['inf'] = tm_wmr[ccols].sum()
    (res/res.sum()).plot.barh(figsize=(8,10))
    plt.show()
    # %%
    # tm_wmr[['07_SR',wmr]].plot.scatter(x='07_SR',y=wmr)
    # g = sns.jointplot(
    #     '07_SR', wmr, data=tm_wmr, kind="kde", height=7, space=0,
    #
    # )
    import matplotlib.colors
    clab = '07_SR'
    for clab in ccols:
        sns.kdeplot(tm_wmr[clab], tm_wmr[wmr],
                    # cmap='RdBu',
                    # norm=matplotlib.colors.LogNorm(vmin=1,vmax=1e10),
                    cbar=True,
                    levels = np.geomspace(.001,.2,10),
                    shade=True,
                    )
        plt.show()
    # %%

    tm_wmr:pd.DataFrame
    cr = (tm_wmr.corr('spearman') * 100).astype(int)
    cr = cr.loc[[wmr],ccols]
    # sns.heatmap(cr,square=True,annot=True)
    cr.T.sort_values(wmr).plot.barh()
    plt.gca().set_xlabel('Spearman rank correlation')
    plt.show()

    # %%
    from sklearn.preprocessing import QuantileTransformer as QT
    x = QT().fit_transform(tm_wmr[[wmr]])[:,0]
    y = QT().fit_transform(tm_wmr[['08_SM']])[:,0]
    f, ax = plt.subplots(figsize=(8,6))
    res = ax.hexbin(x,y,gridsize=5,cmap=plt.get_cmap('Reds'))
    f:plt.Figure
    f.colorbar(res,ax=ax)
    f, ax = plt.subplots()
    sns.kdeplot(x,y,ax=ax,shade=True)



    plt.show()


    # %%
    bcts = ts[['BC']].copy()

    # %%

    wrf_ds = xr.open_dataset(
        '/Users/diego/flexpart_management/flexpart_management'
        '/requests/george/data'
        '/time_series_for_selected_values_at_chc_wrf.nc'
    )

    # %%
    qvapor = 'QVAPOR'
    mwrfts = plot_corr_wrf_mea(qvapor, wmr, wrf_ds, ts)
    # %%

    mwrfts = plot_corr_wrf_mea('rh', 'RH_station', wrf_ds, ts,mult=1)
    # %%
    mwrfts = plot_corr_wrf_mea('theta_e', 'Equivalent potential temperature', wrf_ds, ts,mult=1)
    # %%
    ts['temp_st'] = ts['Temperature_station'] +273.15
    mwrfts = plot_corr_wrf_mea('temp', 'temp_st', wrf_ds, ts,mult=1)
    # %%


    sns.regplot(x=qvapor, y=wmr, data=mwrfts)
    plt.show()



    pass


