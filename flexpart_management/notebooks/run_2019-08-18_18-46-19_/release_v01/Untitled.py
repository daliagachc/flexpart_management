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
v1 = np.array([10,20,30])
v2 = np.array([3,4,5])


# %%
def f1(v1,v2):
    print(v1)
    print(v2)
#     return v1*v2
    return 0


# %%
f1v = np.vectorize(f1)

# %%
f1v1 = np.vectorize(f1,excluded=['v1'])

# %%
f1v(v1,v2)

# %%
np.zeros()

# %%
f1v1(v1,v2)

# %%
f1v1(v1=v1,v2=v2)

# %%
_dm

# %%
k.reshape(-1,1).T

# %%

# %%
_sil_sc.sel(**{CLUS_LENGTH_DIM:3}) = 3

# %%
=4

# %%
_sil_sc

# %%
_ss['m']=_ss.set_index(co.RL).index.month

# %%
_ss=_s.groupby(co.RL).sum()

_ss1 = _ss.resample('4H').mean()
# _ss1.index = _ss1.index+pd.Timedelta(hours=1.5)

_ss1

# %%
_ss1.index = _ss1.index+pd.Timedelta(hours=1.5)

# %%
_ss1.index

# %%
_ss=_s.groupby([co.RL,FLAG]).sum()

# %%
_ss1.T.sum()

# %%

# %%

# %%
_ds = dsF[[co.LAT_00,co.LON_00,co.LAT_10,co.LON_10,co.LAT_11,co.LON_11,co.LAT_01,co.LON_01]]

# %%



# %%
_f = 0
_ds = dscc.loc[{CLUS_LENGTH_DIM:_n}]
_km = _ds[co.R_CENTER]*100

DIS = 'Distance [km]'
_km.name=DIS

_ds = _ds.assign_coords(**{DIS:_km})

# %%
# _ds = dscc.loc[{CLUS_LENGTH_DIM:_n}]
_ds = _ds.drop(KMEAN_OBJ)
_ds = _ds.where(_ds[FLAG]==_f)
_ds = _ds.sum([co.RL])

# %%
_ds1 = xr.merge([_ds,dsF[co.TOPO].mean(co.RL)]).where(_ds[FLAG]==_f)

# %%
_dh = (_ds1[co.CONC]*(_ds1[co.TOPO]+_ds1[co.ZM])).mean([co.TH_CENTER,co.ZM])
_dh = _dh/(_ds1[co.CONC].mean([co.TH_CENTER,co.ZM]))

_,ax = plt.subplots()
_dh.plot(x=DIS,color = [*ucp.cc,*ucp.cc][_f],ax=ax)
ax.set_xscale('log')
# ax.set_yscale('log')
ax.set_xlim(10,2e3)
# ax.set_ylim(25e1,2e4)
ax.set_title(str(_f));

# %%
_dh = (_ds1[co.CONC]*(_ds1[co.TOPO])).mean([co.TH_CENTER,co.ZM])
_dh = _dh/(_ds1[co.CONC].mean([co.TH_CENTER,co.ZM]))

# _,ax = plt.subplots()
_dh.plot(x=DIS,color = 'k',ax=ax)
ax.set_xscale('log')
# ax.set_yscale('log')
ax.set_xlim(10,2e3)
# ax.set_ylim(25e1,2e4)
ax.set_title(str(_f));

# %%
ax.figure

# %%

# %%

# %%
_ds1

# %%
.groupby(co.R_CENTER)

# %%

funs


# %%
_dg.plot()

# %%

# %%

# %%

# %%

# %%
_df

# %%
