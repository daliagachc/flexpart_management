# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo


# %%
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co
from useful_scit.imps import *
import flexpart_management.notebooks.surface_timeseries. \
    surface_timeseries_lfc as lfc
# from flexpart_management.notebooks.fourier_transforms. \
    # fourier_transforms_lfc import *

plt;
# %%

def main():
# %%
    def open_ds():
        _path = pjoin(co.tmp_data_path, 'cluster_series_v3.nc')
        ds = xr.open_mfdataset(_path,
                               concat_dim=co.RL, combine='nested')
        return ds

    # %%

    ds = open_ds()

    # %%

    all_ = ds['conc_all'] * 100
    dall = all_.loc[{'z_column': 'ALL', 'normalized':1}]
    dbll = all_.loc[{'z_column': 'BL', 'normalized':1}]
    doll = all_.loc[{'z_column': 'LEV0', 'normalized':1}]

    # %%
    drat = (dbll / dall) * 100

    # %%
    rat = drat.to_dataframe()['conc_all']
    bll = dbll.to_dataframe()['conc_all']
    oll = doll.to_dataframe()['conc_all']
    obll = (doll / dbll).to_dataframe()['conc_all'] * 100

    # %%
    s = splot(figsize=(30,5))
    rat.plot(ax=s.ax, label ='rat')
    oll.plot(ax=s.ax, label ='o')
    bll.plot(ax=s.ax, label ='b')
    obll.plot(ax=s.ax, label ='ob')
    s.ax.legend()
    plt.show()

    # %%

    s = splot(figsize=(10,3),dpi=300)
    oll.plot(linewidth=.5, label ='lev0')
    moll = oll.rolling(1*24, min_periods=1,center=True).mean()
    moll_l = oll.rolling(20*24, min_periods=1,center=True).mean()

    moll.plot(linewidth=1, label='detrend day')
    moll_l.plot(linewidth=1, label='detrend 20 day')
    s.ax.legend()
    s.f.tight_layout()
    plt.show()

    # %%

    s = splot(figsize=(10,3),dpi=300)
    det = (oll - moll)
    det.plot(linewidth=.5)
    s.f.tight_layout()
    plt.show()
    # %%
    s = splot(ncols=1,nrows=2,figsize=(3.3,4),dpi=300,
              gridspec_kw={'height_ratios': [1, 2]}
              )

    print(lfc.lin_reg(bll.values.reshape(-1,1),oll))
    # s = splot(figsize=(7.25,5),dpi=300)
    ax0 = s.axf[0]
    ops = dict(kde=False,bins=np.arange(0,50,2))
    sns.distplot(oll,ax=ax0,**ops)
    sns.distplot(bll, ax=ax0,**ops)
    ax0.set_ylabel('Frequency [hours]')
    ax0.set_xlabel('Surface and PBL$^*$ influence over CHC [%]')

    sns.despine(ax=ax0)
    ax0.text(11,1000,'$S_{\mathrm{SRR}}$')
    ax0.text(25,550,'$\mathrm{PBL}^*_{\mathrm{SRR}}$')
    df = pd.DataFrame(det)
    ax1 = s.axf[1]
    h = 'Local time'
    d = 'Date'
    df[h] = (df.index - pd.Timedelta(hours=4)).hour+.5
    df[d] = df.index.date
    ar = df.set_index([d, h]).to_xarray().transpose(d,h)
    # s.ax.xaxis_date()
    arr = ar['conc_all']
    arr.name = '''Detrended surface \t\t\tinfluence [%]'''
    arr.plot(ax=ax1)
    ax1.set_xticks(np.arange(0,24.1,4))
    ax1.set_xticks(np.arange(0,24.1,2),minor=True)
    fa.add_ax_lab(ax0,'a')
    fa.add_ax_lab(ax1,'b')
    # fa.add_ax_lab(axin1,'c')
    s.f.tight_layout()
    plt.show()
    s.f.savefig(pjoin(co.paper_fig_path,'surface_bl_influence.pdf'))

    # %%
    # ds = lfc.open_ds()
    # # ls18 = list(ds[lfc.C18]['lab_nc18'].values)
    # ls18 = co.get_nc18_order().sort_values(['sr', '18_NC'])['18_NC'].values
    # %%
    h0 = 0
    h1 = 24
    dic = {'normalized': 1, 'z_column': 'LEV0'}
    conc_all = 'conc_all'
    # df = ds[conc_all].loc[dic].to_dataframe()[conc_all]
    # %%
    df = det
    # %%


    df.index = df.index - pd.Timedelta(4, 'hour')
    df: pd.Series = df.resample('30T').asfreq()
    df = df.interpolate()
    # %%
    days = np.unique(df.index.round('1d'))
    ds_list = []
    for d in days:
        d0 = d + pd.Timedelta(f'{h0}h')
        d1 = d + pd.Timedelta(f'{h1}h')
        d_noon = d + pd.Timedelta('12h')
        chunk = df.loc[d0:d1].copy().reset_index()
        delta_h = (chunk[co.RL] - d) / pd.Timedelta(hours=1)
        chunk['hour'] = delta_h
        chunk['date'] = d
        chunk = chunk.set_index(['date', 'hour'])[conc_all]
        ds_chunk = chunk.to_xarray()
        print(len(chunk))
        if len(chunk) is ((h1 - h0) * 2 + 1):
            ds_list.append(ds_chunk)
    # %%


    # %%
    dds = xr.merge(ds_list)[conc_all]
    # %%
    # %%
    from tslearn.clustering import TimeSeriesKMeans

    km = TimeSeriesKMeans(
        6,
        metric='dtw',
        metric_params={'sakoe_chiba_radius': 4})
    km.fit(dds.values)
    _ = km.cluster_centers_
    for c in _:
        plt.plot(c)
    plt.show()
    # %%
    labs = km.predict(dds.values)
    lb = xr.zeros_like(dds['date'], dtype=int) + labs
    # %%
    dds['labs'] = lb
    # %%
    dds['labs'].reset_coords(drop=True). \
        to_dataframe()['labs'].value_counts(). \
        sort_index(). \
        plot.bar()
    plt.show()

    # %%
    s = splot(3, 2, sharey=True, sharex=True)
    for i, ax in enumerate(s.axf):
        sel = dds[{'date': dds['labs'] == i}]
        sel.plot(
            hue='date', add_legend=False,
            # col='labs',
            # col_wrap=4
            ax=ax,
            color='k',
            alpha=.2
        )
        cen = km.cluster_centers_[i]
        _df = pd.Series(cen[:, 0], index=dds['hour'].values)
        _df.plot(ax=ax)
        ax.set_title(f'n={len(sel)} | c={i}')
        ax.set_ylabel('SRR')
    s.f.tight_layout()
    s.f.suptitle(f'', va='top')
    s.f.subplots_adjust(top=.85)
    # s.f.tight_layout()
    plt.show()
