# ---
# jupyter:
#   jupytext:
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
_f=0
_n=18
funs.plot_dis_height_quantiles_chc_single(_f,_n, dsF, dscc,axs=False)

# %%
_ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]
# _ds = dscc.loc[{CLUS_LENGTH_DIM:_n}]
_ds = _ds.drop(co.KMEAN_OBJ)
# _ds = _ds.where(_ds[FLAG]==_f)
_ds = _ds.sum([co.RL])
#         return _ds
_ds1 = xr.merge([_ds, dsF[[co.TOPO]]]).where(
    _ds[co.FLAG] == _f)
_dsum=_ds1.sum([co.TH_CENTER,co.ZM])[co.CONC]
lens=dsum[co.R_CENTER].shift(**{co.R_CENTER:-1})-_dsum[co.R_CENTER]

_slb = _sl = _dsum/lens
_sl = _sl.rolling(**{co.R_CENTER:5},min_periods=1,center=True).mean()

r1,r2 =_sl[co.R_CENTER].quantile([0,1])
rs = np.linspace(r1,r2,30)

_sl1 = _sl.interp(**{co.R_CENTER:rs})

rmin,rmax = weighted_quantile([.1,.9],_sl1[co.R_CENTER].values,_sl1.values)

_ds1 = _ds1.where(_ds1[co.R_CENTER]>rmin).where(_ds1[co.R_CENTER]<rmax)

# %%
_ds1.sum([co.TH_CENTER,co.ZM])[co.CONC].plot()


# %%
from flexpart_management.modules.flx_array import weighted_quantile

# %%

# %%

# %%
_sl.plot(xscale='log')
axsplot()
_sl.plot()

# %%
_slb.plot(xscale='log')

# %%
plt.plot(dscc[co.ZM].values,marker='.',linestyle='',color = ucp.cc[0])
# plt.plot(dscc[co.ZT].values,marker='.',linestyle='',color = ucp.cc[1])

# %%
dscc

# %%
dsF

# %%
_f=17
_ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]
# _ds = dscc.loc[{CLUS_LENGTH_DIM:_n}]
_ds = _ds.drop(co.KMEAN_OBJ)
# _ds = _ds.where(_ds[FLAG]==_f)
_ds = _ds.sum([co.RL])
#         return _ds
_ds1 = xr.merge([_ds, dsF[[co.TOPO]]]).where(_ds[co.FLAG] == _f,0)



# %%
_f=0
axs = False
# def plot_dis_height_quantiles_chc_single(_f, _n, dsF, dscc,axs=False):
if axs is False:
    _, ax = plt.subplots()
else:
    ax = axs[_f]
    
_cm = fa.get_custom_cmap([*ucp.cc, *ucp.cc, *ucp.cc][_f][:3])

_ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}]

_ds = _ds.drop(co.KMEAN_OBJ)

_ds = _ds.sum([co.RL])

_ds1 = xr.merge([_ds, dsF[[co.TOPO]]]).where(_ds[co.FLAG] == _f)
_ds1 = _ds1.swap_dims({co.R_CENTER: co.DIS})

_ds2 = _ds1/dsF[co.ZLM]

_ds3 = _ds2[co.CONC]
zmin,zmax = _ds2[co.ZM].quantile([0,1])
zz = np.arange(zmin,zmax,zmin)

zl = zz[1]-zz[0]

_ds4 = _ds3.interp(**{co.ZM:zz})*zl

ZREAL = 'ZREAL'
_ds4[ZREAL]=_ds4*0+_ds4[co.ZM]+((_ds4[co.TOPO]/zl).round()*zl)

_dims = set(_ds4.dims)

_keep = _dims.union(set([ZREAL]))

_coor = set(_ds4.coords)

_drop = list(_coor-_keep)

_ds5=_ds4.drop(_drop).to_dataframe()

_ds6 = _ds5.reset_index().groupby([ZREAL,co.DIS,co.TH_CENTER]).sum()[[co.CONC]].to_xarray()

_ds6.sum(co.TH_CENTER)[co.CONC].plot(xscale='log',vmin=0,ax=ax,cmap=_cm)

HEIGHT = 'HEIGHT'
_ds1[HEIGHT] = (_ds1[co.TOPO] + _ds1[co.ZM])

_dg = _ds1[[HEIGHT, co.CONC]].to_dataframe()[[HEIGHT, co.CONC]]
_dg = _dg.groupby(co.DIS)

_dh = (_ds1[co.CONC] * (_ds1[co.TOPO] + _ds1[co.ZM])).mean(
    [co.TH_CENTER, co.ZM])
_dh = _dh / (_ds1[co.CONC].mean([co.TH_CENTER, co.ZM]))

ax.set_xlim(10, 2e3)

_dh = (_ds1[co.CONC] * (_ds1[co.TOPO])).mean([co.TH_CENTER, co.ZM])
_dh = _dh / (_ds1[co.CONC].mean([co.TH_CENTER, co.ZM]))

_dh.plot(x=co.DIS, color='k', ax=ax)
ax.set_xscale('log')

ax.set_xlim(5, 2e3)
ax.set_ylim(0, 1.5e4)
ax.set_title(str(_f))
ax.grid(color='k',alpha=.3,linestyle='--')
ax.set_axisbelow(False)
ax.set_facecolor('white')

# %%
fig.tight_layout()
fig

# %%
# !jupyter-nbconvert --to markdown scratch.ipynb

# %%
