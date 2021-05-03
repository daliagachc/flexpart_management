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
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co
from useful_scit.imps import *

C18 = 'conc_lab_nc18'
plt;
# %%

import flexpart_management.notebooks.fourier_transforms as ft

img_path = pjoin(ft.__path__._path[0],'img')

# %%
def open_ds():
    _path = pjoin(co.tmp_data_path, 'cluster_series_v3.nc')
    ds = xr.open_mfdataset(_path,
                           concat_dim=co.RL, combine='nested')
    return ds

def get_df(clus_lab, ds, z='ALL',norm=1) -> pd.Series:
    dic = {'lab_nc18': clus_lab, 'normalized': norm, 'z_column': z}
    nc_18 = C18
    df = ds[nc_18].loc[dic].to_dataframe()[nc_18]

    return df


def get_fft(df, return_temp_fft=False):
    import scipy as sp
    temp_fft = sp.fftpack.fft(df.values)
    temp_psd = np.abs(temp_fft) ** 2
    fftfreq = sp.fftpack.fftfreq(len(temp_psd), 1. / 24.)
    i = fftfreq > 0
    fftfreq = fftfreq[i]
    temp_psd = temp_psd[i]
    fdf = pd.Series(temp_psd, index=fftfreq)
    if return_temp_fft:
        ret = fdf,temp_fft
    else:
        ret = fdf

    return ret

def plot_fourier_list(col_df, ls18, mean_ds):
    s = splot(6, 3, figsize=(10, 10), sharey=True, sharex=True)
    for ax, lab in zip(s.axf, ls18):
        fdf = col_df[lab]
        # fdf.index = 1/fdf.index
        mean_ds.plot(ax=ax, c='k',alpha=.5,linewidth=2)
        fdf.plot(ax=ax, c='red', alpha=.9,
                 # marker='x'
                 )
        ax: plt.Axes
        ax.set_xscale('log')
        ax.set_yscale('symlog',linthresh=.005)
        ax.set_ylim(0, .1)
        ax.set_xlim(.8, 22)
        ax.set_xticks(
            [1,2,4,7,14,21])
        ax.set_xticks([],minor=True)
        ax.set_xticklabels(['1','2','4','7','14','21'])
        ax.set_title(lab)
    s.f.tight_layout()
    s.f.show()
    return s


def get_fourier_for_all_df(ds, ls18):
    col_df = pd.DataFrame()
    for lab in ls18:
        df = get_df(lab, ds)
        fdf = get_fft(df / df.sum())
        std = 10
        fdf = fdf.rolling(window=std, min_periods=1, center=True,
                          win_type='gaussian').mean(std=int(std/2))

        col_df[lab] = fdf
    return col_df


def get_dds_km(cl_lab, ds, z='LEV0',h0=0,h1=24,nc=4):
    # %%
    dds = get_ds_for_dtw_kmeans(cl_lab, ds, z,h0=h0,h1=h1)[C18]
    from tslearn.clustering import TimeSeriesKMeans
    from tslearn.metrics import dtw
    km = TimeSeriesKMeans(
        nc,
        metric='dtw',
        metric_params={'sakoe_chiba_radius': 4},
        random_state=789

    )
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
    # dds['hour'] = xr.zeros_like(dds['time'], dtype=float) + \
    #               np.arange(0, 24, .5)
    # dds['nday'] = xr.zeros_like(
    #     dds['date'], dtype=int) + \
    #               np.arange(len(dds['date']))
    # dds = dds.swap_dims({'date': 'nday'})
    # dds = dds.swap_dims({'time': 'hour'})
    return dds, km


# %%

def get_ds_for_dtw_kmeans(cl_lab, ds, z,h0=0,h1=24):
    # %%
    df = get_df(cl_lab, ds, z=z)
    df = df - df.rolling(24,1,True).mean()
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
        delta_h = (chunk[co.RL]-d)/pd.Timedelta(hours=1)
        chunk['hour'] = delta_h
        chunk['date'] = d
        chunk = chunk.set_index(['date','hour'])[C18]
        ds_chunk = chunk.to_xarray()
        # print(len(chunk))
        if len(chunk) is ((h1-h0)*2+1):
            ds_list.append(ds_chunk)

    # %%
    dds= xr.merge(ds_list)

    return dds




# %%


def plot_ts_clus(dds, km, cl_lab, _in,
                 h0=0,h1=24,):
    nc = km.n_clusters
    rx = 2
    ry = int(np.ceil(nc/rx))
    s = splot(rx, ry, sharey=False, sharex=False, dpi=300,
              figsize = (3.14,3), squeeze=False
              )
    # for i, ax in enumerate(s.axf):

    # _std = dds.to_dataframe().groupby('labs').mean()[
    #     'conc_lab_nc18'].sort_values()
    # print(_std)
    # index_ = _std.index.values
    # print(index_)

    for i,ci in enumerate(_in):
        ax = s.axf[i]
        sel = dds[{'date': dds['labs'] == ci}]*100
        tot = len(dds['date'])
        yM = dds.quantile(.999) * 100
        ym = dds.quantile(.001) * 100
        yy = np.max([yM,-ym])
        sel.plot(
            hue='date', add_legend=False,
            # col='labs',
            # col_wrap=4
            ax=ax,
            color='k',
            alpha=.1,
            xlim=[h0,h1],
            ylim=[-yy, yy],
            linewidth=.7
        )
        cen = km.cluster_centers_[ci]*100
        _df = pd.Series(cen[:, 0], index=dds['hour'].values)
        _df.plot(ax=ax, c = ucp.cc[0])
        ax.set_title(
            f'n={len(sel)} ({len(sel)/tot*100:2.0f}%)',
            loc='right',y=.95, alpha=.5, size=8)
        # ax.set_ylabel('SRR [%]')
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.set_xticks(np.arange(h0,h1+1,4))
        ax.set_xticks(np.arange(h0, h1 + 1, 2), minor=True)
        # ax.set_yticks([0,5,10,15])
        ax.axvline(12, c = ucp.cc[2],zorder = 0, alpha=.5,
                   linestyle='--')
        sns.despine(ax=ax,trim=True,offset=[0,5])
    if ry > 1:
        for ax in s.axs[:,1:].flatten():
            # sns.despine(ax=ax,left=True)
            ax.spines['left'].set_visible(False)
            ax.set_yticks([])
            ax.set_yticks([], minor=True)
            ax.set_ylabel(None)
    if rx > 1:
        for ax in s.axs[:-1,:].flatten():
            ax.spines['bottom'].set_visible(False)
            ax.set_xticks([])
            ax.set_xticks([], minor=True)
            ax.set_xlabel(None)
    s.axs[-1,0].set_xlabel('Local time [hour]')
    s.axs[-1,0].set_ylabel('det. SRR [%]')
    s.f.tight_layout()
    s.f.suptitle(f'{cl_lab}',va='top')
    fa.add_ax_lab(s.axf[0],'a')
    fa.add_ax_lab(s.axf[1],'b')
    # s.f.subplots_adjust(top=.9)
    s.f.tight_layout()
    plt.show()
    return s

def plot_daily_evolution(ds, ls18):
    s = splot(6, 3, figsize=(10, 10), sharey=True, sharex=True)
    lab = '07_SR'
    for lab, ax in zip(ls18, s.axf):
        temp = get_df(lab, ds)
        temp = temp
        temp.index = temp.index - pd.Timedelta(minutes=180)
        nt = temp.groupby(temp.index.hour).median()
        nt = nt / nt.mean()
        nt.plot(ax=ax)
        # ax.set_ylim(0,None)
        ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
        ax.set_xlim(0, 24)
        ax.axvline(x=12, c='red')
        ax.set_xticks([], minor=True)
        ax.set_title(lab)
        ax.set_xlabel('local time [h]')
    s.axf[0].set_ylim(0, 3.5)
    s.f.tight_layout()
    return s


