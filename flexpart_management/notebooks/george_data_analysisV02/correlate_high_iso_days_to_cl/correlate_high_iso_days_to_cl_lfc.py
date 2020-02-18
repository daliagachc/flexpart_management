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
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co

plt;


# %%
def get_geo_fl(geo_ts: pd.DataFrame, clus_ds):
    def rule(_row):
        t0 = xr.DataArray(_row['t0_utc'])
        t1 = xr.DataArray(_row['t1_utc'])

        _res = (clus_ds[co.RL] >= t0) & \
              (clus_ds[co.RL] <= t1)
        return _res

    geo_ts_trim = geo_ts[geo_ts['jan_case'] == 1]
    flag = clus_ds[co.RL].dt.hour < -1

    for l, row in geo_ts_trim.iterrows():
        res = rule(row)
        flag = np.logical_or(flag, res)

    return flag

def get_geo_fl_dic(geo_ts: pd.DataFrame, clus_ds, filter='jan_case'):
    def rule(_row):
        t0 = xr.DataArray(_row['t0_utc'])
        t1 = xr.DataArray(_row['t1_utc'])

        _res = (clus_ds[co.RL] >= t0) & \
               (clus_ds[co.RL] <= t1)
        return _res

    geo_ts_trim = geo_ts[geo_ts[filter] == 1]
    case_dic = {}
    for l, row in geo_ts_trim.iterrows():
        res = rule(row)
        case_dic[row['name']] = res

    return case_dic


# %%
def reverse_legend(ax):
    leg_han = ax.get_legend_handles_labels()
    [l.reverse() for l in leg_han]
    ax.legend(*leg_han)


# %%
def plot_ratios(rr, ax):
    # ax: plt.Axes
    ax.hlines(y=rr.index, xmin=1, xmax=rr, linewidth=10)
    ax.grid(linestyle=':', axis='y')


# %%
def plot_influences(ax, bar_df):
    bar_df.plot.barh(ax=ax)
    import matplotlib.legend
    # leg:mpl.legend.Legend = ax.get_legend()
    reverse_legend(ax)
    ax.grid(linestyle=':', axis='y')


# %%
def tex_index(df):
    df.index = df.index \
        .str.replace(r'_', r'_{\text{') \
        .str.replace(r'(.)$', r'\1}}$') \
        .str.replace(r'^(.)', r'$\1')


# %%
def plot_comparison(clus_ds, med_ds, fls_dic, cases_flag_dic, order=None):
    fls = fls_dic.keys()
    from matplotlib import rc
    rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
    ## for Palatino and other serif fonts use:
    # rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}']
    f, axs = plt.subplots(1, 3, figsize=(9, 6),
                          sharey=True,
                          dpi=150)
    ax2 = axs.flatten()[0]
    ax1 = axs.flatten()[1]
    ax3 = axs.flatten()[2]

    order1 = plot_box_plot_ratio(cases_flag_dic, clus_ds, fls_dic,ax=ax2)

    if order is None:
        order = order1

    r0 = clus_ds.where(clus_ds['high iso']).mean(co.RL).to_dataframe()
    r1 = clus_ds.where(clus_ds['january night']).mean(co.RL).to_dataframe()
    rr: pd.Series = r0 / r1
    tex_index(rr)
    rr = rr.loc[order]

    bar_df = pd.DataFrame()
    for fl in fls:
        r = clus_ds.where(clus_ds[fl]).mean(co.RL).to_dataframe()
        r = r
        bar_df[fl] = r['srr_pt']
    tex_index(bar_df)
    bar_df = bar_df.loc[rr.index]
    plot_influences(ax1, bar_df)
    ax1.set_xlabel('SRR [\%]')

    # plot_ratios(rr, ax2)
    lab = r'$\frac{\text{SRR}_{\text{high iso}}}{\text{SRR}_{\text{january night}}}$'
    ax2.set_xlabel(lab)
    # ax1.set_xlabel(r'$\frac{SRR_{{january high iso}}}{3}$')
    stat_dim = 'ZMID_ASL_stat'
    _ls = []
    for k, v in fls_dic.items():
        res = get_avg_stat_flag(fls_dic, k, med_ds, stat_dim)
        _ls.append(res)

    df = pd.DataFrame(_ls).T
    tex_index(df)
    # from matplotlib import rc
    # rc('text', usetex=True)
    # mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}']
    df1 = df.loc[rr.index]
    df1.index.name = 'cluster'
    df1.plot.barh(ax=ax3, legend=False)
    ax3.set_xlabel(r'z [asl]')
    ax3: plt.Axes
    ax3.grid(linestyle=':', axis='y')
    f.show()

    return rr


# rr = plot_comparison(clus_ds, fls_dic)
# %%
def not_so_important_plot(med_ds):
    from matplotlib import rc
    rc('text', usetex=False)
    locs = {'stat': 'avg', 'stat_dim': 'ZMID_ASL_stat', 'lab_name': '05_MR'}
    f, ax = plt.subplots()
    ax: plt.Axes
    ax2 = ax.twinx()
    df2 = med_ds.loc[{'lab_name': '05_MR'}]['srr_pt'].to_dataframe()['srr_pt']
    df2.plot(ax=ax2, color='red')
    df1 = med_ds.loc[locs]['stat_vals'].to_dataframe()['stat_vals']
    df1.where(df2 > 10).plot(ax=ax)
    plt.show()


# %%
def get_avg_stat_flag(fls_dic, key, med_ds, stat_dim):
    flag = fls_dic[key]
    ds1 = med_ds.where(flag).loc[{'stat': 'avg', 'stat_dim': stat_dim}]
    mul = ds1['stat_vals'] * ds1['srr_pt']
    res = mul.sum(co.RL) / ds1['srr_pt'].sum(co.RL)
    res.name = key
    return res.to_dataframe()[res.name]

# %%
def wighted_mean_from_flag(case_name, ds_conc, flags, agl=True):
    ds1 = ds_conc.where(flags)
    if agl:
        zagl = ds1[co.ZM] - ds1[co.TOPO]
    else:
        zagl = ds1[co.ZM]
    ds_sum = ds1.sum([co.RL])
    num = (ds_sum * zagl).sum([co.TH_CENTER, co.ZM])
    dem = ds_sum.sum([co.TH_CENTER, co.ZM])
    res = num / dem
    # res = res
    res.name = case_name
    return res
# %%
def plot_cases_distance(agl, cases_flag_dic, ds_conc, fls_dic):
    res_list = []
    mpl.rcParams['text.usetex'] = False
    for case, flags in cases_flag_dic.items():
        res = wighted_mean_from_flag(case, ds_conc, flags,
                                     agl=agl)
        res_list.append(res)
    new_ds = xr.merge(res_list).to_array(dim='case')
    jn = wighted_mean_from_flag('january night',
                                ds_conc,
                                fls_dic['january night'],
                                agl=agl)
    f, ax = plt.subplots()
    ax: plt.Axes
    new_ds.plot(hue='case', ax=ax, alpha=.5)
    jn.plot(ax=ax, color='k')
    if agl:
        ax.set_ylabel('Z AGL')
    else:
        ax.set_ylabel('Z ASL')
    plt.show()
    return res_list

def get_mid_sums(case, ds_conc, flags):
    complement = fa.get_dims_complement(ds_conc, co.ZM)
    res = ds_conc.where(flags).sum(complement)
    res.name = case
    return res


def get_mid_sums_zagl(case, ds_conc, flags):
    complement = fa.get_dims_complement(ds_conc, co.ZM)

    d_fl = ds_conc.where(flags)
    zagl = d_fl[co.ZM] - d_fl[co.TOPO]
    res = d_fl.sum(complement)
    res.name = case
    return res

def get_agl_ds(ds_conc):
    r_len = len(ds_conc[co.R_CENTER])
    th_len = len(ds_conc[co.TH_CENTER])
    out_out = []
    for r in range(r_len):
        out = []
        for th in range(th_len):
            sel = {co.R_CENTER: [r], co.TH_CENTER: [th]}
            r_th = ds_conc[sel]
            topo_i = int(np.round(r_th[co.TOPO] / 500))
            sh = r_th.shift(**{co.ZM: -topo_i})
            out.append(sh)
        print(r)
        th_res = xr.concat(out, dim=co.TH_CENTER)
        out_out.append(th_res)
    agl_ds = xr.concat(out_out, dim=co.R_CENTER)
    return agl_ds

def plot_z_per(cases_flag_dic, ds_conc, fls_dic, agl=False):
    res_list = []
    mpl.rcParams['text.usetex'] = False
    for case, flags in cases_flag_dic.items():
        res = get_mid_sums(case, ds_conc, flags)
        res_list.append(res)
    new_ds = xr.merge(res_list).to_array(dim='case')
    new_ds = new_ds / new_ds.sum(co.ZM)
    # %%

    f, ax = plt.subplots(figsize=(6, 8))
    ax: plt.Axes
    pot = new_ds.plot(hue='case', y=co.ZM, ax=ax, alpha=.5,
                      # add_legend=False
                      )
    # leg1 = ax.get_legend_handles_labels()
    # ax.legend()
    ax.figure.add_artist(ax.get_legend())

    # ax.figure.show()
    # print(leg1)
    ax.grid()
    jan_night = 'january night'
    all = get_mid_sums(jan_night, ds_conc,
                       fls_dic[jan_night])
    all = all / all.sum(co.ZM)
    all.plot(hue='case',
             y=co.ZM, ax=ax, color='k',
             label=jan_night+' mean')
    label = 'high iso mean'
    new_ds.mean('case').plot(y=co.ZM, ax=ax, color='r',
                             label=label)
    # leg2 = ax.get_legend()

    ax.legend(loc='lower right')
    ax.set_ylabel('Z ASL')
    if agl:
        ax.set_ylabel('Z AGL')
    ax.set_xlabel('SRR "PDF"')
    ax.figure.show()

def plot_box_plot_ratio(cases_flag_dic, clus_ds, fls_dic,
                        ax=None, order = None):
    mpl.rcParams['text.usetex'] = True
    # f, ax = plt.subplots()
    ax: plt.Axes
    # gf1 = cases_flag_dic[3]
    new_dic = {}
    for i, (l, gf1) in enumerate(cases_flag_dic.items()):
        num = clus_ds.where(gf1).mean(co.RL)
        den = clus_ds.where(fls_dic['january night']).mean(co.RL)
        res = num / den
        res = res.to_dataframe()
        tex_index(res)
        # res = res.loc[rr.index]
        # srr_ = r'SRR [\%]'
        res = res.rename({'srr_pt': l}, axis=1)
        new_dic[l] = res
    concat = pd.concat(new_dic.values(), axis=1)
    # concat = concat.loc[rr.index]
    df = concat.stack()
    df.name = 'vals'
    df = df.reset_index()
    df = df.rename({'lab_name':'cluster'},axis=1)
    # return df
    if order is None:
        order = df.set_index(['cluster', 'level_1']).unstack().median(
        axis=1).sort_values(ascending=False).index

    if ax is None:
        f, ax = plt.subplots()
    ax: plt.Axes
    sns.boxplot(x='vals', y='cluster', data=df, sym='',
                color=(1, 1, 1, 0), ax=ax, order=order,
                notch=False
                )
    sns.swarmplot(x='vals', y='cluster', data=df, ax=ax, color=ucp.cc[0],
                  marker='.',
                  order=order)
    ax.axvline(x=1, linestyle='--', alpha=.5)
    plt.show()
    return order
