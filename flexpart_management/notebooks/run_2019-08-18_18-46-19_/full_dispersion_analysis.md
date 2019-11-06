```python
%load_ext autoreload
%autoreload 2
```


```python
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FLP
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
```

    reload



```python
path = '/Volumes/mbProD/Downloads/flx_log_coor/run_2019-08-18_18-46-19_'
# flp = FLP.FlexLogPol(path,concat=True)
# self = FLP.FlexLogPol(path,concat=False)
self = FLP.FlexLogPol(
    path,
    #concat=True,
    concat=False,
    get_clusters=False,
    open_merged=True,
    clusters_avail=False
)
```

    'using vol for conc'



```python

```


```python
self.reset_z_levels()
```

    'using vol for conc'



```python
dsF= self.filter_hours_with_few_mea()
```


```python
dsSM = ds1 = FLP.smooth_merged_ds(
    dsF
    )
```

    (3888, 6, 35, 36)
    (3888, 6, 35, 36)
    (3888, 6, 35, 36)
    (3888, 6, 35, 36)



```python
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
```




    (-25, -7)




![png](full_dispersion_analysis_files/full_dispersion_analysis_7_1.png)



```python
ax.figure.savefig('/tmp/map.pdf')
```


```python

```


```python
ds1.sum([co.ZM,co.RL,co.TH_CENTER])[co.CPer].plot(marker='.',xscale='log')
```




    [<matplotlib.lines.Line2D at 0x1243b3eb8>]




![png](full_dispersion_analysis_files/full_dispersion_analysis_10_1.png)



```python
lines = ds1.sum([co.RL,co.TH_CENTER])[co.CPer].plot(marker='.',xscale='log',hue=co.ZM)
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_11_0.png)



```python
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
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_12_0.png)



```python
ax.figure.savefig('/tmp/gen_fig.pdf')
```

# new part


```python
dsZ = dsSM
```


```python
dfcc = self.get_vector_df_for_clustering(self.coarsen_par,ar=dsZ[co.CONC])
```


```python
nc = 21
```


```python
dfres = self.python_cluster(
    random_state=222,
    n_cluster=nc,
    df=dfcc,
    return_df=True,
    
)
```


```python
dsZ[co.ClusFlag]=dfres[co.ClusFlag].to_xarray()
```


```python
dg = dsZ.assign_coords(**{co.ClusFlag:dsZ[co.ClusFlag],co.TOPO:dsZ[co.TOPO]})
dg = dg.groupby(co.ClusFlag)
dg = dg.sum('stacked_R_CENTER_TH_CENTER_ZMID')
```


```python
df = dg.to_dataframe()
```


```python
df1 = df[co.CPer]
```


```python
df2 = df1.unstack(co.ClusFlag)
```


```python
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')
```


```python
FLP.COLORS = [*FLP.COLORS,*FLP.COLORS]
```


```python
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
```

    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/pandas/plotting/_tools.py:203: UserWarning: When passing multiple axes, layout keyword is ignored
      "ignored", UserWarning)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/pandas/plotting/_core.py:1801: UserWarning: When passing multiple axes, sharex and sharey are ignored. These settings must be specified when creating axes
      plot_obj.generate()



![png](full_dispersion_analysis_files/full_dispersion_analysis_26_1.png)



```python
axs[0].figure.savefig('/tmp/inf.pdf')
```


```python
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
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_28_0.png)



```python
axs.figure.savefig('/tmp/inf_area.pdf')
```


```python
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
```


```python
ax.figure.savefig('/tmp/clus_res.pdf')
```


```python
ii=5
ds_fl = dsZ[co.CPer].where(dsZ[co.ClusFlag]==ii)
```


```python
ax = fa.get_ax_bolivia()
cmap = fa.get_custom_cmap(self.colors[ii])
fa.logpolar_plot(ds_fl.sum([co.RL,co.ZM]),
                 name=co.CPer,ax=ax,
                 patch_args={'cmap':cmap}
                )
ax.set_xlim(-75,-60)
yl=ax.set_ylim(-25,-7)
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_33_0.png)



```python
import simplekml
```


```python
import simplekml
kml = simplekml.Kml()
```


```python
dsZ1 = dsZ.assign_coords(**{
    co.ClusFlag:dsZ[co.ClusFlag],
    co.TOPO:dsZ[co.TOPO].mean([co.RL,co.ZM])
})
```


```python
dsM = dsZ1.mean(co.RL)
```

    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:159: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)



```python
dmm=dsM[co.CPer].mean([co.TH_CENTER,co.ZM])
dmmm = dmm.mean()
dsM1 = dsM.copy()
dsM1[co.CPer] = dsM[co.CPer]/(dmm+(.05*dmmm))
```


```python
dmm1=dsM1[co.CPer].mean([co.TH_CENTER,co.ZM])
dmm1.plot()
# (30*dmm).plot(ylim=(0,1))
```




    [<matplotlib.lines.Line2D at 0x129a576a0>]




![png](full_dispersion_analysis_files/full_dispersion_analysis_39_1.png)



```python
drop_coor_list = [co.LON,co.LAT,co.ZB,co.ZLM,co.ZT,co.VOL,co.GA]
```


```python
dfM = dsM1.drop(drop_coor_list)[co.CPer].to_dataframe().reset_index()
```


```python
r = dfM.iloc[100]
kml = simplekml.Kml()
sr =dfM[co.CPer]
max_col=sr[sr>0].quantile(.95)
low_thr=sr[sr>0].quantile(.4)
```


```python
max_col,low_thr
```




    (2.6622503635307733, 0.4390980961594004)




```python
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
```


```python
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
```


```python
dg=dsM1.groupby(co.ClusFlag)
dd = []
ll = []
for l,ds in dg:
    dd.append(ds.unstack().drop(co.ClusFlag))
    ll.append(l) 
dc = xr.concat(dd,pd.Index(ll,name=co.ClusFlag))
```


```python

```


```python
dsum = dc[co.CPer].sum([co.TH_CENTER,co.ZM])
```


```python
dres = (dc[co.CPer].sum([co.TH_CENTER])*dc[co.ZM]).sum(co.ZM)/dsum
```


```python
dr1 = dres.where(dsum>.5)
dr1.name = co.CPer
df1 = dr1.to_dataframe().unstack(co.ClusFlag)
```


```python
cols = df1.columns.levels[-1].values
```


```python
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
```




    <matplotlib.legend.Legend at 0x1397c2a20>




![png](full_dispersion_analysis_files/full_dispersion_analysis_52_1.png)



```python
ax.figure.savefig('/tmp/alt.pdf')
```


```python
res = dsZ1[co.CPer].groupby(co.ClusFlag).sum()
res = 100*res /res.sum()
res = res.to_dataframe()
```

    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/groupby.py:639: FutureWarning: Default reduction dimension will be changed to the grouped dimension in a future version of xarray. To silence this warning, pass dim=xarray.ALL_DIMS explicitly.
      skipna=skipna, allow_lazy=True, **kwargs)



```python
res.reset_index().plot.bar(x=co.ClusFlag,y=co.CPer,color = FLP.COLORS)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x119384710>




![png](full_dispersion_analysis_files/full_dispersion_analysis_55_1.png)



```python
res.T[[1,9,11,14]].T.sum()
```




    CONC_per    43.558643
    dtype: float32




```python
hour = dsZ1[co.RL].to_dataframe()
hour['hour'] = (hour.index + pd.Timedelta(-4,'hour')).hour
hour = hour['hour'].to_xarray()
dsZ1 = dsZ1.assign_coords(**{'hours':hour})
```


```python

```


```python
for i in range(nc):
    bo = (dsZ1[co.ClusFlag]==i)
    res = dsZ1[co.CPer].where(bo).sel(
        **{co.R_CENTER:slice(0,.5),co.ZM:slice(0,100000)}
    ).sum([co.TH_CENTER,co.R_CENTER,co.ZM]).groupby('hours').median()
    ax = res.plot(color=FLP.COLORS[i],linewidth=4,marker=mks[i])
    ax = ax[0]
    ax = ax.axes
ax.set_yscale('log')
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_59_0.png)



```python

```


```python

```




    <matplotlib.axes._subplots.AxesSubplot at 0x124cb60f0>




```python
path_bc = '/Users/diego/JUP/co_bc/data/horiba_chc_corrected_diego.csv'
```


```python
bc,CO,h  = 'abs670','CO_ppbv','hour'
lh = 'Local Time'
dt = 'date'
df = pd.read_csv(path_bc)
df[lh]=np.mod(df[h]-4,24)
```


```python
df[dt] = pd.to_datetime(df[dt])
df = df.set_index(dt)
```


```python
desc = df.groupby(lh)[bc].describe()
```


```python
desc['50%'].plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x135b199e8>




![png](full_dispersion_analysis_files/full_dispersion_analysis_66_1.png)



```python

```


```python
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
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_68_0.png)



```python
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
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_69_0.png)



```python
df2.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>flags</th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>11</th>
      <th>12</th>
      <th>13</th>
      <th>14</th>
      <th>15</th>
      <th>16</th>
      <th>17</th>
      <th>18</th>
      <th>19</th>
      <th>20</th>
    </tr>
    <tr>
      <th>releases</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-12-06 00:00:00</th>
      <td>0.707857</td>
      <td>11.028888</td>
      <td>0.663341</td>
      <td>1.574347</td>
      <td>0.003185</td>
      <td>0.211691</td>
      <td>0.200924</td>
      <td>0.000089</td>
      <td>0.172315</td>
      <td>0.315355</td>
      <td>...</td>
      <td>18.721502</td>
      <td>1.257659</td>
      <td>26.563107</td>
      <td>0.049028</td>
      <td>0.538139</td>
      <td>12.072533</td>
      <td>18.425846</td>
      <td>0.003612</td>
      <td>7.086277</td>
      <td>0.239587</td>
    </tr>
    <tr>
      <th>2017-12-06 01:00:00</th>
      <td>0.763443</td>
      <td>11.422018</td>
      <td>0.643527</td>
      <td>1.694550</td>
      <td>0.003165</td>
      <td>0.202774</td>
      <td>0.234895</td>
      <td>0.000161</td>
      <td>0.217352</td>
      <td>0.293642</td>
      <td>...</td>
      <td>17.585632</td>
      <td>1.203361</td>
      <td>27.362309</td>
      <td>0.045951</td>
      <td>0.487157</td>
      <td>12.258152</td>
      <td>17.687378</td>
      <td>0.005014</td>
      <td>7.505631</td>
      <td>0.218183</td>
    </tr>
    <tr>
      <th>2017-12-06 02:00:00</th>
      <td>0.839689</td>
      <td>11.852537</td>
      <td>0.637966</td>
      <td>1.844306</td>
      <td>0.003250</td>
      <td>0.199224</td>
      <td>0.280951</td>
      <td>0.000294</td>
      <td>0.276872</td>
      <td>0.270650</td>
      <td>...</td>
      <td>16.241253</td>
      <td>1.132297</td>
      <td>28.214409</td>
      <td>0.042688</td>
      <td>0.429895</td>
      <td>12.522763</td>
      <td>16.800739</td>
      <td>0.006966</td>
      <td>8.036245</td>
      <td>0.194255</td>
    </tr>
    <tr>
      <th>2017-12-06 03:00:00</th>
      <td>0.938765</td>
      <td>12.270808</td>
      <td>0.663002</td>
      <td>2.018394</td>
      <td>0.003525</td>
      <td>0.207667</td>
      <td>0.339291</td>
      <td>0.000528</td>
      <td>0.351142</td>
      <td>0.250240</td>
      <td>...</td>
      <td>14.766472</td>
      <td>1.045531</td>
      <td>29.011213</td>
      <td>0.039802</td>
      <td>0.371749</td>
      <td>12.879841</td>
      <td>15.817171</td>
      <td>0.009544</td>
      <td>8.653897</td>
      <td>0.170232</td>
    </tr>
    <tr>
      <th>2017-12-06 04:00:00</th>
      <td>1.061315</td>
      <td>12.618526</td>
      <td>0.739574</td>
      <td>2.207890</td>
      <td>0.004091</td>
      <td>0.236792</td>
      <td>0.408405</td>
      <td>0.000921</td>
      <td>0.439090</td>
      <td>0.237385</td>
      <td>...</td>
      <td>13.261915</td>
      <td>0.946363</td>
      <td>29.632080</td>
      <td>0.038023</td>
      <td>0.319167</td>
      <td>13.336612</td>
      <td>14.808998</td>
      <td>0.012794</td>
      <td>9.312475</td>
      <td>0.149067</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>




```python
cols = df2.columns
```


```python
resI.index.name = co.RL
res2 = pd.merge(resI,df2,left_index=True,right_index=True)
res2=res2.dropna()
```


```python
import scipy.optimize.nnls as nnls
```


```python
bcl='eBC [µg/m³]'
res2[bcl]=res2[bc]/6.6
```


```python
A = res2[cols]
Av = A.values
```


```python
b = res2[bcl]
bv = b.values
```


```python
# res = nnls(A,b)
res = nnls(Av[:],bv[:])
```


```python
r0 =res[0]
```


```python
AA = res2.copy()
c=np.dot(A,np.array(r0))
cc = 'reconstructed eBC signal'
AA[cc]=c
```


```python
ax = AA[[bcl,cc]].resample('H').mean().plot()
ax.figure.tight_layout()
ax.set_xlabel('')
ax.figure.savefig('/tmp/abs_mea_cal.pdf')
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_80_0.png)



```python

```


```python

```


```python
r1 = pd.Series(res[0],index=cols)
r1 = r1/r1.sum()
```


```python

```


```python

ax = r1.plot.bar(color = FLP.COLORS)
ax.set_xlabel('cluster region')
ax.set_ylabel('weights [%]')
ax.figure.savefig('/tmp/meas_bar_abs.pdf')
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_85_0.png)



```python
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
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_86_0.png)



![png](full_dispersion_analysis_files/full_dispersion_analysis_86_1.png)



```python
r1.index.name=co.ClusFlag
```


```python
path = '/Volumes/mbProD/Downloads/CHC_QACSM.xlsx'
```


```python
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



```


```python

```


```python
acsm.index.name = co.RL
```


```python
resI.index.name = co.RL
res2 = pd.merge(acsm,df2,left_index=True,right_index=True)
res2=res2.dropna()
```


```python
acsm.columns
```




    Index(['Organics', 'Sulfate', 'Nitrate', 'Ammonium', 'Chloride'], dtype='object')




```python
A = res2[cols]
Av = A.values
```


```python
# c1 = 'Nitrate'
c1 = 'Sulfate'
b = res2[c1]
# bo = b<4
# b = b[bo]
# A = res2[cols][bo]
# Av = A.values
bv = b.values
```


```python
# res = nnls(A,b)
res = nnls(Av[:],bv[:])
```


```python
r1 = pd.Series(res[0],index=cols)
r1 = r1/r1.sum()
ax = r1.plot.bar(color = FLP.COLORS)
ax.set_xlabel('cluster region')
ax.set_ylabel('weights [%]')

ax.figure.savefig('/tmp/sulf_weights.pdf')
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_97_0.png)



```python
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
```


![png](full_dispersion_analysis_files/full_dispersion_analysis_98_0.png)



![png](full_dispersion_analysis_files/full_dispersion_analysis_98_1.png)



```python

```




    array(['2018-04-01 00:00:00', '2018-04-01 01:00:00',
           '2018-04-01 02:00:00', ..., '2018-05-16 21:00:00',
           '2018-05-16 22:00:00', '2018-05-16 23:00:00'], dtype=object)




```python
res2[c1].plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x135e79b70>




![png](full_dispersion_analysis_files/full_dispersion_analysis_100_1.png)



```python

```


```python

```


```python

```


```python

```
