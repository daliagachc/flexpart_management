```python
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
```


```python
selfFLP.reset_z_levels()
```


```python
dsF= selfFLP.filter_hours_with_few_mea()
```


```python
dsSM = ds1 = FlexLogPol.smooth_merged_ds(
    dsF
    )
```


```python
funs.plot_general(ds1)
```




    <cartopy.mpl.geoaxes.GeoAxesSubplot at 0x121bafda0>




![png](main_files/main_4_1.png)



```python
funs.plot_general_lapaz(ds1)
```




    <cartopy.mpl.geoaxes.GeoAxesSubplot at 0x1479ff9e8>




![png](main_files/main_5_1.png)



```python
dsZ = dsSM.copy()
dfcc = selfFLP.get_vector_df_for_clustering(selfFLP.coarsen_par, ar=dsZ[co.CONC])


```


```python
funs.plot_hist_values(dfcc)
```


![png](main_files/main_7_0.png)



```python
funs.plot_hist_all_values(dfcc)
```


```python

```


```python

# lest create the dataset again
dscc = funs.rebuild_the_dscc(dfcc)

funs.print_percentage_res_time_mass_considered(dscc)
```


```python

MAX_LENGTH = 25
dscc = funs.preprocess_dscc_for_clustering(MAX_LENGTH, dscc)
```


```python
funs.plot_cells_used_for_clustering(dscc)
```


```python
funs.plot_sample_of_vectors_norm_used_for_clustering(dscc)
```


```python
funs.plot_hist_all_log(dscc[co.CONC_NORMS])
```


![png](main_files/main_14_0.png)



```python
funs.plot_hist_all_log(dscc[co.CONC_NORMS].where(dscc[co.LAB_CLUSTER_THRESHOLD]))
```


![png](main_files/main_15_0.png)



```python
# this one take a long time
dscc = funs.do_clust_multiple(dscc)
```


```python
funs.plot_bar_charts_for_each_cluster_set(dscc)
```


![png](main_files/main_17_0.png)



```python

```


```python
dscc = funs.calc_silhouette_scores(dscc)

dscc[co.SIL_SC].plot()
```

    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24





    [<matplotlib.lines.Line2D at 0x13c184550>]




![png](main_files/main_19_2.png)



```python
# ii = 2
```


```python
# _d = dscc.loc[{co.CLUS_LENGTH_DIM:ii}][[co.FLAG,co.SIL_SC,SIL_SAMPLE]].stack({co.DUM_STACK:[co.R_CENTER,co.TH_CENTER,co.ZM]})
```


```python
funs.plot_sil_score_grid(dscc)
```


![png](main_files/main_22_0.png)



```python
_n = 4
# _f = 2
_ss1 = funs.get_df_for_plot(_n, dscc)
```


![png](main_files/main_23_0.png)



![png](main_files/main_23_1.png)



```python
_ss1.plot(sharex=True,sharey=True, layout=(2, -1),subplots=True,figsize=(10,5),color=ucp.cc);
```


![png](main_files/main_24_0.png)



```python
_ss1.plot.area(legend=True, figsize=(12,6),color=ucp.cc)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x13505ae10>




![png](main_files/main_25_1.png)



```python

```


```python
dscc = funs.add_lat_lon_to_dscc(dscc, selfFLP)
```


```python
funs.plot_clust_in_bolivia(_n, dscc)
```


![png](main_files/main_28_0.png)



```python
_n = 18
funs.plot_clust_in_lapaz(_n, dscc)
```


![png](main_files/main_29_0.png)



![png](main_files/main_29_1.png)



![png](main_files/main_29_2.png)



![png](main_files/main_29_3.png)



![png](main_files/main_29_4.png)



![png](main_files/main_29_5.png)



![png](main_files/main_29_6.png)



![png](main_files/main_29_7.png)



![png](main_files/main_29_8.png)



![png](main_files/main_29_9.png)



![png](main_files/main_29_10.png)



![png](main_files/main_29_11.png)



![png](main_files/main_29_12.png)



![png](main_files/main_29_13.png)



![png](main_files/main_29_14.png)



![png](main_files/main_29_15.png)



![png](main_files/main_29_16.png)



![png](main_files/main_29_17.png)



```python

_n = 18
funs.plot_clust_bolivia_individual(_n, dscc)
```


![png](main_files/main_30_0.png)



![png](main_files/main_30_1.png)



![png](main_files/main_30_2.png)



![png](main_files/main_30_3.png)



![png](main_files/main_30_4.png)



![png](main_files/main_30_5.png)



![png](main_files/main_30_6.png)



![png](main_files/main_30_7.png)



![png](main_files/main_30_8.png)



![png](main_files/main_30_9.png)



![png](main_files/main_30_10.png)



![png](main_files/main_30_11.png)



![png](main_files/main_30_12.png)



![png](main_files/main_30_13.png)



![png](main_files/main_30_14.png)



![png](main_files/main_30_15.png)



![png](main_files/main_30_16.png)



![png](main_files/main_30_17.png)



```python
_f = 2
_n = 18
funs.plot_distance_height_chc(_n, dscc)
```


![png](main_files/main_31_0.png)



![png](main_files/main_31_1.png)



![png](main_files/main_31_2.png)



![png](main_files/main_31_3.png)



![png](main_files/main_31_4.png)



![png](main_files/main_31_5.png)



![png](main_files/main_31_6.png)



![png](main_files/main_31_7.png)



![png](main_files/main_31_8.png)



![png](main_files/main_31_9.png)



![png](main_files/main_31_10.png)



![png](main_files/main_31_11.png)



![png](main_files/main_31_12.png)



![png](main_files/main_31_13.png)



![png](main_files/main_31_14.png)



![png](main_files/main_31_15.png)



![png](main_files/main_31_16.png)



![png](main_files/main_31_17.png)



```python
dscc = funs.add_dis_km_dscc(dscc)
```


```python

```


```python
_cols = 6
_rows = 3
fig, axs = plt.subplots(_rows,_cols,sharex=True,sharey=True,figsize=(2*_cols,2*_rows))
axsf = axs.flatten()
_n=18
funs.plot_dis_height_quantiles_chc(_n, dsF, dscc,axs=axsf)
```

    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)



![png](main_files/main_34_1.png)



```python
dscc[co.CONC].sum([co.TH_CENTER,co.ZM,co.RL]).plot()
```




    [<matplotlib.lines.Line2D at 0x1247d9550>]




![png](main_files/main_35_1.png)



```python
dscc[co.CONC].sum([co.TH_CENTER,co.RL]).plot.line(x=co.R_CENTER);
```


![png](main_files/main_36_0.png)



```python
_n = 18
funs.plot_influences(_n, dscc)
```


![png](main_files/main_37_0.png)



```python
_n = 18
less_than = .3
more_than = .15
height_less_than = 1000

funs.plot_target_distance_height_influence(_n, dscc, height_less_than,
                                           less_than, more_than)
```


![png](main_files/main_38_0.png)



```python

_n = 18
```


```python
mdsc = selfFLP.merged_ds.copy()
```


```python
_dscc = dscc.drop([co.KMEAN_OBJ,co.CONC,co.CONC_NORMALIZED,co.RL])
_dscc=xr.merge([mdsc,_dscc])
_dscc[co.CONC] = _dscc[co.CONC].where(_dscc[co.CONC].sum([co.R_CENTER,co.TH_CENTER,co.ZM])>2e5)
_dscc[co.CONC] = _dscc[[co.CONC]].resample(releases='H').mean()[co.CONC]
```

    /Users/diego/miniconda3/envs/b36/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)



```python
_n = 18
funs.plot_influences(_n, _dscc)
```


![png](main_files/main_42_0.png)



```python
_n = 18
less_than = .3
more_than = .15
height_less_than = 1000

funs.plot_target_distance_height_influence(_n, _dscc, height_less_than,
                                           less_than, more_than)
```


![png](main_files/main_43_0.png)



```python
_ns = [0,2,8,9,11,14]

for _nn in _ns:

    funs.plot_hour_influence_targeted(_n, _nn, _dscc, height_less_than,
                                      less_than, more_than)
```


![png](main_files/main_44_0.png)



![png](main_files/main_44_1.png)



![png](main_files/main_44_2.png)



![png](main_files/main_44_3.png)



![png](main_files/main_44_4.png)



![png](main_files/main_44_5.png)



```python
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



```


```python
import scipy.optimize.nnls as nnls
```


```python
_n = 18
# _ds = dscc.loc[{CLUS_LENGTH_DIM:_n}].drop(KMEAN_OBJ)
_ds=_dscc.loc[{co.CLUS_LENGTH_DIM:_n}]
_ds[co.CONC]=100*_ds[co.CONC]/_ds[co.CONC].sum([co.R_CENTER,co.TH_CENTER,co.ZM])
```


```python
_all_c = set(_ds.coords.keys())
```


```python
_dims = set(_ds.dims.keys())
```


```python
_drop = list(_all_c - _dims)
```


```python
_ds1 = _ds[[co.CONC,co.FLAG]].drop(_drop)
```


```python
_ds2 = _ds1.to_dataframe()
```


```python
_ds3=_ds2.groupby([co.FLAG,co.RL]).sum()
```


```python
_df1 = _ds3.unstack(co.FLAG)[co.CONC]
```


```python
cols = _df1.columns
```


```python
res2 = pd.merge(acsm,_df1,left_index=True,right_index=True)
res2=res2.dropna()
```


```python

```


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
r1 = 100*r1/r1.sum()
ax = r1.plot.bar(color = [*ucp.cc,*ucp.cc])
ax.set_xlabel('cluster region')
ax.set_ylabel('weights [%]')

ax.figure.savefig('/tmp/sulf_weights.pdf')
```


![png](main_files/main_61_0.png)



```python
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
```


![png](main_files/main_62_0.png)



![png](main_files/main_62_1.png)



```python
path_bc = '/Users/diego/JUP/co_bc/data/horiba_chc_corrected_diego.csv'
bc,CO,h  = 'abs670','CO_ppbv','hour'
lh = 'Local Time'
dt = 'date'
df = pd.read_csv(path_bc)
df[lh]=np.mod(df[h]-4,24)
df[dt] = pd.to_datetime(df[dt])
df = df.set_index(dt)
```


```python
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
```


![png](main_files/main_64_0.png)



```python
res.index.name = co.RL
res2 = pd.merge(res,_df1,left_index=True,right_index=True)
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
ax = AA[[bcl,cc]].resample('H').mean().plot(figsize=(15,5))
ax.figure.tight_layout()
ax.set_xlabel('')
ax.figure.savefig('/tmp/abs_mea_cal.pdf')
ax.set_yscale('log')
ax.set_ylim(.1,5)
```




    (0.1, 5)




![png](main_files/main_73_1.png)



```python
r1 = pd.Series(res[0],index=cols)
r1 = 100*r1/r1.sum()


ax = r1.plot.bar(color = [*ucp.cc,*ucp.cc])
ax.set_xlabel('cluster region')
ax.set_ylabel('weights [%]')
ax.figure.savefig('/tmp/meas_bar_abs.pdf')
```


![png](main_files/main_74_0.png)



```python
_n = 18
_ds = _dscc.loc[{co.CLUS_LENGTH_DIM:_n}]
```


```python
_df = _ds[[co.CONC,co.FLAG]]
_df = _df.drop(list(set(_df.coords)-set(_df.dims))).to_dataframe()
```


```python
_df = _df.reset_index()[[co.RL,co.CONC,co.FLAG]]
```


```python
_df1 = _df.groupby([co.FLAG,co.RL]).sum()
```


```python
_df2 = _df1[co.CONC].unstack(co.FLAG)
```


```python
_df3 = 100*(_df2.T/_df2.T.sum()).T
```


```python
_df3.to_csv('/tmp/clust18_v00.csv')
```


```python
_df3
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
      <th>FLAG</th>
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
      <th>10</th>
      <th>11</th>
      <th>12</th>
      <th>13</th>
      <th>14</th>
      <th>15</th>
      <th>16</th>
      <th>17</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2017-12-06 00:00:00</td>
      <td>0.070780</td>
      <td>22.868494</td>
      <td>6.569861</td>
      <td>0.001666</td>
      <td>0.359176</td>
      <td>0.000156</td>
      <td>42.874092</td>
      <td>0.000000</td>
      <td>0.648159</td>
      <td>0.578303</td>
      <td>5.986179</td>
      <td>0.066650</td>
      <td>5.966999</td>
      <td>0.038548</td>
      <td>12.553345</td>
      <td>9.570999e-02</td>
      <td>0.271337</td>
      <td>1.050560</td>
    </tr>
    <tr>
      <td>2017-12-06 01:00:00</td>
      <td>0.136718</td>
      <td>26.507875</td>
      <td>5.206011</td>
      <td>0.003282</td>
      <td>0.548890</td>
      <td>0.000381</td>
      <td>43.263142</td>
      <td>0.000000</td>
      <td>0.594684</td>
      <td>0.781243</td>
      <td>5.232129</td>
      <td>0.104835</td>
      <td>6.678673</td>
      <td>0.031022</td>
      <td>9.597729</td>
      <td>1.078369e-01</td>
      <td>0.272245</td>
      <td>0.933307</td>
    </tr>
    <tr>
      <td>2017-12-06 02:00:00</td>
      <td>0.021776</td>
      <td>37.712887</td>
      <td>1.133380</td>
      <td>0.001445</td>
      <td>0.131855</td>
      <td>0.000021</td>
      <td>43.464920</td>
      <td>0.002031</td>
      <td>0.167171</td>
      <td>0.086523</td>
      <td>3.564277</td>
      <td>0.059788</td>
      <td>10.132391</td>
      <td>0.016435</td>
      <td>2.558075</td>
      <td>3.616426e-02</td>
      <td>0.058323</td>
      <td>0.852539</td>
    </tr>
    <tr>
      <td>2017-12-06 03:00:00</td>
      <td>0.017508</td>
      <td>36.160027</td>
      <td>2.850354</td>
      <td>0.000949</td>
      <td>0.132986</td>
      <td>0.000063</td>
      <td>42.033596</td>
      <td>0.000000</td>
      <td>0.135590</td>
      <td>0.103098</td>
      <td>4.154691</td>
      <td>0.082604</td>
      <td>10.501380</td>
      <td>0.029358</td>
      <td>2.685647</td>
      <td>3.497278e-02</td>
      <td>0.048742</td>
      <td>1.028439</td>
    </tr>
    <tr>
      <td>2017-12-06 04:00:00</td>
      <td>0.019021</td>
      <td>38.231937</td>
      <td>10.619304</td>
      <td>0.000039</td>
      <td>0.092714</td>
      <td>0.000000</td>
      <td>32.213829</td>
      <td>0.000000</td>
      <td>0.081277</td>
      <td>1.491897</td>
      <td>1.998419</td>
      <td>0.028500</td>
      <td>12.091787</td>
      <td>0.059037</td>
      <td>1.216002</td>
      <td>1.390249e-02</td>
      <td>0.029708</td>
      <td>1.812618</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>2018-05-16 19:00:00</td>
      <td>2.917524</td>
      <td>4.391117</td>
      <td>15.051891</td>
      <td>0.000147</td>
      <td>0.765345</td>
      <td>0.000000</td>
      <td>0.944150</td>
      <td>0.410699</td>
      <td>13.993229</td>
      <td>2.826778</td>
      <td>0.046040</td>
      <td>2.570739</td>
      <td>29.169893</td>
      <td>4.695522</td>
      <td>12.610127</td>
      <td>4.367301e-07</td>
      <td>0.059859</td>
      <td>9.546943</td>
    </tr>
    <tr>
      <td>2018-05-16 20:00:00</td>
      <td>4.986663</td>
      <td>4.170250</td>
      <td>14.560091</td>
      <td>0.000306</td>
      <td>0.810839</td>
      <td>0.000007</td>
      <td>0.877938</td>
      <td>1.058543</td>
      <td>13.353012</td>
      <td>3.742719</td>
      <td>0.039320</td>
      <td>2.151260</td>
      <td>27.957621</td>
      <td>6.622285</td>
      <td>10.691784</td>
      <td>0.000000e+00</td>
      <td>0.056404</td>
      <td>8.920951</td>
    </tr>
    <tr>
      <td>2018-05-16 21:00:00</td>
      <td>6.117431</td>
      <td>3.960845</td>
      <td>15.068586</td>
      <td>0.000043</td>
      <td>0.812452</td>
      <td>0.000000</td>
      <td>1.025884</td>
      <td>1.483620</td>
      <td>11.683426</td>
      <td>5.483875</td>
      <td>0.017740</td>
      <td>2.272300</td>
      <td>27.354755</td>
      <td>7.185821</td>
      <td>8.876569</td>
      <td>0.000000e+00</td>
      <td>0.052709</td>
      <td>8.603943</td>
    </tr>
    <tr>
      <td>2018-05-16 22:00:00</td>
      <td>6.133749</td>
      <td>4.011127</td>
      <td>16.098446</td>
      <td>0.000000</td>
      <td>1.003015</td>
      <td>0.000006</td>
      <td>0.997278</td>
      <td>1.121742</td>
      <td>11.797158</td>
      <td>6.968419</td>
      <td>0.026934</td>
      <td>2.724398</td>
      <td>26.370811</td>
      <td>5.664712</td>
      <td>8.570171</td>
      <td>2.125354e-09</td>
      <td>0.055763</td>
      <td>8.456272</td>
    </tr>
    <tr>
      <td>2018-05-16 23:00:00</td>
      <td>4.827027</td>
      <td>4.299737</td>
      <td>15.518525</td>
      <td>0.000000</td>
      <td>0.784748</td>
      <td>0.000012</td>
      <td>0.966185</td>
      <td>0.893243</td>
      <td>11.952178</td>
      <td>5.475704</td>
      <td>0.023505</td>
      <td>3.732693</td>
      <td>26.690069</td>
      <td>5.144713</td>
      <td>10.907743</td>
      <td>0.000000e+00</td>
      <td>0.080517</td>
      <td>8.703398</td>
    </tr>
  </tbody>
</table>
<p>3864 rows × 18 columns</p>
</div>




```python





```
