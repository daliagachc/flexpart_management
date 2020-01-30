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
import numpy
import seaborn
import xarray
from matplotlib import pyplot
from useful_scit import plot
from useful_scit.imps import *
import flexpart_management.modules.flx_array as fa
# %%
from flexpart_management.modules import constants as co


def lab2name(l,lab_name_dict):
    if np.isnan(l):
        ret = np.nan
    else:
        ret = lab_name_dict[l]
    return ret

def get_lab_name(ds_zg, lab_name_dict):
    dalab: xr.DataArray = ds_zg['lab']
    def l2n(l): return lab2name(l,lab_name_dict)
    res = xr.apply_ufunc(l2n, dalab.load(), vectorize=True,
                         output_dtypes=[str])
    return res


# %%
def get_lab_agl(ds_zg, ds_zs, lab_name_dict):
    da_lab = ds_zs['lab']
    topo = (da_lab[co.TOPOGRAPHY] / 500).round() * 500
    da_lab['z'] = da_lab * 0 + da_lab[co.ZM] - topo
    df = da_lab.reset_coords()[['z', 'lab']].to_dataframe().reset_index()
    # %%
    df1 = df[df['z'] > 0].drop(co.ZM, axis=1).rename({'z': co.ZM}, axis=1)
    new_lab = df1.set_index(
        [co.R_CENTER, co.TH_CENTER, co.ZM]
    ).sort_index().to_xarray()
    # %%
    dsm: xr.DataArray = xr.merge([ds_zg, new_lab])
    dsm = dsm.assign_coords({'lab': dsm['lab']})
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    lab_name = get_lab_name(dsm, lab_name_dict)
    dsm = dsm.assign_coords({'lab_name': lab_name})
    return dsm


def get_time_series_sfc_tot(dsm,lab_name_dict):
    ds_tot = dsm['CONC'].sum(fa.get_dims_complement(dsm, co.RL))
    daz: xr.DataArray = (dsm / ds_tot * 100)['CONC'].rename('conc_tot')
    daz0: xr.DataArray = daz[{co.ZM: 0}].rename('conc_sfc')
    ts = daz.groupby('lab').sum()
    ts0 = daz0.groupby('lab').sum().drop([co.ZT, co.ZM])
    # %%
    tts = xr.merge([ts, ts0])

    # %%
    def l2n(l): return lab2name(l, lab_name_dict)

    vec_l2n = np.vectorize(l2n)
    lab_name = xr.DataArray(
        vec_l2n(tts['lab']),
        coords={'lab': tts['lab']}, dims=['lab'])
    tts = tts.assign_coords({'lab_name': lab_name}).load()
    return tts


def get_time_series_df(tts):
    tsdf = tts.to_dataframe().reset_index().set_index(co.RL)
    _boo = tsdf['conc_sfc'] > 0
    tsdf['conc_sfc'][~_boo] = 0
    tsdf['rat_sfc_tot']=tsdf['conc_sfc']/tsdf['conc_tot']
    return tsdf


def plot_ts_conc_sfc_tot(lab_name_dict, tsdf):
    for i in range(18):
        concs = ['conc_tot', 'conc_sfc']
        # i=3
        _boo = tsdf['lab'] == i
        f, ax = plt.subplots(figsize=(20, 5))
        tsdf[_boo][concs].plot(ax=ax)
        ax.set_title(lab_name_dict[i])
        plt.tight_layout()
        plt.show()


def plot_scatter_sfc_tot(lab_name_dict, tsdf):
    for i in range(18):
        _boo = tsdf['lab'] == i
        tsdf[_boo].plot(x='conc_tot', y='conc_sfc', kind='scatter', alpha=.2,
                        marker='.',
                        label=i, title=lab_name_dict[i])
        plt.show()



def plot_ratio_clusters(prop_df,tsdf):
    sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    ucp.set_dpi(150)
    _ts = tsdf[tsdf['rat_sfc_tot'] >= 0]
    i2r_dic = prop_df.set_index('cluster_i')[co.R_CENTER].to_dict()
    i2r = np.vectorize(lambda x: i2r_dic[x])
    _ts['r'] = i2r(_ts['lab'])
    _order = prop_df.sort_values(co.R_CENTER)['short_name']
    name = "lab_name"
    cd = dict(SR=ucp.cc[0], SM=ucp.cc[1], MR=ucp.cc[2], LR=ucp.cc[3])
    colors = {}
    for l, r in prop_df.sort_values(co.R_CENTER).iterrows():
        colors[r['short_name']] = cd[r['range']]
    g = sns.FacetGrid(_ts, col=name,
                      hue=name,
                      aspect=1/10, height=7,
                      col_order=_order,
                      sharex=False,
                      palette=colors,
                      ylim=(1.1,-.1)
                      )
    ops = dict(clip_on=False, alpha=1, lw=1.5, bw=.01, cut=3, vertical=True)
    g.map(sns.kdeplot, "rat_sfc_tot", shade=True, **ops)
    g.map(sns.kdeplot, "rat_sfc_tot", shade=False, color='w', **ops)
    # g.map(sns.distplot,"rat_sfc_tot",kde=False,hist_kws=dict(alpha=1),bins=np.linspace(0,1,30))
    g.map(plt.axvline, x=0, lw=2, clip_on=False)
    for x in list(np.arange(0, 1.1, .1)):
        g.map(plt.axhline, y=x, lw=1, color='w', alpha=1)

    def label_fun(x, color, label):
        # print(args)
        # print(kwargs)
        ax = plt.gca()
        ax.text(.05, 1, label,
                # fontweight="bold",
                # color=color,
                ha="left", va="center", transform=ax.transAxes)

    g.map(label_fun, "rat_sfc_tot")
    g.fig.subplots_adjust(wspace=-.4)
    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(xticks=[])
    g.despine(bottom=True, left=True)
    g.set_ylabels('distribution for the ratio surface/total')
    g.set_xlabels('')
    [ax.set_zorder(30 - i) for i, ax in enumerate(g.axes[0])]
    # return g
    plt.show()


def create_sfc_tot_ds_with_attrs(tsdf):
    new_ts = tsdf.sort_index().reset_index().set_index([co.RL, 'lab_name'])
    new_ds = new_ts.to_xarray().set_coords('lab')
    # %%
    conc_tot = dict(
        short_name='SRR',
        description='source receptor relationship for each cluster i such that $sum_{i}{SRR} = 100$',
        units='%'
    )
    conc_sfc = dict(
        short_name='SRRz0',
        description='source receptor relationship for each cluster i below 500 magl',
        units='%'
    )
    rat_sfc_tot = dict(
        short_name='SRRz0/SRR',
        description='ratio between SRRz0 and SRR for each cluster i',
        units='%'
    )
    new_ds['conc_tot'].attrs = conc_tot
    new_ds['conc_sfc'].attrs = conc_sfc
    new_ds['rat_sfc_tot'].attrs = rat_sfc_tot
    return new_ds