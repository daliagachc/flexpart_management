# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import *
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co
mpl.rcParams['figure.dpi'] = 150

# %%
# log.ger.setLevel(log.log.DEBUG)
log.ger.setLevel(log.log.INFO)
# %%
def swap_xy2lon_lat(nds):
    _boo1 = (nds[co.XLONG].max(co.SOUTH_NORTH) - nds[co.XLONG].min(
        co.SOUTH_NORTH)).sum().item() == 0
    # %% {"jupyter": {"outputs_hidden": true}}
    _boo2 = (nds[co.XLAT].max(co.WEST_EAST) - nds[co.XLAT].min(
        co.WEST_EAST)).sum().item() == 0

    log.ger.debug('_boo1 is %s',_boo1)

    if _boo1 and _boo2:
        log.ger.debug('inside loop')
        xx = [co.XLAT, co.XLONG]
        ww = [co.WEST_EAST, co.SOUTH_NORTH]
        vv = [co.VLAT, co.VLONG]
        rr = [co.VLONG, co.VLAT]
        # %% {"jupyter": {"outputs_hidden": true}}
        for i in range(2):
            ff = nds[xx[i]].mean(ww[i])
            ff.name = vv[i]
            nds = nds.assign_coords(**{vv[i]: ff})
        for i in range(2):
            nds = nds.swap_dims({ww[i]: rr[i]})
    return nds


def get_combined_flx_ds(DD, dir_path,chop_list=-1):
    _ds_list = fa.get_flx_ds_list(DD, dir_path)
    _ds_list = _ds_list[:chop_list]
    # %% {"jupyter": {"outputs_hidden": true}}
    ds_list = fa.trim_flx_ds_list(_ds_list)
    # %% {"jupyter": {"outputs_hidden": true}}
    dsm = xr.open_mfdataset(ds_list, concat_dim=co.TIME, combine='nested')
    dsm = fa.convert_ds_time_format(dsm)
    dsm = fa.remove_ageclass(dsm)
    # %% {"jupyter": {"outputs_hidden": true}}
    hds = fa.import_head_ds(dir_path, DD)
    hds = hds.drop_dims([co.SPECIES, co.RECEPTORS, co.TIME, co.AGECLASS])
    # %% {"jupyter": {"outputs_hidden": true}}
    nds = xr.merge([hds, dsm])
    nds.attrs = hds.attrs.copy()
    nds = fa.add_zmid(nds)
    for v in (set(co.HEAD_VARS) & set(hds.variables)):
        nds = nds.assign_coords(**{v: nds[v]})
    _cr = co.RELEASENAME
    _df = nds[_cr].to_pandas().str.decode("utf-8")
    _df = pd.to_datetime(_df, format='chc%Y%m%d_%H')
    nds = nds.assign_coords(**{co.RELEASE_TIME: _df.to_xarray()})
    nds = nds.swap_dims({co.BT:co.ZM})


    return nds


def __main__():
    pass
# %%
dir_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-10_11-10-03_/2017-12-31'

# %%
# concat_ds = fa.concat_file_ds_list(ds_list)

# %%
DD = co.D2
nds = get_combined_flx_ds(DD, dir_path)
nds = swap_xy2lon_lat(nds)
# nds = nds[{co.RL:-1}]


# %%
_da = nds[co.CONC][{co.RL:23}]

# %%
_da1 = _da.sum([co.VLAT],keep_attrs=True).load()

# %%
# _da2 = _da1.loc[{co.VLONG:slice(-68.5,-67),co.ZM:slice(0,1e4)}]
_da2 = _da1


# %%
args = dict(
    x=co.DIS,
    y=co.ZM,
    norm=mpl.colors.LogNorm(),
    vmin=10,vmax=50000
)

# %%
# fig,ax=plt.subplots(figsize=(10,5))
__da2 = _da2.copy()
__da2[co.DIS] = __da2[co.VLONG]*100
__da2[co.DIS] = __da2[co.DIS].assign_attrs(units='km')
__da2[co.DIS]=(__da2[co.DIS]/100-co.CHC_LON)*100
__da2[co.DIS]=__da2[co.DIS].assign_attrs(units='km')

__da2.plot(**{
    **args,
    'add_colorbar':True,
    'cmap': plt.get_cmap('Reds'),
    'norm':mpl.colors.Normalize(),
    'vmax':80,
    'col':co.TIME,
    'col_wrap':4,
    'ylim':(0,2e3),
    'xlim':(-5,5)
}

)
# ax.grid(True)
# ax.set_axisbelow(False)
# ax.xaxis.set_tick_params(rotation=90)
# ax.set_ylim(0,.2e4)
xl = 5
# ax.set_xlim(-xl,xl);


# %% {"jupyter": {"outputs_hidden": true}}
_dss = _da2.sum(co.VLONG, keep_attrs = True)
_fg = _dss.plot(col=co.TIME,y=co.ZM,col_wrap=4,ylim=(0,4e3))

_v = _da2.sum([co.VLONG,co.TIME],keep_attrs = True)

q50=fa.weighted_quantile(.5,_v[co.ZM],sample_weight=_v.values)

_lt = len(_dss[co.TIME])
for i,ax in enumerate(_fg.axes.flatten()[:_lt]):
    _di = _dss.isel(**{co.TIME:i})
    _q50=fa.weighted_quantile(.5,_di[co.ZM],_di.values)
    _tot = _di.sum().item()
    ax.axhline(q50,color='k',linestyle='--',alpha=.5,label=f'global median = {np.round(q50)}')
    ax.axhline(_q50,color='r',linestyle='--',alpha=.5,label=f'global = {np.round(_q50)}')
    ax.axhline(_q50,color='r',linestyle='-',alpha=.5,label=f'tot = {np.round(_tot)}')
    ax.legend()




# %%
_da.sum(fa.get_dims_complement(_da,[co.TIME])).plot()

# %%
nds[co.CONC].sum(fa.get_dims_complement(nds[co.CONC],[co.TIME])).plot()

# %%
_n = nds[{co.RL:-1}]

_n1 = _n.coarsen(**{co.TIME:11},boundary='trim').sum().sum(co.ZM)[co.CONC].load()

_n1.plot.pcolormesh(col=co.TIME,col_wrap=5)

# %%
args = {'norm':mpl.colors.LogNorm(vmin=10,vmax=500),'cmap':plt.get_cmap('Reds')}
ylim = (5e2,1e4)

def plot_multiple_view_parts(_in, args, nds, ylim):
    _n = nds[{co.RL: _in}][co.CONC]
    _n = _n.where(_n > 0)
    _n = _n.dropna(dim=co.TIME, how='all')
    _n = _n[{co.TIME: slice(-24, None)}]
    _n1 = _n.coarsen(**{co.TIME: 2}, boundary='trim').sum().sum(co.ZM).load()
    _n1.plot.pcolormesh(col=co.TIME, col_wrap=5, **args)
    _n1 = _n.coarsen(**{co.TIME: 2}, boundary='trim').sum().sum(co.VLAT).load()
    _n1.plot.pcolormesh(col=co.TIME, col_wrap=5, yscale='log', ylim=ylim,
                        **args)
    _n1 = _n.coarsen(**{co.TIME: 2}, boundary='trim').sum().sum(co.VLONG).load()
    _n1.plot.pcolormesh(col=co.TIME, col_wrap=5, yscale='log', ylim=ylim,
                        **args)


# %%
plot_multiple_view_parts(1, args, nds, ylim)

# %%

# %%
plot_multiple_view_parts(-1, args, nds, ylim)

# %%
# !jupyter-nbconvert --to markdown ./check_heght.ipynb

# %%
plot_multiple_view_parts(-2, args, nds, ylim)



xr.DataArray.plot