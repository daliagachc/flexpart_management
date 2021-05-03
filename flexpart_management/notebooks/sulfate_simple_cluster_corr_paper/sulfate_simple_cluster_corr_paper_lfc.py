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

plt;
# %%

from scipy.odr import Model, Data, ODR
from scipy.stats import linregress
import numpy as np


def orthoregress(x, y):
    """Perform an Orthogonal Distance Regression on the given data,
    using the same interface as the standard scipy.stats.linregress function.
    Arguments:
    x: x data
    y: y data
    Returns:
    [m, c, nan, nan, nan]
    Uses standard ordinary least squares to estimate the starting parameters
    then uses the scipy.odr interface to the ODRPACK Fortran code to do the
    orthogonal distance calculations.
    """
    linreg = linregress(x, y)
    mod = Model(f)
    dat = Data(x, y)
    od = ODR(dat, mod, beta0=linreg[0:2])
    out = od.run()

    return list(out.beta) + [np.nan, np.nan, np.nan]


def f(p, x):
    """Basic linear regression 'model' for use with ODR"""
    return (p[0] * x) + p[1]


def get_lab_df(ds, lab_name, *, zM):
    # %%
    # zM=3
    ds_ = ds[[co.CONC, lab_name]][{co.ZM: slice(0, zM)}]
    # %%
    labs = np.unique(ds[lab_name][{co.RL: 0}])
    labs = list(set(labs) - {'nan'})
    labs.sort()

    # %%
    ll = []
    for l in labs:
        r = ds_[co.CONC].where(ds_[lab_name] == l).sum(
            [co.TH_CENTER, co.R_CENTER, co.ZM])
        r.name = l
        ll.append(r)
    lld = xr.merge(ll)
    df = lld.to_dataframe()

    # %%
    # %%

    # df = ds_.to_dataframe()
    return df


def plot_fig_comparison(_dic, cols, dj3, sul):
    f = plt.figure(dpi=300, figsize=(7.25, 6), constrained_layout=True)
    gs = plt.GridSpec(6, 3, figure=f)
    ax1 = f.add_subplot(gs[-2, :])
    tax = f.add_subplot(gs[-1, :])
    axp = f.add_subplot(gs[:4, 0])
    axp: plt.Axes
    dfp = _dic[('tot', 'pearson')][sul][cols]
    c9 = ucp.cb[1]
    c10 = ucp.cb[4]
    dfc = dfp.copy()
    dfc = dfc.apply(lambda x: (.5, .5, .5, 1))
    dfc.loc['09_MR'] = c9
    dfc.loc['10_SR'] = c10
    axp.barh(dfp.index, dfp, zorder=100, color=dfc, height=.6)
    axp.tick_params(axis='y', labelcolor=(.5, .5, .5), labelsize=7,
                    color=(0, 0, 0, 0))
    axp.set_title('Pearson correlation coefficient', size=8)
    axp.set_xlim(-.4, .4)
    sns.despine(ax=axp, left=True)
    axp.grid(True, linestyle='--', alpha=.5, axis='y', zorder=0)
    dj_ = dj3[dj3[sul] < 6]
    lin_df = dj_.resample('H').mean()
    # ax1 = s.axf[0]
    lin_df[[sul]].plot(linewidth=.7, marker=',', ax=ax1, color=[ucp.cb[0]],
                       legend=False)
    ops_ = dict(offset={'left': 5, 'bottom': 4}, trim=False)
    ax1.set_xticks([])
    # ax1.set_xticks([],minor=True)
    ax1.set_xlabel(None)
    ax1.set_ylabel(r'$\mathrm{SO}_4\ [\mathrm{\mu}  \mathrm{m}^{-3}]$')
    ax1.set_ylim(0, 6)
    ax1.set_yticks([0, 2, 4, 6])
    ax1.set_yticklabels([0, 2, 4, None])
    sns.despine(ax=ax1, bottom=True, **ops_)
    ax1.grid(True, which='minor', axis='x', linestyle='--')
    # tax = s.ax.twinx()
    # tax = s.axf[1]
    sr_ = lin_df[['09_MR', '10_SR']]
    sr_: pd.DataFrame = sr_ / sr_.mean()
    sr_.plot(ax=tax, legend=False, linewidth=.7, color=[c9, c10])
    tax.set_xlabel(None)
    tax.set_ylabel(r'$\mathrm{SRR}\,/\,\overline{\mathrm{SRR}}$')
    tax.set_ylim(0, 6)
    tax.set_yticks([0, 2, 4, 6])
    tax.set_yticklabels([0, 2, 4, None])
    # tax.set_yticks([1,3,5],minor=True)
    sns.despine(ax=tax, **ops_)
    tax.grid(True, which='minor', axis='x', linestyle='--')
    f.subplots_adjust(hspace=.1)
    f.tight_layout()
    plt.show()


def plot_corrs(_dic, cols, sul):
    s = splot(2, 3, figsize=(8, 10), dpi=300, sharey=True, sharex=True)
    # cors = [ken,spe,pea]
    for i, (l, corr) in enumerate(_dic.items()):
        corr[sul][cols].plot.barh(ax=s.axf[i])
        s.axf[i].set_title(l)
        pass
    s.f.tight_layout()
    plt.show()
    return s


def get_corrs(acsm, ds, lab_name, sul):
    df3 = get_lab_df(ds, lab_name, zM=4)
    df33 = get_lab_df(ds, lab_name, zM=None)
    # %%
    dj = df3.join(acsm, how='inner')
    df4 = dj[df3.columns]
    dj3 = df33.join(acsm, how='inner')
    df44 = dj3[df33.columns]
    ac = dj[[sul]].copy()
    ac.loc[ac[sul] <= 0, sul] = .001
    # %%
    cols = df4.columns
    cors = []
    meths = 'spearman', 'pearson', 'kendall'
    arrs = {'surf': dj, 'tot': dj3}
    _dic = {}
    for la, dj in arrs.items():
        _dj = dj[[*cols, sul]]
        for meth in meths:
            _res = _dj.corr(method=meth)
            _dic[(la, meth)] = _res
    return _dic, cols, dj3


def plot_distributions(acsm, sul):
    f, axs = plt.subplots(2, 2, dpi=300)
    f: plt.Figure
    sul_ = acsm[sul]
    sul_[sul_ <= 0] = 0.01
    sul_.plot(ax=axs[0, 0])
    from sklearn.preprocessing import PowerTransformer, QuantileTransformer
    spt = PowerTransformer(standardize=False).fit_transform(acsm[[sul]])
    spt2 = PowerTransformer(standardize=True, method='box-cox').fit_transform(
        acsm[[sul]])
    sns.distplot(sul_, ax=axs[1, 0])
    axs[1, 0].set_title('normal')
    sns.distplot(spt, ax=axs[1, 1])
    axs[1, 1].set_title('power transform')
    sns.distplot(spt2, ax=axs[0, 1])
    axs[0, 1].set_title('power transform Box-Cox')
    f.tight_layout()
    plt.show()


def get_acsm_data():
    path = 'CHC_QACSM.xlsx'
    path = pjoin(co.tmp_data_path, path)
    acsm = pd.read_excel(path)
    acsm = acsm.set_index('Date UTC')
    acsm = acsm[1:]
    # acsm = acsm['2018-04-01':]
    acsm = acsm.resample('1H').median()
    acsm.index.name = co.RL
    return acsm


# %%

def get_dcc(ds):
    dsn = xr.open_mfdataset(pjoin(co.tmp_data_path, 'new_log_pol_ds_agl.nc'),
                            combine='nested', concat_dim=co.RL)
    dsn['lab_name'] = ds['lab_name'][{co.R_CENTER: slice(0, 30)}]
    dsn['lab_name'].values = ds['lab_name'][{co.R_CENTER: slice(0, 30)}].values
    dsn['lab_nc06'] = ds['lab_nc06'][{co.R_CENTER: slice(0, 30)}]
    dsn['lab_nc06'].values = ds['lab_nc06'][{co.R_CENTER: slice(0, 30)}].values
    dcc = dsn[['CONC']].where(dsn['lab_nc06'] == '08_PW').sum(
        [co.RL, co.ZM]).load()
    return dcc, dsn


def get_dfs(_dic, _dic6, sul):
    cols18 = co.DIC_186['18_NC']
    cols6 = co.DIC_186['06_NC']
    df6 = _dic6[('tot', 'pearson')].loc[sul, cols6]
    df6.name = 'corr6'
    df18 = _dic[('tot', 'pearson')].loc[sul, cols18]
    df18.name = 'corr18'
    df18.index.name = '18_NC'
    df18 = df18.reset_index()
    df6.index.name = '06_NC'
    df6 = df6.reset_index()
    df6['color'] = df6['06_NC'].apply(lambda x: co.pw_col_dict[x])
    white_lines = df6.reset_index().groupby('06_NC')['index'].max() + .5
    white_lines = white_lines[:-1]
    ticks = df6.reset_index().groupby('06_NC')['index'].mean().reset_index()
    ticks['color'] = ticks['06_NC'].apply(lambda x: co.pw_col_dict[x])

    def _fun(x):
        dic = {1: 'right', -1: 'left'}
        return dic[np.sign(x)]

    df18['ha'] = df18['corr18'].apply(_fun)
    df18['color'] = df18['corr18'].apply(lambda x: [[0, 0, 0, .5]])
    c9 = ucp.cb[1]
    c10 = ucp.cb[4]
    df18 = df18.set_index('18_NC')
    df18.loc['09_MR', 'color'] = [[[*c9, 1]]]
    df18 = df18.reset_index()
    return df18, df6, ticks, white_lines


def plot_fig_corr_s04(_dic, cols, dcc, df18, df6, dj18, dj6, sul, ticks,
                      white_lines, dsn):
    f: plt.Figure = plt.figure(dpi=300, figsize=(7.25, 6),
                               constrained_layout=True)
    gs = plt.GridSpec(6, 3, figure=f)
    ax1 = f.add_subplot(gs[-2, :])
    tax = f.add_subplot(gs[-1, :])
    axf_: plt.Axes = f.add_subplot(gs[:4, 0])
    axf_.barh(df6.index, df6['corr6'], height=1, color=df6['color'], alpha=.7)
    for _y in white_lines.values:
        axf_.axhline(y=_y, color='w', linewidth=2)
    axf_.barh(df18.index, df18['corr18'],
              # color=[[0, 0, 0, .3]],
              color=df18['color'].apply(lambda x: x[0]),
              height=.7)
    r9 = df18.reset_index().set_index('18_NC').loc['09_MR']
    axf_.text(r9['corr18'], r9['index'], f'{r9["corr18"]:0.1f} ', color='w',
              horizontalalignment=r9['ha'],
              verticalalignment='center',
              size=6
              )
    axf_.set_yticks([])
    for l, r in ticks.iterrows():
        axf_.text(-.4, r['index'], r['06_NC'],
                  horizontalalignment='right',
                  verticalalignment='center',
                  color=r['color'],
                  weight='bold',
                  size=7
                  )
    for l, r in df18.reset_index().iterrows():
        axf_.text(-np.sign(r['corr18']) * .01, r['index'], r['18_NC'],
                  horizontalalignment=r['ha'],
                  verticalalignment='center',
                  color=r['color'][0],
                  # weight='bold',
                  size=6
                  )
    axf_.set_xlim(-.4, .4)
    axf_.set_xticks([-.4, -.2, 0, .2, .4])
    sns.despine(ax=axf_, bottom=True, left=True, trim=True, top=False)
    axf_.tick_params(labelbottom=False, labeltop=True, top=True, bottom=False,
                     labelsize=7)
    dfp = _dic[('tot', 'pearson')][sul][cols]
    c9 = ucp.cb[1]
    c10 = ucp.cb[4]
    dfc = dfp.copy()
    dfc = dfc.apply(lambda x: (.5, .5, .5, 1))
    dfc.loc['09_MR'] = c9
    dfc.loc['10_SR'] = c10
    # axp.barh(dfp.index, dfp, zorder=100, color=dfc, height=.6)
    # axp.tick_params(axis='y', labelcolor=(.5, .5, .5), labelsize=7,
    #                 color=(0, 0, 0, 0))
    axf_.set_title('Pearson correlation coefficient', size=8)
    # axp.set_xlim(-.4, .4)
    # sns.despine(ax=axp, left=True)
    # axp.grid(True, linestyle='--', alpha=.5, axis='y', zorder=0)
    dj_ = dj18[dj18[sul] < 6]
    lin_df = dj_.resample('H').mean()
    # ax1 = s.axf[0]
    lin_df[[sul]].plot(linewidth=.7, marker=',', ax=ax1, color=[ucp.cb[0]],
                       legend=False)
    ops_ = dict(offset={'left': 5, 'bottom': 4}, trim=False)
    ax1.set_xticks([])
    # ax1.set_xticks([],minor=True)
    ax1.set_xlabel(None)
    ax1.set_ylabel(r'$\mathrm{SO}_4\ [\mathrm{\mu g}\, \mathrm{m}^{-3}]$')
    ax1.set_ylim(0, 6)
    ax1.set_yticks([0, 2, 4, 6])
    ax1.set_yticklabels([0, 2, 4, None])
    sns.despine(ax=ax1, bottom=True, **ops_)
    ax1.grid(True, which='minor', axis='x', linestyle='--')
    # tax = s.ax.twinx()
    # tax = s.axf[1]
    sr_ = lin_df[['09_MR',
                  # '10_SR'
                  ]]
    sr_: pd.DataFrame = sr_ / sr_.mean()
    sr_.plot(ax=tax, legend=False, linewidth=.7, color=[c9, c10])
    pw_ = dj6.resample('H').mean()['08_PW']
    pw_ = pw_ / pw_.mean()
    pw_.plot(ax=tax, linewidth=.7, color=[co.pw_col_dict['08_PW']])
    tax.set_xlabel(None)
    tax.set_ylabel(r'$\mathrm{SRR}\,/\,\overline{\mathrm{SRR}}$')
    tax.set_ylim(0, 6)
    tax.set_yticks([0, 2, 4, 6])
    tax.set_yticklabels([0, 2, 4, None])
    # tax.set_yticks([1,3,5],minor=True)
    sns.despine(ax=tax, **ops_)
    tax.grid(True, which='minor', axis='x', linestyle='--')
    tax: plt.Axes
    tax.annotate('09_MR', xy=[.11, .6], xycoords='axes fraction', color=c9,
                 size=6,
                 bbox=dict(color='w', alpha=0.5)
                 )
    tax.annotate('08_PW', xy=[0.02, .2], xycoords='axes fraction',
                 color=co.pw_col_dict['08_PW'], size=6,
                 bbox=dict(color='w', alpha=0.5)
                 )
    f.subplots_adjust(right=.95, left=.08, top=.9, bottom=.05, hspace=.2,
                      wspace=.5)
    f.tight_layout()
    # plt.show()
    return f,gs, axf_,ax1, tax




def plot_map2(d10c, d7c, d8c, d8mc, d9c, f, gs):
    def _add_labels(ax2, c9):

        _lo = -71.857
        _la = -15.787
        ax2.scatter(_lo, _la, c='k', edgecolors='w', zorder=10, s=20)
        ax2.annotate('Sabancaya', xy=[_lo, _la],
                     xytext=[-73.7, -15.5], size=8,
                     # arrowprops=dict(arrowstyle='-'),
                     alpha = .5
                     )

        _la,lo = -16.348611, -70.902222
        ax2.scatter(_lo, _la, c='k', edgecolors='w', zorder=10, s=20)
        ax2.annotate('Ubinas', xy=[_lo, _la],
                     xytext=[_lo, _la -.5], size=8,
                     # arrowprops=dict(arrowstyle='-'),
                     alpha = .5
                     )

        ax2.scatter(co.CHC_LON, co.CHC_LAT, c='k', edgecolors='w', zorder=10,
                    s=8)
        ax2.annotate(' CHC', xy=[co.CHC_LON, co.CHC_LAT], size=8,
                     # arrowprops=dict(arrowstyle='-'),
                     )
        ax2.scatter(co.LPB_LON, co.LPB_LAT, c='k', edgecolors='w', zorder=10,
                    s=8)
        ax2.annotate(' LPB', xy=[co.LPB_LON, co.LPB_LAT], size=8,
                     # arrowprops=dict(arrowstyle='-'),
                     xytext=[co.LPB_LON + 0, co.LPB_LAT - .5]
                     )
        ax2.annotate('08_PW', xy=[-77.8, -14.4], size=8, weight='bold',
                     color=co.pw_col_dict['08_PW']
                     # arrowprops=dict(arrowstyle='-'),
                     )
        ax2.annotate('09_MR', xy=[-74.5, -19], size=8,
                     # arrowprops=dict(arrowstyle='-'),
                     color=c9, weight='bold'
                     )
        ax2.annotate('07_SR', xy=[-68.5, -17.8], size=8,
                     # arrowprops=dict(arrowstyle='-'),
                     color=ucp.cb[2], weight='bold'
                     )
        ax2.annotate('08_SM', xy=[-73, -20.6], size=8,
                     # arrowprops=dict(arrowstyle='-'),
                     color=ucp.cb[7], weight='bold'
                     )
        ax2.annotate('10_SR', xy=[-69, -15], size=8,
                     # arrowprops=dict(arrowstyle='-'),
                     color=ucp.cb[6], weight='bold'
                     )

    # f,ax = plt.subplots(figsize=(5,4),dpi=300,subplot_kw={
    # 'projection':crt.crs.PlateCarree()})
    ax = f.add_subplot(gs[:4, 1:], projection=crt.crs.PlateCarree())
    ax2 = fa.get_ax_bolivia(ax=ax,
                            lola_extent=[-78, -67, -22, -11],
                            plot_cities=False, chc_lp_legend=False,
                            grid_alpha=0,
                            ylab_right=False,
                            ylab_left=False,
                            xlab_top=False,
                            xlab_bot=False

                            )
    ax2.xaxis.set_ticks_position('top')
    ax2.xaxis.set_label_position('top')
    ax2.yaxis.set_ticks_position('right')
    # ax2.yaxis.set_label_position('right')
    ax2.set_xticks([-75, -70], crs=crt.crs.PlateCarree())
    ax2.set_yticks([-15, -20], crs=crt.crs.PlateCarree())
    ax2.set_xlabel('longitude')
    ax2.set_ylabel('latitude')
    # cm = plt.get_cmap('Reds', 10)
    cm = fa.red_cmap(5)
    from descartes import PolygonPatch
    # for PER in np.arange(.9, 0, -.1):
    #     # print(PER)
    #     c = cm(1 - PER)
    #     # PER = 1
    #     pols = get_pols(d8c, per_M=PER, per_m=PER - .1)
    #     patch2b = PolygonPatch(pols, fc=c, ec='none', alpha=c[-1], zorder=2)
    #     ax2.add_patch(patch2b)
    #     # ax2.set_xlim(-85, -55)
    #     # ax2.set_ylim(-30, 0)
    import matplotlib.colors
    pols = get_pols(d8c, per_M=.85, per_m=0)
    patch2b = PolygonPatch(pols, fc='none', ec='w', alpha=1, zorder=2,
                           linewidth=5)
    ax2.add_patch(patch2b)
    patch2b = PolygonPatch(pols, fc=co.pw_col_dict['08_PW'], ec='none',
                           alpha=.4,
                           zorder=2,
                           )
    ax2.add_patch(patch2b)
    patch2b = PolygonPatch(pols, fc='none',
                           ec=co.pw_col_dict['08_PW'], alpha=1,
                           zorder=2,
                           linewidth=2)
    ax2.add_patch(patch2b)
    c9 = ucp.cb[1]
    pols = get_pols(d9c, per_M=.85, per_m=0)
    # patch2b = PolygonPatch(pols, fc='none', ec='w', alpha=1, zorder=2,
    #                        linewidth=2, linestyle='-')
    # ax2.add_patch(patch2b)
    patch2b = PolygonPatch(pols, fc='none', ec=c9, alpha=1, zorder=2,
                           linewidth=2, linestyle='-')
    ax2.add_patch(patch2b)
    pols = get_pols(d10c, per_M=.85, per_m=0)
    patch2b = PolygonPatch(pols, fc='none', ec=ucp.cb[6], alpha=1, zorder=2,
                           linewidth=2, linestyle='-')
    ax2.add_patch(patch2b)
    pols = get_pols(d8mc, per_M=.85, per_m=0)
    patch2b = PolygonPatch(pols, fc='none', ec=ucp.cb[7], alpha=1, zorder=2,
                           linewidth=2, linestyle='-')
    ax2.add_patch(patch2b)
    pols = get_pols(d7c, per_M=.85, per_m=0)
    patch2b = PolygonPatch(pols, fc='none', ec=ucp.cb[2], alpha=1, zorder=2,
                           linewidth=2, linestyle='-')
    ax2.add_patch(patch2b)
    # norm = mpl.colors.Normalize(vmin=0, vmax=100)
    # sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
    # sm.set_array([])
    # plt.colorbar(sm, ax=ax2)
    _add_labels(ax2, c9)
    return ax2


# %%



def get_pols(d9c, per_M, per_m=0):
    from shapely.geometry import Polygon
    from shapely.ops import cascaded_union, unary_union
    _df: pd.DataFrame = d9c.to_dataframe()
    # _df = _df[_df[co.CONC]>0]
    _df = _df.sort_values(co.CONC, ascending=False)
    take_M = _df['CONC'].sum() * per_M
    take_m = _df['CONC'].sum() * per_m
    _df1 = _df.copy()
    cumsum = _df['CONC'].cumsum()
    # _df1.loc['CONC'] = np.nan

    _boo = (take_M > cumsum) & (cumsum >= take_m)
    # print(_boo)
    _df1.loc[_boo, 'CONC'] = 1

    # _df1.loc[cumsum >= take, 'CONC'] = np.nan
    # ar = _df1.to_xarray()
    # coo = list(set(ar.var()) - {'CONC'})
    # ar = ar.set_coords(coo)
    # ar = ar['CONC'].sortby([co.R_CENTER, co.TH_CENTER])
    # %%
    _dfc: pd.DataFrame = _df1[_df1['CONC'] == 1].reset_index()

    def _get_pol(r):
        # rr = int(8/r[co.R_CENTER])

        rr = 5
        p1 = r[[co.LON_00, co.LAT_00]].round(rr)
        p2 = r[[co.LON_01, co.LAT_01]].round(rr)
        p3 = r[[co.LON_11, co.LAT_11]].round(rr)
        p4 = r[[co.LON_10, co.LAT_10]].round(rr)

        po = Polygon([p1, p2, p3, p4])
        return po

    _dfc['pol'] = _dfc.apply(_get_pol, axis=1)
    pols = unary_union(_dfc['pol'])
    return pols
