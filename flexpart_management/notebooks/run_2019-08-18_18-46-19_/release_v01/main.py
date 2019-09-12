# -*- coding: utf-8 -*-
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


# -*- coding: utf-8 -*-
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
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

import funs

mpl.rcParams['figure.dpi'] = 150

# class Dummy:
# def __init__(self):
# # pass

        # %%
path = '/Volumes/mbProD/Downloads/flx_log_coor/run_2019-08-18_18-46-19_'
# flp = FLP.FlexLogPol(path,concat=True)
# selfFLP = FLP.FlexLogPol(path,concat=False)
selfFLP = FlexLogPol.FlexLogPol(
    path,
    #concat=True,
    concat=False,
    get_clusters=False,
    open_merged=True,
    clusters_avail=False
)

# %%
selfFLP.reset_z_levels()

# %%
dsF= selfFLP.filter_hours_with_few_mea()

# %%
dsSM = ds1 = FlexLogPol.smooth_merged_ds(
    dsF
    )

# %%
funs.plot_general(ds1)

# %%
funs.plot_general_lapaz(ds1)

# %%
dsZ = dsSM.copy()
dfcc = selfFLP.get_vector_df_for_clustering(selfFLP.coarsen_par, ar=dsZ[co.CONC])



# %%
funs.plot_hist_values(dfcc)

# %%
funs.plot_hist_all_values(dfcc)

# %%

# %%

# lest create the dataset again
dscc = funs.rebuild_the_dscc(dfcc)

funs.print_percentage_res_time_mass_considered(dscc)

# %%

MAX_LENGTH = 25
dscc = funs.preprocess_dscc_for_clustering(MAX_LENGTH, dscc)

# %%
funs.plot_cells_used_for_clustering(dscc)

# %%
funs.plot_sample_of_vectors_norm_used_for_clustering(dscc)

# %%
funs.plot_hist_all_log(dscc[co.CONC_NORMS])

# %%
funs.plot_hist_all_log(dscc[co.CONC_NORMS].where(dscc[co.LAB_CLUSTER_THRESHOLD]))

# %%
# this one take a long time
dscc = funs.do_clust_multiple(dscc)

# %%
funs.plot_bar_charts_for_each_cluster_set(dscc)

# %%

# %%
dscc = funs.calc_silhouette_scores(dscc)

dscc[co.SIL_SC].plot()

# %%
# ii = 2

# %%
# _d = dscc.loc[{co.CLUS_LENGTH_DIM:ii}][[co.FLAG,co.SIL_SC,SIL_SAMPLE]].stack({co.DUM_STACK:[co.R_CENTER,co.TH_CENTER,co.ZM]})

# %%
funs.plot_sil_score_grid(dscc)

# %%
_n = 4
# _f = 2
_ss1 = funs.get_df_for_plot(_n, dscc)

# %%
_ss1.plot(sharex=True,sharey=True, layout=(2, -1),subplots=True,figsize=(10,5),color=ucp.cc);

# %%
_ss1.plot.area(legend=True, figsize=(12,6),color=ucp.cc)

# %%


# %%
dscc = funs.add_lat_lon_to_dscc(dscc, selfFLP)

# %%
funs.plot_clust_in_bolivia(_n, dscc)

# %%
_n = 18
funs.plot_clust_in_lapaz(_n, dscc)

# %%

_n = 18
funs.plot_clust_bolivia_individual(_n, dscc)

# %%
_f = 2
_n = 18
funs.plot_distance_height_chc(_n, dscc)

# %%
dscc = funs.add_dis_km_dscc(dscc)

# %%

# %%
_cols = 6
_rows = 3
fig, axs = plt.subplots(_rows,_cols,sharex=True,sharey=True,figsize=(2*_cols,2*_rows))
axsf = axs.flatten()
_n=18
funs.plot_dis_height_quantiles_chc(_n, dsF, dscc,axs=axsf)

# %%
dscc[co.CONC].sum([co.TH_CENTER,co.ZM,co.RL]).plot()

# %%
dscc[co.CONC].sum([co.TH_CENTER,co.RL]).plot.line(x=co.R_CENTER);

# %%
_n = 18
funs.plot_influences(_n, dscc)

# %%
_n = 18
less_than = .3
more_than = .15
height_less_than = 1000

funs.plot_target_distance_height_influence(_n, dscc, height_less_than,
                                           less_than, more_than)

# %%

_n = 18
# %%
mdsc = selfFLP.merged_ds.copy()

# %%
_dscc = dscc.drop([co.KMEAN_OBJ,co.CONC,co.CONC_NORMALIZED,co.RL])
_dscc=xr.merge([mdsc,_dscc])

_n = 18
funs.plot_influences(_n, _dscc)

# %%
_n = 18
less_than = .3
more_than = .15
height_less_than = 1000

funs.plot_target_distance_height_influence(_n, _dscc, height_less_than,
                                           less_than, more_than)


_ns = [0,2,8,9,11,14]

for _nn in _ns:

    funs.plot_hour_influence_targeted(_n, _nn, dscc, height_less_than,
                                      less_than, more_than)

# %%
path = '/Volumes/mbProD/Downloads/CHC_QACSM.xlsx'
acsm = pd.read_excel(path)
acsm = acsm.set_index('Date UTC')
acsm = acsm[1:]
acsm = acsm['2018-04-01':]
acsm = acsm.resample('1H').median()
# acsm = acsm.rolling(
#     12,min_periods=1,center=True,win_type='gaussian'
# ).mean(std=4)

# acsm = acsm.rolling(
#     24,min_periods=1,center=True
# ).median()
acsm.index.name = co.RL

# acsm = acsm[(acsm.index<'2018-04-24 00')|(acsm.index>'2018-04-25 00')]




# %%
import scipy.optimize.nnls as nnls

# %%
_n = 18
# _ds = dscc.loc[{CLUS_LENGTH_DIM:_n}].drop(KMEAN_OBJ)
_ds=_dscc.loc[{co.CLUS_LENGTH_DIM:_n}]
_ds[co.CONC]=100*_ds[co.CONC]/_ds[co.CONC].sum([co.R_CENTER,co.TH_CENTER,co.ZM])

# %%
_all_c = set(_ds.coords.keys())

# %%
_dims = set(_ds.dims.keys())

# %%
_drop = list(_all_c - _dims)

# %%
_ds1 = _ds[[co.CONC,co.FLAG]].drop(_drop)

# %%
_ds2 = _ds1.to_dataframe()

# %%
_ds3=_ds2.groupby([co.FLAG,co.RL]).sum()

# %%
_df1 = _ds3.unstack(co.FLAG)[co.CONC]

# %%
cols = _df1.columns

# %%
res2 = pd.merge(acsm,_df1,left_index=True,right_index=True)
res2=res2.dropna()

# %%

# %%
A = res2[cols]
Av = A.values

# %%
# c1 = 'Nitrate'
c1 = 'Sulfate'
b = res2[c1]
# bo = b<4
# b = b[bo]
# A = res2[cols][bo]
# Av = A.values
bv = b.values

# %%
# res = nnls(A,b)
res = nnls(Av[:],bv[:])

# %%
r1 = pd.Series(res[0],index=cols)
r1 = 100*r1/r1.sum()
ax = r1.plot.bar(color = [*ucp.cc,*ucp.cc])
ax.set_xlabel('cluster region')
ax.set_ylabel('weights [%]')

ax.figure.savefig('/tmp/sulf_weights.pdf')


# %%
r0 =res[0]
AA = res2.copy()
c=np.dot(A,np.array(r0))
lab = 'reconstructed Sulfate signal'
AA[lab]=c
AA[lab]=AA[lab][AA[lab]>0]
l1 = 'Sulfate ACSM [ug/m3]'
AA[l1]=AA[c1]
# AA=AA.rename(mapper=str,columns={c1:l1})
ax = AA[[l1,lab]].resample('H').mean().plot()
ax.figure.tight_layout()
ax.figure.savefig('/tmp/abs_mea_cal.pdf')

r0 =res[0]
AA = res2.copy()
c=np.dot(A,np.array(r0))
lab = 'reconstructed Sulfate signal'
AA[lab]=c
AA[lab]=AA[lab][AA[lab]>0]
l1 = 'Sulfate ACSM [ug/m3]'
AA[l1]=AA[c1]
# AA=AA.rename(mapper=str,columns={c1:l1})
ax = AA[[l1]].resample('H').mean().plot()
ax.figure.tight_layout()
ax.figure.savefig('/tmp/abs_mea_cal1.pdf')

# %%
path_bc = '/Users/diego/JUP/co_bc/data/horiba_chc_corrected_diego.csv'
bc,CO,h  = 'abs670','CO_ppbv','hour'
lh = 'Local Time'
dt = 'date'
df = pd.read_csv(path_bc)
df[lh]=np.mod(df[h]-4,24)
df[dt] = pd.to_datetime(df[dt])
df = df.set_index(dt)

# %%
dd = df[bc]['2017-12':'2018-05']

dd.plot(
    marker=',',linewidth=0,
    figsize=(10,5)
)
std=24
# res = dd.rolling(std,min_periods=int(std/4),center=True).median()
res = dd
ax=res.plot()
# ax.set_ylim(.1,12)
# ax.set_yscale('log')

# %%
res.index.name = co.RL
res2 = pd.merge(res,_df1,left_index=True,right_index=True)
res2=res2.dropna()

# %%
import scipy.optimize.nnls as nnls

# %%
bcl='eBC [µg/m³]'
res2[bcl]=res2[bc]/6.6

# %%
A = res2[cols]
Av = A.values

# %%
b = res2[bcl]
bv = b.values

# %%
# res = nnls(A,b)
res = nnls(Av[:],bv[:])

# %%
r0 =res[0]


# %%
AA = res2.copy()
c=np.dot(A,np.array(r0))
cc = 'reconstructed eBC signal'
AA[cc]=c

# %%
ax = AA[[bcl,cc]].resample('H').mean().plot(figsize=(15,5))
ax.figure.tight_layout()
ax.set_xlabel('')
ax.figure.savefig('/tmp/abs_mea_cal.pdf')
ax.set_yscale('log')
ax.set_ylim(.1,5)

# %%
r1 = pd.Series(res[0],index=cols)
r1 = 100*r1/r1.sum()


ax = r1.plot.bar(color = [*ucp.cc,*ucp.cc])
ax.set_xlabel('cluster region')
ax.set_ylabel('weights [%]')
ax.figure.savefig('/tmp/meas_bar_abs.pdf')

# %%
_n = 18
_ds = _dscc.loc[{co.CLUS_LENGTH_DIM:_n}]

# %%
_df = _ds[[co.CONC,co.FLAG]]
_df = _df.drop(list(set(_df.coords)-set(_df.dims))).to_dataframe()

# %%
_df = _df.reset_index()[[co.RL,co.CONC,co.FLAG]]

# %%
_df1 = _df.groupby([co.FLAG,co.RL]).sum()

# %%
_df2 = _df1[co.CONC].unstack(co.FLAG)

# %%
_df3 = 100*(_df2.T/_df2.T.sum()).T

# %%
_df3.to_csv('/tmp/clust18_v00.csv')

# %%
_df3

# %%






