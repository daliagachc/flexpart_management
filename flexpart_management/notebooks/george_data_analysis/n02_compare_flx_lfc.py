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
from matplotlib import pyplot
from useful_scit.imps import *
from flexpart_management.modules import fa, co, constants, flx_array
fa,co,plt

# %%
is_ft_candidate = 'is_ft_candidate'


def import_george_data():
    data_path = pjoin(co.tmp_data_path, 'data_george_cc.xlsx')
    df_ft = pd.read_excel(data_path)
    df_ts = pd.read_excel(data_path, sheet_name=1, skiprows=1)
    # %%
    df_ts = df_ts.set_index(pd.to_datetime(df_ts['time_utc']))
    df_ts = df_ts.drop('time_utc', axis=1)
    return {'candidate_ft_timestamps':df_ft,'data_time_series':df_ts}


def plot_z_above_sea_level_comparison(flx_ds):
    jan_boo = flx_ds[co.RL].dt.month == 1
    # %%
    z_com = fa.get_dims_complement(flx_ds, co.ZM)
    res_jan = flx_ds['CONC'].where(jan_boo).sum(z_com).load()
    # %%
    z_com = fa.get_dims_complement(flx_ds, co.ZM)
    res_ft = flx_ds['CONC'].where(flx_ds['is_ft_candidate']).sum(z_com).load()
    # %%
    f, ax = plt.subplots()
    (res_jan / res_jan.sum()).plot(ax=ax, label='january')
    (res_ft / res_ft.sum()).plot(ax=ax, label='ft_candidate')
    ax.grid()
    ax.legend()
    plt.show()

def plot_z_above_ground_level_comparison(flx_ds):
    jan_boo = flx_ds[co.RL].dt.month == 1
    # %%
    z_com = fa.get_dims_complement(flx_ds, co.ZM)
    res_jan = flx_ds['CONC'].where(jan_boo).sum(z_com).load()
    # %%
    z_com = fa.get_dims_complement(flx_ds, co.ZM)
    res_ft = flx_ds['CONC'].where(flx_ds['is_ft_candidate']).sum(z_com).load()
    # %%
    f, ax = plt.subplots()
    (res_jan / res_jan.sum()).plot(ax=ax, label='january')
    (res_ft / res_ft.sum()).plot(ax=ax, label='ft_candidate')
    ax.grid()
    ax.legend()
    plt.show()


def add_is_it_ft_candidate(flx_ds, time_stamps):
    flx_time = flx_ds[co.RL].copy()
    ft_boo = flx_time <= flx_time[0]
    for l, r in time_stamps.iterrows():
        new_boo = np.logical_and(flx_time >= xr.DataArray(r.iloc[0]),
                                 flx_time <= xr.DataArray(r.iloc[1]))
        ft_boo = np.logical_or(ft_boo, new_boo)
    # %%
    flx_ds = flx_ds.assign_coords({is_ft_candidate: ft_boo})
    return flx_ds


def plot_above_ground_level(flx_ds):
    jan_boo = flx_ds[co.RL].dt.month == 1
    res_sum_tot = regrid_and_sum(flx_ds, _boo=True)
    res_sum_jan = regrid_and_sum(flx_ds, _boo=jan_boo)
    res_sum_ftc = regrid_and_sum(flx_ds, _boo=flx_ds[is_ft_candidate])
    # %%
    f, ax = plt.subplots()
    _ds = res_sum_ftc
    (_ds / _ds.sum()).plot(ax=ax, label='ft_candidate')
    _ds = res_sum_tot
    (_ds / _ds.sum()).plot(ax=ax, label='6 month total')
    _ds = res_sum_jan
    (_ds / _ds.sum()).plot(ax=ax, label='january')
    ax.legend()
    ax.grid()
    ax.set_xlabel('magl')
    ax: plt.Axes
    ax.set_ylabel('normalized SRR')
    plt.show()


def regrid_and_sum(flx_ds,_boo=True):
    ds_rl = flx_ds['CONC'].where(_boo).sum(co.RL).load()
    # %%
    import wrf
    topo_ = (ds_rl[co.ZM] - ds_rl[co.TOPO])
    ds_g = (topo_ / 500).round() * 500
    # %%
    res = wrf.interplevel(ds_rl.reset_coords(drop=True), ds_g, ds_g[co.ZM])
    res = res.rename({'level': co.ZM})
    res.name = 'CONC'
    # %%
    res_sum = res.sum([co.R_CENTER, co.TH_CENTER])
    return res_sum


def plot_for_time_stamp(flx_ds, r, l, hs=None):
    if hs is None:
        hs = [[0, 12]]

    df = get_th_bool(hs)

    fig:plt.Figure = plt.figure(constrained_layout=True,figsize=(8,10))
    spec = fig.add_gridspec(ncols=2, nrows=5)
    ax11 = fig.add_subplot(spec[3,:])
    ax12 = fig.add_subplot(spec[4,:])

    axs = [ax11,ax12]
    import cartopy as cy
    ax2 = fig.add_subplot(spec[:3,:],projection=cy.crs.PlateCarree())

    boo = r['boo']
    for i,df_r in df.iterrows():
        ax = axs[i]
        clock_boo = df_r['fun'](
            flx_ds[co.TH_CENTER]>=df_r['th1'],
            flx_ds[co.TH_CENTER]<df_r['th2']
        )
        flx_trim = flx_ds['CONC'].where(boo).where(clock_boo).sum(co.RL).load()
        flx_sum = flx_trim.sum([co.TH_CENTER])

        flx_Z = flx_trim.sum(co.ZM)
        surf = (flx_Z*flx_trim[co.TOPO])/flx_Z.sum(co.TH_CENTER)

        to_plot = 0.1*flx_Z.mean()
        _boo = flx_Z.sum(co.TH_CENTER)>to_plot
        surf.sum(co.TH_CENTER).where(_boo).plot(ax=ax)

        flx_sum.plot(cmap=plt.get_cmap('Reds'),ax=ax)



        st = f'clock {df_r["h1"]}-{df_r["h2"]}'
        ax:plt.Axes
        ax.annotate(st,[0,.99],xycoords='axes fraction',verticalalignment='top')


    flx_sum = flx_ds[['CONC']].where(boo).sum([co.RL, co.ZM])

    ax2 = fa.get_ax_bolivia(ax=ax2)
    fa.logpolar_plot(flx_sum, ax=ax2)
    ax2:plt.Axes
    ax2.set_title(f'{l}|{r.iloc[0]}-{r.iloc[1]}')
    plt.show()


def get_th_bool(hs):
    df = pd.DataFrame(hs, columns=['h1', 'h2'])
    df['normal'] = df['h1'] < df['h2']
    df['th1'] = df['h1'] * np.pi / 6
    df['th2'] = df['h2'] * np.pi / 6
    df['fun'] = np.logical_and
    df['fun'][~df['normal']] = np.logical_or


    return df