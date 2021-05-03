# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.7.0-rc1
#   kernelspec:
#     display_name: Python [conda env:b36]
#     language: python
#     name: conda-env-b36-py
# ---

# %% [markdown]
# ## imports

# %%
from useful_scit.imps import *

# %%
LT = "local time"

# %%

def merge_df_ds(da2, ds_cl, lev='LEV0',con='18'):
    d1 = ds_cl.loc[{'normalized': 0}]
    d1 = d1['conc_lab_nc'+con].loc[{'z_column': lev}].reset_coords(
        drop=True).to_dataset('lab_nc'+con)
    dd1 = d1.to_dataframe()
    dm = pd.merge(dd1, da2, left_index=True, right_index=True)
    
    # add night flag
    dm['night']=dm.index.hour.isin([19,20,21,22,23,24,0,1,2,3,4,5,6,7,8]).astype(int)
    return dm

def open_ds(cluster_path):
    ds_cl = xr.open_dataset(cluster_path)
    ds_cl[LT] = ds_cl['releases'] - pd.Timedelta(hours=3.5)
    ds_cl = ds_cl.swap_dims({'releases': LT})
    return ds_cl


def open_df(c45_path):
    df_45 = pd.read_excel(c45_path)

    df_45[LT] = pd.to_datetime(df_45['Time_LT'], format='%d/%m/%Y %H:%M:%S')

    da1 = df_45.set_index(LT).drop('Time_LT', axis=1)

    da2 = da1.resample('h').mean()
    da2.index += pd.Timedelta(hours=.5)
    return da2


# %% [markdown]
# ### open dataset
# %%
cluster_path = '/Users/diego/flexpart_management/flexpart_management/releases/v03/data/cluster_series_v3.nc'
c45_path = '/Users/diego/flexpart_management/flexpart_management/notebooks/george_paper/c45_timeseries.xlsx'
# %%
# %%
da2 = open_df(c45_path)
ds_cl = open_ds(cluster_path)
dm = merge_df_ds(da2, ds_cl)
d = ds_cl.loc[{'normalized': 0}]
# %%

# %% [markdown]
# ### plot histogram
# %%
ds_cl['conc_lab_nc18'].loc[{'normalized':0}]

# %%
da2.hist();
plt.gcf().tight_layout()
# %% [markdown]
# ### plot correlations
# %%
dm

# %%
_ = dm.corr(method='spearman')['C45_Total_ratio']
_.plot.barh(figsize=(10, 10))
plt.gca().grid()
# %%
_ = dm.corr(method='pearson')['C45_Total_ratio']
_.plot.barh(figsize=(10, 10))
plt.gca().grid()
# %%
dm.hist(figsize=(10, 10))
plt.gcf().tight_layout()
# %%
# %% [markdown]
# ### sklearn
# %%
import sklearn.preprocessing
# %%
qt = sklearn.preprocessing.RobustScaler(quantile_range=(10.0, 90.0))
# %%
dm1 = dm.dropna().copy()
dmm = dm1.copy()
dm1 = dm1 * 0 + qt.fit_transform(dm1)
# %%
dm1.hist(figsize=(10, 10))
plt.gcf().tight_layout()
# %%
import sklearn.cluster
# %%
nc = 8
km = sklearn.cluster.KMeans(n_clusters=nc)
# %%
dm2 = dm1.copy()
dm2['C45_Total_ratio'] *= 5
dm2['night'] *= 5
km.fit(dm2)
dm2['C45_Total_ratio'] /= 5
dm2['night'] /= 5
# %%
valas = pd.DataFrame(km.cluster_centers_, columns=dm2.columns).sort_values(
    ['C45_Total_ratio']).index
# %%
kk = {k: a for k, a in zip(valas, 'abcdefghijklmnopqrstuv')};
# %%
dmm['k'] = [kk[x] for x in km.labels_]
# %%
g = sns.catplot(x='k', y='value', data=dmm.melt(id_vars='k'), orient="v",
                kind="strip",
                col='variable', col_wrap=4, sharex=False, palette='Set2',
                sharey=False, aspect=2, height=2,
                order='abcdefghijklmnopqrstuv'[:nc],
                alpha=.1,
                #                size=1

                )

# g.set_xticklabels(rotation=90)
# plt.gcf().set_dpi(50)
plt.gcf().tight_layout()
# %% [markdown]
# ### Compare time series
# %%

# %%

# %%
dmm.iloc[:,:18]/dmm.iloc[:,:18].mean()


# %%
def plt_bp(dmm):
    ccn = pd.Series(list(dmm.columns[:18]))
    
    ccn = ccn[ccn.str.endswith('_SR')]
    
    print(ccn)

    nd = dmm[ccn].mean()
#     nd['T'] = 'mean'
    pp = []
    
   
    for c in ['e','g']:
        nd1 = dmm[dmm['k']==c][ccn]
        nd1['T'] = c
        pp.append(nd1)

    pc = pd.concat([*pp])
    
    pc[ccn] = pc[ccn]/nd
    

    # pc[ccn] = np.log(pc[ccn])

    _,ax = plt.subplots(figsize=(20,5),dpi=70)
    sns.boxplot(
        data=pc.melt(id_vars='T'),
        x='variable',
        y='value',
        hue='T'
    )
    ax.set_ylim(.01,3)
#     ax.set_yscale('log')

# %%
plt_bp(dmm)

# %%
dmm.iloc[:,:18].boxplot(color='r')

# %%

# %%
dmm.iloc[:,:18].mean().plot.bar(color='r',alpha=.5)
dmm[dmm['k']=='r'].iloc[:,:18].mean().plot.bar(color='b',alpha=.5)

# %%
ds_cl.loc[{'normalized':0}].loc[{LT: '2018-01'}]['age_all'].plot(hue='z_column', figsize=(10, 5),
                                       alpha=.5)
ax = plt.gca()
axt = ax.twinx()
da2['C45_Total_ratio'].plot(ax=axt, alpha=.5, color='red')
ax.figure.set_dpi(300)
# %%
da2['C45_Total_ratio'].resample('6H').mean().plot(alpha=.5, color='red')
ax = plt.gca()
axt = ax.twinx()
d.loc[{LT: '2018-01'}]['age_all'].resample({LT: '6H'}).mean().plot(
    hue='z_column', alpha=.5, ax=axt)
# ax.figure.set_dpi(300)
# %%
ds_cl['conc_all'].loc[{'normalized': 0}].plot(hue='z_column',
                                              figsize=(10, 5), alpha=.5)
# %%
for c in ds_cl['z_column']:
    ds_cl['age_all'].loc[{'z_column': c}].plot.hist(alpha=.4, label=c)
plt.gca().legend()
plt.gcf().set_size_inches(10, 5)
plt.gcf().set_dpi(100)
# %%
plt.Figure.set_si
# %%
s = pd.Series(dm.columns)
# %%
sr = s[s.str.endswith('_SR')]
sm = s[s.str.endswith('_SM')]
mr = s[s.str.endswith('_MR')]
lr = s[s.str.endswith('_LR')]
# %%
dm['SR_'] = dm[sr].sum(axis=1)
dm['SM_'] = dm[sm].sum(axis=1)
dm['MR_'] = dm[mr].sum(axis=1)
dm['LR_'] = dm[lr].sum(axis=1)
dm['SS_'] = dm['SR_'] + dm['SM_']
# %%
dm.plot.scatter(x='SR_', y='C45_Total_ratio')
# %%
dm.plot.scatter(x='SM_', y='C45_Total_ratio')
# %%
dm.plot.scatter(x='MR_', y='C45_Total_ratio')
# %%
dm.plot.scatter(x='LR_', y='C45_Total_ratio')
# %%
dm.plot.scatter(x='SS_', y='C45_Total_ratio')




# %% [markdown]
# ## create a BL flag

# %%

# %%
def ppl(m=True):
    if m:
        dmA = merge_df_ds(da2, ds_cl,lev='ALL')
        dmB = merge_df_ds(da2, ds_cl,lev='BL')
        dm = dmA
        dm[dm.columns[:18]] = dmA[dm.columns[:18]]-dmB[dm.columns[:18]]
    else:
        dm = merge_df_ds(da2, ds_cl,lev='BL')

    dm = dm[dm['night']==1]
    dm = dm.resample('h').mean()
    dm.index += pd.Timedelta(hours=.5)

    sr_ = dm.columns[dm.columns.str.endswith('_SR')]
    sr_lev0 = dm[sr_].sum(axis=1)
    dm['SR'] = sr_lev0

    sr_ = dm.columns[dm.columns.str.endswith('_SM')]
    sm_lev0 = dm[sr_].sum(axis=1)
    dm['SM'] = sm_lev0

    mr_ = dm.columns[dm.columns.str.endswith('_MR')]
    mr_lev0 = dm[mr_].sum(axis=1)
    dm['MR'] = mr_lev0

    mr_ = dm.columns[dm.columns.str.endswith('_LR')]
    lr_lev0 = dm[mr_].sum(axis=1)
    dm['LR'] = lr_lev0




    ddd= dm[dm['night']==1]

#     plt.subplots(figsize=(20,20),dpi=200)
    dc = ddd.corr().sort_values('C45_Total_ratio')
    dc = dc.T.sort_values('C45_Total_ratio')
#     sns.heatmap(dc,cmap = plt.get_cmap('RdBu_r',15),center=0,vmin=-.7,vmax=.7,linewidths=1,square=True,
#                 annot=True,fmt="0.1f"
#                )
    return dm,dc

# %%
# %matplotlib inline
ddd,dc = ppl()

# %%
f,ax=plt.subplots(figsize=(20,5),dpi=200)
ddd[['SR','SM','MR','LR']].plot(ax=ax)
# ax = plt.gca()
axt = ax.twinx()
ax3 = ax.twinx()
ddd['C45_Total_ratio'].plot(ax=axt,c='purple', label='c45')
axt.tick_params(pad=30,color='purple',labelcolor='purple')
ddd['water mixing ratio'].plot(ax=ax3,c='k', label='wmr')
ax3.tick_params(color='k',labelcolor='k')
ax.legend()
axt.legend(loc='lower left')
ax3.legend()

# %%
dc.loc[['C45_Total_ratio','water mixing ratio','BC']]

# %%
cc=['C45_Total_ratio','water mixing ratio','BC']

# %%
_,dm = ppl(m=True)
_,dm1 = ppl(m=False)


# %%
def hm(dm,ax,title):
    sns.heatmap(dm.loc[cc],
                cmap = plt.get_cmap('RdBu_r',15),center=0,vmin=-.7,vmax=.7,linewidths=1,square=True,
                annot=True,fmt="0.1f",
                cbar = False,
                ax=ax
               )
    ax.set_title(title)


# %%
ccc=dm.columns

# %%
f,axs = plt.subplots(2,1,figsize=(20,6),dpi=200,sharex=True)
hm(dm[ccc],axs[0],'above BL')
hm(dm1[ccc],axs[1],'BL')

# %% [markdown]
# ## create a proxi fro feer troposphere

# %%
dm = merge_df_ds(da2, ds_cl,lev='BL')
dm6 = merge_df_ds(da2, ds_cl,lev='BL',con='06')
nn = 6

# %%
d1 = dm.where(dm['night']==1)

# %%
d1['day'] = pd.to_datetime(d1.index.date) - pd.Timedelta(hours=12)

# %%
d2 = d1.groupby('day').mean()
d2.index += pd.Timedelta(hours=12)

# %%
leg = d2.iloc[:,:18].sum().sort_values(ascending=False).index

# %%
d2[leg].plot()
plt.legend(loc='center left',bbox_to_anchor=(1.05, 0.5))

# %%
aa=leg[leg.str.endswith('_SR')]

# %%
aa

# %%
# %matplotlib osx
f,ax=plt.subplots(figsize=(25,6))
(-dm[aa]).plot(ax=ax)
(-dm[aa]).sum(axis=1).plot(legend='SR')

axt = plt.gca().twinx()
dm['C45_Total_ratio'].plot(ax=axt,linestyle='-.',color='r')

axt = plt.gca().twinx()
dm['water mixing ratio'].plot(ax=axt,linestyle='--')
plt.legend(loc='center left',bbox_to_anchor=(1.05, 0.5))
plt.tight_layout()
plt.gca().grid()

# %%
dm6.plot(ax=ax)

# %%

# %%
dm

# %% [markdown]
# ## 5 FLAGS

# %% [markdown]
# - D05
# - D15 
# - D25 
# - WMR
# - C45 
# - DIR6
# - NIGHT
# - RH

# %%
dm = merge_df_ds(da2, ds_cl,lev='BL')
dm6 = merge_df_ds(da2, ds_cl,lev='ALL',con='06')

# dm = dm[dm['night']==1]
# dm6 = dm6[dm6['night']==1]

# %%
# %matplotlib inline
dm6['03_PW'].plot()

# %%
SR_c = dm.iloc[:,:18].columns[dm.iloc[:,:18].columns.str.endswith('_SR')]
D05 = dm[SR_c].sum(axis=1)

SR_c = dm.iloc[:,:18].columns[dm.iloc[:,:18].columns.str.endswith('_SM')]
D15 = dm[SR_c].sum(axis=1) + D05

SR_c = dm.iloc[:,:18].columns[dm.iloc[:,:18].columns.str.endswith('_MR')]
D25 = dm[SR_c].sum(axis=1) + D15



# %%
D05.plot()
D15.plot()
D25.plot()

# %%
dm.columns

# %%
WMR = dm['water mixing ratio']
C45 = dm['C45_Total_ratio']
Dp50 = dm['Dp50']
Dp100 = dm['Dp100']
RH = dm['RH_station']
DIR6 = dm6.iloc[:,:6]
CO = dm['CO_ppb']
BC = dm['BC']


# %%
DIR6.plot()


# %%
f,ax = plt.subplots(figsize=(20,5))
RH.plot()
axt = ax.twinx()
WMR.plot(ax=axt,c='r')

# %%
cdf = DIR6

# %%
cdf['D05'] = D05
cdf['D15'] = D15
cdf['D25'] = D25
cdf['L_Dp50'] = np.log(Dp50)
cdf['L_Dp100'] = np.log(Dp100)
cdf['RH'] = RH

# %%
cdf['WMR'] = WMR
cdf['C45'] = C45
cdf['L_BC'] = np.log(BC)
cdf['L_CO'] = np.log(CO )

# %%
cdf = cdf[cdf.columns[::-1]]

# %%

# %%

# %%
import sklearn.preprocessing
# %%
qt = sklearn.preprocessing.RobustScaler(quantile_range=(10.0, 90.0))
# %%
dm1 = cdf.dropna().copy()
dmm = dm1.copy()
dm1 = dm1 * 0 + qt.fit_transform(dm1)
# %%
dm1.hist(figsize=(10, 10))
plt.gcf().tight_layout()
# %%
import sklearn.cluster
# %%
nc = 7
km = sklearn.cluster.KMeans(n_clusters=nc)
# %%
dm2 = dm1.copy()
dm2['C45'] *= 3
dm2['RH'] *= 2
dm2['D05'] *= 3
dm2['L_CO'] = 0
dm2['L_BC'] = 0 
# dm2['WMR'] *= 2
# dm2['night'] *= 5
km.fit(dm2)
# dm2['C45_Total_ratio'] /= 5
dm2['D05'] /= 3
dm2['C45'] /= 3
dm2['RH'] /= 2
# %%
valas = pd.DataFrame(km.cluster_centers_, columns=dm2.columns).sort_values(
    ['D05']).index
# %%
abc= 'abcdefghijklmnopqrstuv'
kk = {k: a for k, a in zip(valas, abc)};
rc = pd.Series(['D05','C45','WMR',*dm2.columns]).drop_duplicates()
# %%
dmm['k'] = [kk[x] for x in km.labels_]
# %%
sns.set_palette('Set2')

# %%
# %matplotlib inline
g = sns.catplot(x='k', y='value', data=dmm.melt(id_vars='k'), orient="v",
                kind="box",
                col='variable', col_wrap=4, sharex=False, 
#                 palette='Set2',
                sharey=False, aspect=2, height=2,
                order='abcdefghijklmnopqrstuv'[:nc],
                col_order=rc
#                 alpha=.1,
                #                size=1

                )

# g.set_xticklabels(rotation=90)
# plt.gcf().set_dpi(50)
plt.gcf().tight_layout()

for a in g.axes[-6:]:
    a.set_ylim(0,300000)
    
# %%
# %matplotlib inline
(dmm['k'].value_counts()/dmm['k'].value_counts().sum()*100).sort_index().plot.bar()

# %%
sns.color_palette()

# %%
# %matplotlib inline
(dmm['k'].value_counts()).sort_index().plot.bar(color = sns.color_palette())

plt.gca().set_ylabel('n. cases (hours)')

# %%
dmm2 = dmm.resample('H').first()

# %%
# %matplotlib inline
f,ax = plt.subplots(figsize=(20,4))
for i in abc[:nc]:
    dmm2.where(dmm2['k']==i)['C45'].plot(label=i,marker='.')
#     dmm2.where(dmm2['k']==i)['C45'].plot(linewidth=0,,label=i)
    
plt.gca().legend()


# %%
dmm2.to_csv('cluster_george_c45.csv')

# %%

# %%
