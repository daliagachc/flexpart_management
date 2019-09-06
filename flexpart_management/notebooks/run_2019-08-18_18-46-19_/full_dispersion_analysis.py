# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2


# %%
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FLP
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

# %%
path = '/Volumes/mbProD/Downloads/flx_log_coor/run_2019-08-18_18-46-19_'
# flp = FLP.FlexLogPol(path,concat=True)
# self = FLP.FlexLogPol(path,concat=False)
self = FLP.FlexLogPol(
    path,
#     concat=True,
    concat=False,
    get_clusters=False,
    open_merged=True,
    clusters_avail=False
)

# %%

# %%
self.reset_z_levels()

# %%
dsF= self.filter_hours_with_few_mea()


# %%
dsSM = ds1 = FLP.smooth_merged_ds(
    dsF
    )

# %%
cl = co.CPer
c1 =ds1[cl].sum([co.RL,co.ZM])
c2 = ds1[cl].sum([co.ZM,co.RL,co.TH_CENTER])
ar = c1/c2
# ar = c1
ar = ar.isel(**{co.R_CENTER:slice(0,-3)})
ax = fa.get_ax_bolivia(fig_args={'figsize':(5,5)})
fa.logpolar_plot(ar,name=co.CPer,ax=ax,perM=.95,perm=.01)
ax.set_xlim(-75,-60)
ax.set_ylim(-25,-7)
# ax = fa.get_ax_lapaz()
# fa.logpolar_plot(ar,name=co.CPer,ax=ax,perM=.95)


# %%
ax.figure.savefig('/tmp/map.pdf')

# %%

# %%
ds1.sum([co.ZM,co.RL,co.TH_CENTER])[co.CPer].plot(marker='.',xscale='log')

# %%
lines = ds1.sum([co.RL,co.TH_CENTER])[co.CPer].plot(marker='.',xscale='log',hue=co.ZM)

# %%
cl = co.CPer
c1 =ds1[cl].sum([co.RL,co.ZM])
c2 = ds1[cl].sum([co.ZM,co.RL,co.TH_CENTER])
ar = c1/c2
ar = c1
ar = ar.isel(**{co.R_CENTER:slice(0,-3)})
ax = fa.get_ax_bolivia()
fa.logpolar_plot(ar,name=co.CPer,ax=ax,perM=.999,perm=.1)
ax.set_xlim(-75,-60)
yl=ax.set_ylim(-25,-7)
# ax = fa.get_ax_lapaz()
# fa.logpolar_plot(ar,name=co.CPer,ax=ax,perM=.95)

# %%
ax.figure.savefig('/tmp/gen_fig.pdf')

# %% [markdown]
# # new part

# %%
dsZ = dsSM

# %%
dfcc = self.get_vector_df_for_clustering(self.coarsen_par,ar=dsZ[co.CONC])

# %%
nc = 21

# %%
dfres = self.python_cluster(
    random_state=222,
    n_cluster=nc,
    df=dfcc,
    return_df=True,
    
)

# %%
dsZ[co.ClusFlag]=dfres[co.ClusFlag].to_xarray()

# %%
dg = dsZ.assign_coords(**{co.ClusFlag:dsZ[co.ClusFlag],co.TOPO:dsZ[co.TOPO]})
dg = dg.groupby(co.ClusFlag)
dg = dg.sum('stacked_R_CENTER_TH_CENTER_ZMID')

# %%
df = dg.to_dataframe()

# %%
df1 = df[co.CPer]

# %%
df2 = df1.unstack(co.ClusFlag)

# %%
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')

# %%
FLP.COLORS = [*FLP.COLORS,*FLP.COLORS]

# %%
set_matplotlib_formats('png')
axs = df2.plot(subplots=True,sharex=True,sharey=True,color = FLP.COLORS,
              figsize=(10,5),layout=(int(np.ceil(nc/3)),3),grid=True,marker='.',linewidth=0,alpha=.1,
              legend=True)
df3= df2.rolling(45*24,center=True,min_periods=1,win_type='gaussian').mean(std=45*24)
axs = df3.plot(
    subplots=True,sharex=True,sharey=True,layout=(int(np.ceil(nc/3)), 3),color = FLP.COLORS,
    ylim = (0,50),grid=True,figsize=(10,5),linewidth=4,ax =axs.flatten()[:nc],
    legend=False
              )

# %%
axs[0].figure.savefig('/tmp/inf.pdf')

# %%
axs = df2.plot.area(
    subplots=False,
    layout=(int(np.ceil(nc/3)), 3),color = FLP.COLORS,
    ylim = (0,100),grid=True,figsize=(10,5),linewidth=0,
    legend=False
              )

# dd = df[bc]['2017-12':'2018-05']*10

# dd.plot(
#     marker=',',linewidth=0,
#     figsize=(10,5),
#     color='k'
# )
# std=24
# res = dd.rolling(std,min_periods=int(std/4),center=True,win_type='gaussian').mean(std=.5*std)
# ax=res.plot(figsize=(20,10),color='k',linewidth=2)
# # ax.set_ylim(.1,8)
# # ax.set_yscale('log')
# std=24*30
# res = dd.rolling(std,min_periods=int(std/4),center=True,win_type='gaussian').mean(std=.5*std)
# ax=res.plot(figsize=(10,5),color='k',linewidth=2)
# # ax.set_ylim(.1,8)
# # ax.set_yscale('log')

# %%
axs.figure.savefig('/tmp/inf_area.pdf')

# %%
# top = np.asscalar(
#     (dsZ[co.CPer]/c2).quantile(.9999)
# )
# c2 = dsSM[co.CPer].sum([co.ZM,co.RL,co.TH_CENTER])
# for ii in range(1):
#     ax = fa.get_ax_bolivia(
#         fig_args={'figsize':(5,5)})
#     for i in range(nc):
#         cmap = fa.get_custom_cmap(self.colors[i])
#         ds1 = dsZ[co.CPer].where(dsZ[co.ClusFlag]==i)
#         ds1 = ds1.isel(**{co.ZM:ii})
#         ds2 = ds1.sum(co.RL)
#         ex = ds2.sum().values > 0
#         if ex:
#             fa.logpolar_plot(
#                 ds2,name=co.CPer,ax=ax,perM=.99,perm=0,quantile=True,colorbar=False,
#                 patch_args={'cmap':cmap}
#             )
#     ax.set_xlim(-75,-60)
#     ax.set_title(ii)
#     yl=ax.set_ylim(-25,-7)

# %%
ax.figure.savefig('/tmp/clus_res.pdf')

# %%
ii=5
ds_fl = dsZ[co.CPer].where(dsZ[co.ClusFlag]==ii)

# %%
ax = fa.get_ax_bolivia()
cmap = fa.get_custom_cmap(self.colors[ii])
fa.logpolar_plot(ds_fl.sum([co.RL,co.ZM]),
                 name=co.CPer,ax=ax,
                 patch_args={'cmap':cmap}
                )
ax.set_xlim(-75,-60)
yl=ax.set_ylim(-25,-7)

# %%
import simplekml

# %%
import simplekml
kml = simplekml.Kml()

# %%
dsZ1 = dsZ.assign_coords(**{
    co.ClusFlag:dsZ[co.ClusFlag],
    co.TOPO:dsZ[co.TOPO].mean([co.RL,co.ZM])
})

# %%
dsM = dsZ1.mean(co.RL)

# %%
dmm=dsM[co.CPer].mean([co.TH_CENTER,co.ZM])
dmmm = dmm.mean()
dsM1 = dsM.copy()
dsM1[co.CPer] = dsM[co.CPer]/(dmm+(.05*dmmm))

# %%
dmm1=dsM1[co.CPer].mean([co.TH_CENTER,co.ZM])
dmm1.plot()
# (30*dmm).plot(ylim=(0,1))

# %%
drop_coor_list = [co.LON,co.LAT,co.ZB,co.ZLM,co.ZT,co.VOL,co.GA]

# %%
dfM = dsM1.drop(drop_coor_list)[co.CPer].to_dataframe().reset_index()

# %%
r = dfM.iloc[100]
kml = simplekml.Kml()
sr =dfM[co.CPer]
max_col=sr[sr>0].quantile(.95)
low_thr=sr[sr>0].quantile(.4)

# %%
max_col,low_thr


# %%
def polygon_from_row(r,kml:simplekml.Kml, max_col,low_thr, full=False):
    col = 255*np.array(FLP.COLORS[int(r[co.ClusFlag])])
#     col = 255-col
    col = col.astype('int16')
    col = list(col)
    _z  = (r[co.ZM] ) + r[co.TOPO]
    points1 = [
        (r[co.LON_00], r[co.LAT_00],_z),
        (r[co.LON_10], r[co.LAT_10],_z),
        (r[co.LON_11], r[co.LAT_11],_z),
#         (r[co.LON_01], r[co.LAT_01],_z)
        (r[co.LON_00], r[co.LAT_00],_z),
    ]
    points2 = [
        (r[co.LON_00], r[co.LAT_00],_z),
#         (r[co.LON_10], r[co.LAT_10],_z),
        (r[co.LON_11], r[co.LAT_11],_z),
        (r[co.LON_01], r[co.LAT_01],_z),
        (r[co.LON_00], r[co.LAT_00],_z),
    ]    
    def make_pol(points):
        pol = kml.newpolygon(
            name = str(r.name),
            outerboundaryis = points,
            altitudemode = simplekml.AltitudeMode.absolute
        )

        alpha= (255/max_col) * r[co.CPer]
        alpha = min(int(alpha),255)
        if full:
            alpha=255


        pol.style.polystyle.color = simplekml.Color.rgb(*col,alpha)
        pol.style.polystyle.outline = 0
    if r[co.CPer]>low_thr:
        make_pol(points1)
        make_pol(points2)
    
   
    
    return col

# %%
kmlT = simplekml.Kml()
dfM = dsM1.drop(drop_coor_list)[co.CPer].to_dataframe().reset_index()
for ii in range(nc):
    _df = dfM[dfM[co.ClusFlag]==ii]
    kml = simplekml.Kml()
    sr =dfM[co.CPer]
    max_col=sr[sr>0].quantile(.95)
    res = _df.iloc[:].apply(lambda x: polygon_from_row(x,kml,max_col,low_thr),axis = 1)
#     res = _df.iloc[:].apply(lambda x: polygon_from_row(x,kmlT,max_col,low_thr),axis = 1)
    kml.save('/tmp/clus'+str(ii)+'.kml')
# kmlT.save('/tmp/clusT.kml')

kmlT = simplekml.Kml()
dfM = dsM1.drop(drop_coor_list)[co.CPer].to_dataframe().reset_index()
for ii in range(nc):
    _df = dfM[dfM[co.ClusFlag]==ii]
    kml = simplekml.Kml()
    sr =dfM[co.CPer]
    max_col=sr[sr>0].quantile(.95)
    res = _df.iloc[:].apply(lambda x: polygon_from_row(x,kml,max_col,low_thr,full=True),axis = 1)
#     res = _df.iloc[:].apply(lambda x: polygon_from_row(x,kmlT,max_col,low_thr),axis = 1)
    kml.save('/tmp/clusFull'+str(ii)+'.kml')
# kmlT.save('/tmp/clusT.kml')


# %%
dg=dsM1.groupby(co.ClusFlag)
dd = []
ll = []
for l,ds in dg:
    dd.append(ds.unstack().drop(co.ClusFlag))
    ll.append(l) 
dc = xr.concat(dd,pd.Index(ll,name=co.ClusFlag))

# %%

# %%
dsum = dc[co.CPer].sum([co.TH_CENTER,co.ZM])

# %%
dres = (dc[co.CPer].sum([co.TH_CENTER])*dc[co.ZM]).sum(co.ZM)/dsum

# %%
dr1 = dres.where(dsum>.5)
dr1.name = co.CPer
df1 = dr1.to_dataframe().unstack(co.ClusFlag)

# %%
cols = df1.columns.levels[-1].values

# %%
mks = ['o','1','v','8','s','p','P','*','h','+','x','D','X','o','1','v']
mks = [*mks,*mks]
for c in cols:
    ax = df1[co.CPer][c].plot(
            color = FLP.COLORS[c],
        marker=mks[c],
    #               legend=False,
                  logy=True,
                linewidth=2,
                  logx=True,
                  figsize=(10,8),
        label=c
                 )
ax.set_xlim(.05,50)
ax.legend()

# %%
ax.figure.savefig('/tmp/alt.pdf')

# %%
res = dsZ1[co.CPer].groupby(co.ClusFlag).sum()
res = 100*res /res.sum()
res = res.to_dataframe()

# %%
res.reset_index().plot.bar(x=co.ClusFlag,y=co.CPer,color = FLP.COLORS)

# %%
res.T[[1,9,11,14]].T.sum()

# %%
hour = dsZ1[co.RL].to_dataframe()
hour['hour'] = (hour.index + pd.Timedelta(-4,'hour')).hour
hour = hour['hour'].to_xarray()
dsZ1 = dsZ1.assign_coords(**{'hours':hour})

# %%

# %%
for i in range(nc):
    bo = (dsZ1[co.ClusFlag]==i)
    res = dsZ1[co.CPer].where(bo).sel(
        **{co.R_CENTER:slice(0,.5),co.ZM:slice(0,100000)}
    ).sum([co.TH_CENTER,co.R_CENTER,co.ZM]).groupby('hours').median()
    ax = res.plot(color=FLP.COLORS[i],linewidth=4,marker=mks[i])
    ax = ax[0]
    ax = ax.axes
ax.set_yscale('log')


# %%

# %%

# %%
path_bc = '/Users/diego/JUP/co_bc/data/horiba_chc_corrected_diego.csv'

# %%
bc,CO,h  = 'abs670','CO_ppbv','hour'
lh = 'Local Time'
dt = 'date'
df = pd.read_csv(path_bc)
df[lh]=np.mod(df[h]-4,24)

# %%
df[dt] = pd.to_datetime(df[dt])
df = df.set_index(dt)

# %%
desc = df.groupby(lh)[bc].describe()

# %%
desc['50%'].plot()

# %%

# %%
dd = df[bc]['2017-12':'2018-05']

dd.plot(
    marker=',',linewidth=0,
    figsize=(10,5)
)
std=24
res = dd.rolling(std,min_periods=int(std/4),center=True).median()
ax=res.plot()
# ax.set_ylim(.1,12)
# ax.set_yscale('log')

# %%
axs = df2.plot.area(
    subplots=False,
    layout=(int(np.ceil(nc/3)), 3),color = FLP.COLORS,
    ylim = (0,100),grid=True,figsize=(20,10),linewidth=0,
    legend=False
              )

dd = df[bc]['2017-12':'2018-05']*10

dd.plot(
    marker=',',linewidth=0,
    figsize=(10,5),
    color='k'
)
std=24
resI = res = dd.rolling(std,min_periods=int(std/4),center=True,win_type='gaussian').mean(std=.5*std)
ax=res.plot(figsize=(20,10),color='k',linewidth=2)
# ax.set_ylim(.1,8)
# ax.set_yscale('log')
std=24*30
res = dd.rolling(std,min_periods=int(std/4),center=True,win_type='gaussian').mean(std=.5*std)
ax=res.plot(figsize=(20,10),color='k',linewidth=2)
# ax.set_ylim(.1,8)

# %%
df2.head()

# %%
cols = df2.columns

# %%
resI.index.name = co.RL
res2 = pd.merge(resI,df2,left_index=True,right_index=True)
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
ax = AA[[bcl,cc]].resample('H').mean().plot()
ax.figure.tight_layout()
ax.set_xlabel('')
ax.figure.savefig('/tmp/abs_mea_cal.pdf')

# %%

# %%

# %%
r1 = pd.Series(res[0],index=cols)
r1 = r1/r1.sum()

# %%

# %%

ax = r1.plot.bar(color = FLP.COLORS)
ax.set_xlabel('cluster region')
ax.set_ylabel('weights [%]')
ax.figure.savefig('/tmp/meas_bar_abs.pdf')

# %%
r0 =res[0]
AA = res2.copy()
c=np.dot(A,np.array(r0))
lab = 'reconstructed Sulfate signal'
AA[lab]=c
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
l1 = 'Sulfate ACSM [ug/m3]'
AA[l1]=AA[c1]
# AA=AA.rename(mapper=str,columns={c1:l1})
ax = AA[[l1]].resample('H').mean().plot()
ax.figure.tight_layout()
ax.figure.savefig('/tmp/abs_mea_cal1.pdf')

# %%
r1.index.name=co.ClusFlag

# %%
path = '/Volumes/mbProD/Downloads/CHC_QACSM.xlsx'

# %%
acsm = pd.read_excel(path)
acsm = acsm.set_index('Date UTC')
acsm = acsm[1:]
acsm = acsm['2018-04-01':]
acsm = acsm.resample('1H').median()
acsm = acsm.rolling(
    12,min_periods=1,center=True,win_type='gaussian'
).mean(std=4)

# acsm = acsm.rolling(
#     24,min_periods=1,center=True
# ).median()




# %%

# %%
acsm.index.name = co.RL

# %%
resI.index.name = co.RL
res2 = pd.merge(acsm,df2,left_index=True,right_index=True)
res2=res2.dropna()

# %%
acsm.columns

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
r1 = r1/r1.sum()
ax = r1.plot.bar(color = FLP.COLORS)
ax.set_xlabel('cluster region')
ax.set_ylabel('weights [%]')

ax.figure.savefig('/tmp/sulf_weights.pdf')


# %%
r0 =res[0]
AA = res2.copy()
c=np.dot(A,np.array(r0))
lab = 'reconstructed Sulfate signal'
AA[lab]=c
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
l1 = 'Sulfate ACSM [ug/m3]'
AA[l1]=AA[c1]
# AA=AA.rename(mapper=str,columns={c1:l1})
ax = AA[[l1]].resample('H').mean().plot()
ax.figure.tight_layout()
ax.figure.savefig('/tmp/abs_mea_cal1.pdf')

# %%

# %%
res2[c1].plot()

# %%

# %%

# %%

# %%
