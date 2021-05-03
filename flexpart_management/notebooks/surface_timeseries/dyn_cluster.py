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

import flexpart_management.notebooks.fourier_transforms. \
    fourier_transforms_lfc as lfc
from flexpart_management.notebooks.fourier_transforms. \
    fourier_transforms_lfc import *


# %%
def main():
    # %%
    ds = lfc.open_ds()
    # ls18 = list(ds[lfc.C18]['lab_nc18'].values)
    ls18 = co.get_nc18_order().sort_values(['sr', '18_NC'])['18_NC'].values
    # %%
    h0 = 0
    h1 = 24
    dic = {'normalized': 1, 'z_column': 'LEV0'}
    conc_all = 'conc_all'
    df = ds[conc_all].loc[dic].to_dataframe()[conc_all]
    # %%
    df
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
        delta_h = (chunk[co.RL]-d)/pd.Timedelta(hours=1)
        chunk['hour'] = delta_h
        chunk['date'] = d
        chunk = chunk.set_index(['date','hour'])[conc_all]
        ds_chunk = chunk.to_xarray()
        print(len(chunk))
        if len(chunk) is ((h1-h0)*2+1):
            ds_list.append(ds_chunk)
    # %%


    # %%
    dds = xr.merge(ds_list)[conc_all]
    # %%
    # %%
    from tslearn.clustering import TimeSeriesKMeans
    from tslearn.metrics import dtw
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
    s.f.suptitle(f'',va='top')
    s.f.subplots_adjust(top=.85)
    # s.f.tight_layout()
    plt.show()

    # %%



    # cl_lab = '09_MR'
    for cl_lab in ls18:
        dds, km = lfc.get_dds_km(cl_lab, ds, z='ALL', h0=0, h1=24)
        s = lfc.plot_ts_clus(dds, km, cl_lab)
        name = f'day_dtw_kmean_{cl_lab}.pdf'
        s.f.savefig(pjoin(img_path, name))
    for cl_lab in ls18:
        dds, km = lfc.get_dds_km(cl_lab, ds, z='ALL',h0=-12,h1=12)
        s = lfc.plot_ts_clus(dds, km, cl_lab)
        name = f'night_dtw_kmean_{cl_lab}.pdf'
        s.f.savefig(pjoin(img_path,name))


        # break

    # %%

    pass



# %%
if __name__ == '__main__':
    main()
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
