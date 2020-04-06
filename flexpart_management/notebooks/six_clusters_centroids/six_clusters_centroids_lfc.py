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
from flexpart_management.modules import flx_array as fa
from flexpart_management.modules import constants as co
plt;
# %%
def from_asl_agl(*,
                 ds,
                 ds_var='conc_norm',
                 delta_z=500,
                 z_top=15000,
                 ds_var_name_out=None
                 ):
    import wrf
    log.ger.warning(
        f'this will only work if ds z levels are constant')
    t_list = [co.ZM, co.R_CENTER, co.TH_CENTER]

    d3d = ds[ds_var]  # .sum( [ co.RL ] )
    d3d_attrs = d3d.attrs
    d3d = d3d.transpose(
        co.RL, *t_list, transpose_coords=True
    )
    rounded_zm = np.round(d3d[co.ZM] / delta_z) * delta_z
    rounded_topo = np.round(d3d[co.TOPO] / delta_z) * delta_z
    dz = rounded_zm - rounded_topo
    dz = dz.transpose(*t_list, transpose_coords=True)
    dz = dz.reset_coords(drop=True)
    # %%
    d3d = d3d.reset_coords(drop=True)
    # %%
    # print( d3d.shape )
    # print( dz.shape )
    # %%
    z_lev = np.arange(delta_z / 2, z_top, delta_z)
    da_interp = wrf.interplevel(d3d, dz, z_lev)
    da_reinterp = da_interp.rename(level=co.ZM)

    # %%
    ds_chop = ds.isel({co.ZM: slice(0, len(da_reinterp[co.ZM]))})
    for coord in list(ds.coords):
        da_reinterp = da_reinterp.assign_coords(
            **{coord: ds_chop[coord]})
    if ds_var_name_out is not None:
        da_reinterp.name = ds_var_name_out

    # we do this in order to avoid the problem of setting attributes
    # to none that cannot be saved using to netcdf.
    da_reinterp.attrs = d3d_attrs

    ds_reinterp = da_reinterp.to_dataset()
    # todo: check that concentrations are the same after resampling
    return ds_reinterp

def get_r_dis_dic(da, ls, lss):
    _dic = {}
    for la in lss:
        boo = da[ls] == la
        dw = da.where(boo)
        _ds = (dw * dw[co.R_CENTER]).sum()
        _dc = dw.sum()
        dR = _ds / _dc
        val = dR.load().item()
        _dic[la] = val
    return _dic

def get_th_dic(da, ls, lss):
    _dic = {}
    for la in lss:
        boo = da[ls] == la
        dw = da.where(boo)
        x = (dw * np.sin(dw[co.TH_CENTER])).sum()
        y = (dw * np.cos(dw[co.TH_CENTER])).sum()

        dR = np.mod(np.arctan2(x,y),2*np.pi)

        val = dR.load().item()
        _dic[la] = val
    return _dic


def get_agl_dic(da, ls, lss):
    _dic = {}
    for la in lss:
        boo = da[ls] == la
        dw = da.where(boo)
        _ds = (dw * dw[co.ZM]).sum()
        _dc = dw.sum()
        dR = _ds / _dc
        val = dR.load().item()
        _dic[la] = val
    return _dic

def get_asl_dic(da, ls, lss):
    _dic = {}
    for la in lss:
        boo = da[ls] == la
        dw = da.where(boo)
        _ds = (dw * (dw[co.ZM]+dw[co.TOPO])).sum()
        _dc = dw.sum()
        dR = _ds / _dc
        val = dR.load().item()
        _dic[la] = val
    return _dic

def get_ratio_dic(da, ls, lss):
    _dic = {}
    for la in lss:
        boo = da[ls] == la
        dw = da.where(boo)
        _ds = dw.where(dw[co.ZM]<1500).sum()
        _dc = dw.sum()
        dR = _ds / _dc
        val = dR.load().item()
        _dic[la] = val
    return _dic

def get_srr_dic(da, ls, lss):
    _dic = {}
    tot = da.sum([co.ZM,co.TH_CENTER,co.R_CENTER])
    da_no = da/tot
    da_tot = da_no.sum().load().item()

    for la in lss:
        boo = da[ls] == la
        dw = da_no.where(boo)
        _ds = dw.sum()
        # _dc = dw.sum()
        # dR = _ds / _dc
        val = _ds.load().item()
        _dic[la] = val * 100 / da_tot
    return _dic



mark_dic = {
    '12_PW':"d",
    '08_PW':"h",
    '05_PW':"*",
    '11_PW':"P",
    '03_PW':"p",
    '07_PW':">",
}

def create_dic_df(*,agl,ratio,r,rrs,asl,th):
    labs = ['agl', 'ratio', 'r','rrs','asl','th']
    df = pd.DataFrame([agl,ratio,r,rrs,asl,th], index=labs).T
    df['dis'] = df['r'] * 100
    df['ratio'] = df['ratio'] * 100
    df['agl'] = df['agl']/1000
    df['asl'] = df['asl']/1000
    col_se = pd.Series(co.pw_col_dict)
    df['col'] = col_se
    df['mark'] = pd.Series(mark_dic)
    return df

def get_df(da, ls):
    lss = np.unique(da[ls])
    lss = list(set(lss) - {'nan'})
    # %%
    _dic_sum = get_r_dis_dic(da, ls, lss)
    # %%
    _dic_agl = get_agl_dic(da, ls, lss)
    # %%
    _dic_asl = get_asl_dic(da, ls, lss)
    # %%
    _dic_ratio = get_ratio_dic(da, ls, lss)
    # %%
    _dic_rrs = get_srr_dic(da, ls, lss)
    # %%
    _dic_th = get_th_dic(da,ls,lss)
    # %%
    df = create_dic_df(
        agl=_dic_agl, ratio=_dic_ratio, r=_dic_sum,
        rrs=_dic_rrs, asl=_dic_asl,th =_dic_th
    )
    df = df.sort_index()
    return df


def get_da(con):
    ds = xr.open_mfdataset(
        pjoin(co.tmp_data_path, 'ds_clustered_18_agl.nc'),
        combine='nested',
        concat_dim=co.RL
    )
    ds['lab'] = ds['lab'][{co.RL: 0}]
    ds['lab_nc06'] = ds['lab_nc06'][{co.RL: 0}]
    ds['lab_name'] = ds['lab_name'][{co.RL: 0}]
    ds = ds.set_coords(names=['lab', 'lab_name', 'lab_nc06'])
    # %%
    da: xr.DataArray = ds[con]
    return da

def plot_nc6_vert_props(df)->plt.Figure:
    f, axs = plt.subplots(
        2, 2,
        figsize=(7.25, 7.25 / 1.4), sharex=False, dpi=300
    )
    # y_label = 'sdf'
    _ax: plt.Axes
    axf = axs.flatten()
    _ax = axs[0, 0]
    # _ax.scatter(df['dis'], df['agl'], c=df['col'],marker=df['mark'])
    for l, r in df.iterrows():
        # print(r)
        _ax.annotate(l, r[['dis', 'agl']], color=r['col'], alpha=.5,
                     xytext=[5, -5],
                     textcoords='offset points',
                     size=7)

        _ax.scatter([r['dis']], [r['agl']],
                    c=[r['col']],
                    marker=r['mark']
                    )
    _ax.set_ylim(0, 8)
    _ax.set_ylabel('height above ground [km]\n')
    _ax = axs[0, 1]
    # _ax.scatter(df['dis'], df['asl'], c=df['col'])
    for l, r in df.iterrows():
        _ax.scatter(r['dis'], r['asl'], c=[r['col']], marker=r['mark'])
    # _ax.axhline(5.2, linestyle='--',c='k',alpha=.3, linewidth=1)
    # _ax.annotate('CHC',[10,5.25],size=6,alpha=.3)
    _ax.annotate('CHC', xy=[5, 5.2],
                 xytext=[0, 0],
                 textcoords='offset points',
                 zorder=12,
                 alpha=.5,
                 fontsize=6,
                 # arrowprops=dict(arrowstyle='-', alpha=.5),
                 horizontalalignment = 'center',
                 verticalalignment = 'center'

                 )
    _ax.set_ylim(3.9, 8)
    _ax.set_ylabel('height above sea level [km]')
    _ax = axs[1, 0]
    _ax.vlines(df['dis'], 0, df['ratio'], color=df['col'], alpha=.5)
    for l, r in df.iterrows():
        _ax.scatter(r['dis'], r['ratio'], c=[r['col']], marker=r['mark'])
    _ax.set_ylim(-10, 100)
    y_label = r'$\frac{\mathrm{SRR}_{<1.5\mathrm{km}}}{\mathrm{SRR}_{' \
              r'\mathrm{total}}}\ [\%]$'
    _ax.set_ylabel(y_label)
    _ax = axs[1, 1]
    _ax.vlines(df['dis'], 0, df['rrs'], color=df['col'], alpha=.5)
    # _ax.scatter(df['dis'], df['rrs'], c=df['col'])
    for l, r in df.iterrows():
        _ax.scatter(r['dis'], r['rrs'], c=[r['col']], marker=r['mark'])
    _ax.set_ylim(-3, 30)
    _ax.set_ylabel('SRR [%]')
    for ax in axf:
        ax.set_xlim(-50, 1199)
        sns.despine(ax=ax,trim=True)
    for ax in axs[1, :]:
        ax.set_xlabel('distance from CHC [km]')
    for ax in axs[0, :]:
        sns.despine(ax=ax,bottom=True)
        ax.set_xticks([])
    for ax, l in zip(axf, 'abcd'):
        ax.annotate(f'{l}', [0.02, 1.05], xycoords='axes fraction',
                    weight='bold')
    plt.tight_layout()
    plt.show()
    return f

def get_nc18_order():
    _d = {'SR': 0, 'SM': 1, 'MR': 2, 'LR': 3}
    dic_186: pd.DataFrame = pd.read_csv(
        pjoin(co.tmp_data_path, 'nc_18_nc_06.csv'))
    dic_186['range'] = dic_186['18_NC'].str[-2:]
    dic_186['sr'] = dic_186['range'].apply(lambda v: _d[v])
    dic_186 = dic_186.sort_values(['06_NC', 'sr'])
    return dic_186