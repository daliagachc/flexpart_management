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

# %%
from useful_scit.imps2.defs import *
from scipy.signal import find_peaks as fp

# %%
ds = xr.open_dataset('/Users/diego/flexpart_management/flexpart_management/releases/v03/data/cluster_series_v3.nc')

# %%
df = ds['conc_lab_nc18'].loc[{'normalized':1,'z_column':'ALL'}].reset_coords(drop=True).\
to_dataframe()['conc_lab_nc18'].\
unstack(0)

# %%
df.columns

# %%
    
dic = {}
for cl in df.columns:
    dat = df[cl]
    v = 24
    d2 = dat.rolling(v*4, win_type='gaussian',center=True, min_periods=1).mean(std=int(round(v*.5)))
    mm = d2.mean()

    peaks, properties = fp(
        d2,
        #distance=24,
        #prominence=mm/2,            
        width=24,
        height=mm
             )

    w_med = np.median(properties['widths']/24)
    h_med = np.median(properties['peak_heights'])
    l = len(properties['widths'])
    dic[cl] = dict(
        w_med = w_med,
        h_med = h_med,
        l = l
    )


# %%
ddf = pd.DataFrame(dic).T

# %%

# %%
f,ax = plt.subplots()
for l,r in ddf.iterrows():
    def _rc(l): return np.random.choice(l)
#     ax.text(r['w_med'],r['h_med'],l,fontsize=5,alpha=.5)
    ax.text(r['w_med'],r['l'],l,fontsize=5,alpha=.5,
            ha=_rc(['left','right']),
            va=_rc(['top','bottom'])
           )
    ax.scatter(r['w_med'],r['l'],alpha=.5,marker='x',c='k',s=2)
    
    

# %%
mm

# %%
d2.quantile(.02)*.1

# %%
cl = '12_SR'
dat = -df[cl]
v = 24
d2 = dat.rolling(24, 
#                  win_type='gaussian',
                 center=True, 
                 min_periods=1).mean(
    std=int(12)
           )

# d2 = dat 
mm = d2.quantile(.02)*.1

peaks, properties = fp(
        d2,
        #distance=24,
        prominence=abs(1*mm),
#     threshold=abs(.2*mm),
        width=6,
        height=mm,
#         plateau_size = 2
             )

plt.rcParams["figure.dpi"] = 150

f,ax = plt.subplots(figsize=(20,2))
(-dat).plot(ax=ax)
(-d2).plot(ax=ax)
(-d2)[peaks].plot(ax=ax,linewidth=0,marker='x',c='k')
ax.axhline(-mm)

# ax.vlines(x=d2[peaks].index, ymin=d2[peaks] - properties["prominences"],
#            ymax = d2[peaks], color = "C1")
# ax.hlines(y=properties["width_heights"], 
#           xmin=left,
#            xmax=right, color = "C1")

# %%
np.median(properties['widths']/24)

# %%
plt.hist(properties['widths']/24)

# %%
plt.hist(properties['widths']/24)

# %%
a = 2
rr = {}
alist = []
dfc = df.copy()
df_residuals = df * 0 
rols = []
for i in range(6):
    dfc = dfc - df_residuals
    a = int(a + a)
    alist.append(a)
    rol = dfc.rolling(window = a, min_periods=1,center=True)
    rm = rol.mean()
    rols.append(rm)
    df_residuals = dfc - rm
    res = (df_residuals/df.mean()).std()
    rr[a] = res.to_dict()

# %%
ss = '07_SR'
# ss = '11_MR'
df[ss].plot(figsize=(20,2))
dfc[ss].plot()
rm[ss].plot()
dfcc[ss].plot()

# %%
std_o = df[ss].std()
std_o

# %%
aa = []
a = 3
for i in range(10): 
    a *=2
    aa.append(a)
    
aa = aa[::-1]


# %%
aa

# %%
dfc = df.copy()
stds = []
for a in aa:
#     dfc.plot()
    dfc = dfc - dfc.rolling(window = a, min_periods=1,center=True).mean()
    std = dfc.std()
    stds.append(std)   


# %%
stds

# %%
sig   = pd.Series(np.sin(np.arange(0,1000)/10))
plt.plot(sig)

# %%
(sig.rolling(window=500,center=True,min_periods=1,win_type='gaussian').mean(std=100)).plot()
sig.plot()

# %%
df[ss].plot()

# %%

# %%

rols[0][ss].plot()
rols[1][ss].plot()
rols[10][ss].plot()
rols[-1][ss].plot()

# %%
dd = pd.DataFrame(rr)

# %%
col_order = dd.iloc[:,0].sort_values()[::-1].index

# %%

# %%
xa = dd.loc[col_order].stack().to_xarray()

# %%
xp = xa.plot(
    col='level_0',col_wrap=6,linewidth=1,marker='x',
    hue='level_0',xscale='log')

# %%
for ax in xp.axes.flatten():


# %%
def b(m,k,w):
    return ( 
        ( np.sin( np.pi * m * w ) )/ ( m * np.sin( np.pi * w ) )
    )**(2*k)

def w0(m,k):
    cc = ( 0.5 **(0.5*k) )
    
    a = np.sqrt(6)
    b = np.pi
    c = 1 - cc
    d = m**2 - cc
    r = ( a / b ) * np.sqrt( c / d) 
    return r 


# %%
1/w0(15,5)

# %%
1003*np.sqrt(5)/24

# %%
ra = np.arange(0,100)

# %%
plt.plot(ra,b(3,2,ra)**2)
plt.gca()


# %%
def kf(ts, m, k):
    ts1 = ts.copy()
    for kk in range(k):
        ts1 = ts1.rolling(
            m,
            center=True, 
#             min_periods=int(m * 2/3)
            min_periods=1
        ).mean()
    return ts1


# %%
do = df['09_MR'].copy()
do = df.copy()
# do = np.log10(do+.00001)

# %%
id, du,sy,bl = ll =  0,3*np.sqrt(3)/24,13*np.sqrt(5)/24,103*np.sqrt(5)/24
ll

# %%
nam = ['0h - 12h','12h - 1.2d','1.2d - 10d','>10d']
nam = ['ID','DU','SY','BL']

# %%
ID = do - kf(do,3,3)
DU = kf(do,3,3) - kf(do,13,5)
SY = kf(do,13,5) - kf(do,103,5)
BL = kf(do,103,5) 
# M = kf(do,403,5)


# %%
ov = do.var()

# %%
ndf = pd.DataFrame()

# %%
ndf[nam[0]]=(ID.var()/ov)

# %%
ndf[nam[1]]=(DU.var()/ov)

# %%
ndf[nam[2]]=(SY.var()/ov)

# %%
ndf[nam[3]]=BL.var()/ov
ndf = ndf[ndf.columns[::-1]]

# %%
# ndf[nam[4]]=M.var()/ov

# %%

# %%



# %%
# ndf=ndf.sort_values('12h - 1.2d')[::-1]
ndf=ndf.sort_values('DU')[::-1]

# %%
ndf1 = pd.melt(ndf,ignore_index=False).reset_index()

# %%
ndf1

# %%

# %%
med=ndf.median(axis=0)
med

# %%
grid = sns.FacetGrid(ndf1, col="lab_nc18", 
#                      hue="lab_nc18", palette="tab20c",
                     col_wrap=6, height=1.5,col_order=ndf.index,aspect=1)
def _pp(xx,yy,**kw): return plt.plot(xx,yy,**kw)
grid.map(_pp, yy=med.index,xx=med, ls=":",marker='o',color='.8')
grid.map(plt.plot, "value",  "variable",marker="o",color='k')
# grid.grid()
grid.set_titles('{col_name}')
# sns.despine(fig=grid.fig,left=True)
grid.fig.savefig('KF_filter.pdf')

# %% [markdown]
# A time-series of hourly species (S) data can be presented by:
# $$S(t) = ID(t) + DU(t) + SY(t) + BL(t)$$
# Kolmogorov Zurbenko filter. Applied as described here:
# https://www.sciencedirect.com/science/article/pii/S1352231013003002#appsec1

# %%
np.var(ID['02_MR'])

# %%
la='12_SR'

# %%
do[la].var()

# %%
res= np.cov([ID[la],DU[la],SY[la],BL[la]])/do[la].var()

# %%
sns.heatmap(res,cmap='Reds')

# %%
res.sum()

# %%
pd.concat([ID[['02_MR']],DU[['02_MR']]],axis=1).cov()

# %%
# Create a dataset with many short random walks
rs = np.random.RandomState(4)
pos = rs.randint(-1, 2, (20, 5)).cumsum(axis=1)
pos -= pos[:, 0, np.newaxis]
step = np.tile(range(5), 20)
walk = np.repeat(range(20), 5)
df = pd.DataFrame(np.c_[pos.flat, step, walk],
                  columns=["position", "step", "walk"])

df

# %%
# (ID + DU + SY + BL + M  ).plot(figsize=(40,5))
# ID.plot()
# DU.plot()
# SY.plot()
# BL.plot()
# M.plot()

# %%
M['12_SR'].plot()

# %%
