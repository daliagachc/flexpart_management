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
import flexpart_management.notebooks.meteo_cumbre.meteo_cumbre_lfc as lfc
from flexpart_management.notebooks.meteo_cumbre.meteo_cumbre_lfc import *

# %%
def main():
    # %%
    path = '/Volumes/mbProD/bolivia_campaign_data/meteo_cumbre/meteo_cumbre_mariadb/meteo_cumbre.csv'
    # %%
    df_wrf = xr.open_dataset('/Users/diego/flexpart_management/flexpart_management/requests/george/data/time_series_for_selected_values_at_chc_wrf.nc')
    df_wrf = df_wrf.reset_coords(drop=True).to_dataframe()

    # %%

    df = pd.read_csv(path).set_index('date_time')
    df.index = pd.to_datetime(df.index)
    df.index.name='Time'
    # %%
    df['wx'] = df['WS'] * np.sin(df['WD']*np.pi/180)
    df['wy'] = df['WS'] * np.cos(df['WD']*np.pi/180)
    df['ws'] = df['WS'] * 1
    df['ck'] = df['WD']*12/360
    # %%
    df['2018-04-19':'2018-04-21'][['ck','ws']].plot()
    plt.show()

    # %%
    _r = (df['wx'] - df_wrf['ua']).dropna()
    _r1 = (df['wx'] + df_wrf['ua']).dropna()
    sns.distplot(_r)
    sns.distplot(_r1)
    plt.show()
    # %%
    sns.distplot(df['wx'][_r.index],label='wx')
    sns.distplot(df['wy'][_r.index],label='wy')
    sns.distplot(df_wrf['va'][_r.index],label='va')
    sns.distplot(df_wrf['ua'][_r.index],label='ua')
    ax = plt.gca()
    ax.legend()
    plt.show()
    # %%
    s = splot(2,sharex=True)
    sl = slice('2018','2018')
    s.axf[0].hist(df['WD'][_r.index][sl]*12/360,)
    # plt.show()

    ss = np.arctan2(-df_wrf['ua'], -df_wrf['va'])[_r.index][sl]
    ss.name='wrf'
    ss = np.mod(ss,2 * np.pi)*6/np.pi
    s.axf[1].hist(
        ss
    )
    plt.show()
    # %%
    # import ma
    s = splot(2,sharex=True,figsize=(5,10))
    df_wrf_ = df_wrf.loc[_r.index]
    hops = dict(cmap='Reds',
                # norm=mpl.colors.LogNorm(vmin=10,vmax=20000),
                bins=15
                )

    s.axf[0].hist2d(-df_wrf_['ua'],-df_wrf_['va'],
                    **hops)

    df_ = df.loc[_r.index][['wx','wy']].dropna()
    s.axf[1].hist2d(df_['wx'],df_['wy'],
                    **hops)
    for ax in s.axf:
        ax.grid()
    plt.show()

    # %%
    dj = pd.DataFrame()
    dj['ax'] = df['wx'][_r.index]
    dj['ay'] = df['wy'][_r.index]
    dj['mx'] = -df_wrf['ua'][_r.index]
    dj['my'] = -df_wrf['va'][_r.index]
    dj['one'] = .001
    dj['ar'] = np.log(np.sqrt(dj['ax']**2+dj['ay']**2)+.001)*3
    dj['mr'] = np.log(np.sqrt(dj['mx']**2+dj['my']**2)+.001)*3
    aj = dj[['ax','ay','one','ar']].copy()
    mj = dj[['mx','my','one','mr']].copy()

    from sklearn.cluster import AgglomerativeClustering
    from sklearn.mixture import GaussianMixture
    ho = 10
    # km = AgglomerativeClustering(
    #     n_clusters=ho,
    #     affinity='cosine',
    #     linkage='average'
    # )
    # ar = km.fit_predict(aj.values)
    # aj['l'] = ar

    km = AgglomerativeClustering(
        n_clusters=ho,
        affinity='euclidean',
        linkage='ward'
    )
    ar = km.fit_predict(dj[['ax','ay','mx','my']].values)
    dj['l'] = ar

    # %%
    s = splot(2,figsize=(5,10),sharex=True,sharey=True)
    lab = 9
    _dj = dj[dj['l']==lab]
    s.axf[0].hist2d(_dj['mx'],_dj['my'],
                    # palette="Set2",alpha=1,
                    # ax=s.axf[0]
                    cmap = 'Reds'
                    )
    s.axf[1].hist2d(_dj['ax'],_dj['ay'],
                    # palette="Set2",alpha=1,
                    # ax=s.axf[1]
                    cmap='Reds'
                    )
    for ax in s.axf:
        ax.scatter(0,0)
    s.axf[0].set_title('model')
    s.axf[1].set_title('an')
    s.axf[0].set_ylim(-10,10)
    s.axf[0].set_xlim(-10,10)
    plt.show()
    # %%
    dj['l'].hist(bins=np.arange(-.5,ho))
    plt.show()
    # %%
    df_ts = lfc.import_time_series()
    df_ts[co.RL] = df_ts.index
    df_ts = df_ts.set_index(co.RL)
    df_ts = df_ts.resample('H').mean()
    # %%
    df_ts
    aaj = dj.resample('H').mean()
    mer = pd.merge(left=df_ts['BC'],right=aaj,left_index=True,right_index=True)
    mer = mer[mer['BC']>=0]
    mer = mer[~mer['ax'].isnull()]
    # %%
    # %%
    bins = np.arange(-10.5,10,1)
    plt.hist2d(
        mer['ax'],mer['ay'],bins=[bins,bins],
        cmap='Reds'
    )
    plt.show()

    # %%
    # bins = np.arange(-10,10,1)
    plt.hist2d(
        mer['ax'],mer['ay'],weights=(mer['BC']**(1/1)),bins=[bins,bins],
        cmap='Reds'
    )
    plt.show()
    # %%
    # %%
    bins = np.arange(-10,10,1)
    plt.hist2d(
        mer['mx'],mer['my'],weights=(mer['BC']**(1/2)),bins=[bins,bins],
        cmap='Reds'
    )
    plt.show()
    # %%
    # %%
    # %%
    bins = np.arange(-10,10,1)
    plt.hist2d(
        mer['mx'],mer['my'],bins=[bins,bins],
        cmap='Reds'
    )
    plt.show()
    # %%


# %%

# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%


