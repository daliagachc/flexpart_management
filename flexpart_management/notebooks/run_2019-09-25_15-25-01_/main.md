```python
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

import funs

mpl.rcParams['figure.dpi'] = 150
```


```python
# class Dummy:
# def __init__(self):
# # pass

        # %%
path = \
'/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/' + \
'run_2019-09-25_15-25-01_/log_pol/run_2019-09-25_15-25-01_'
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

    reload


    2019-10-09 13:53:28,577 useful_scit  WARNING  rpy2 not installed. Everything works except functions requiring r


    'using vol for conc'
    starting



```python
selfFLP.reset_z_levels()
```

    'using vol for conc'



```python
dsF= selfFLP.filter_hours_with_few_mea()
```

    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/missing.py:207: FutureWarning: This DataArray contains multi-dimensional coordinates. In the future, these coordinates will be transposed as well unless you specify transpose_coords=False.
      keep_attrs=True).transpose(*self.dims)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/missing.py:207: FutureWarning: This DataArray contains multi-dimensional coordinates. In the future, these coordinates will be transposed as well unless you specify transpose_coords=False.
      keep_attrs=True).transpose(*self.dims)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/missing.py:207: FutureWarning: This DataArray contains multi-dimensional coordinates. In the future, these coordinates will be transposed as well unless you specify transpose_coords=False.
      keep_attrs=True).transpose(*self.dims)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/missing.py:207: FutureWarning: This DataArray contains multi-dimensional coordinates. In the future, these coordinates will be transposed as well unless you specify transpose_coords=False.
      keep_attrs=True).transpose(*self.dims)



```python
dsSM = ds1 = FlexLogPol.smooth_merged_ds(
    dsF
    )
```

    (4248, 6, 35, 36)
    (4248, 6, 35, 36)
    (4248, 6, 35, 36)
    (4248, 6, 35, 36)



```python
funs.plot_general(ds1)
funs.plot_general(selfFLP.merged_ds)
```




    <cartopy.mpl.geoaxes.GeoAxesSubplot at 0x7fa2a2f18e48>




![png](main_files/main_5_1.png)



![png](main_files/main_5_2.png)



```python
funs.plot_general_lapaz(ds1)
funs.plot_general_lapaz(selfFLP.merged_ds)
```




    <cartopy.mpl.geoaxes.GeoAxesSubplot at 0x7fa2a804be80>




![png](main_files/main_6_1.png)



![png](main_files/main_6_2.png)



```python
dsZ = dsSM.copy()
dfcc = selfFLP.get_vector_df_for_clustering(selfFLP.coarsen_par, ar=dsZ[co.CONC])


```


```python
funs.plot_hist_values(dfcc)
```


![png](main_files/main_8_0.png)



```python
funs.plot_hist_all_values(dfcc)
```


![png](main_files/main_9_0.png)



```python

```


```python

# lest create the dataset again
dscc = funs.rebuild_the_dscc(dfcc)

funs.print_percentage_res_time_mass_considered(dscc)
```

    97.91222810745239



```python

MAX_LENGTH = 25
dscc = funs.preprocess_dscc_for_clustering(MAX_LENGTH, dscc)
```


```python
funs.plot_cells_used_for_clustering(dscc)
```


![png](main_files/main_13_0.png)



```python
funs.plot_sample_of_vectors_norm_used_for_clustering(dscc)
```


![png](main_files/main_14_0.png)



```python
funs.plot_hist_all_log(dscc[co.CONC_NORMS])
```


![png](main_files/main_15_0.png)



```python
funs.plot_hist_all_log(dscc[co.CONC_NORMS].where(dscc[co.LAB_CLUSTER_THRESHOLD]))
```


![png](main_files/main_16_0.png)



```python
# this one take a long time
dscc = funs.do_clust_multiple(dscc)
```


```python
funs.plot_bar_charts_for_each_cluster_set(dscc)
```


![png](main_files/main_18_0.png)



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





    [<matplotlib.lines.Line2D at 0x7fa2a8435198>]




![png](main_files/main_20_2.png)



```python
# ii = 2
```


```python
# _d = dscc.loc[{co.CLUS_LENGTH_DIM:ii}][[co.FLAG,co.SIL_SC,SIL_SAMPLE]].stack({co.DUM_STACK:[co.R_CENTER,co.TH_CENTER,co.ZM]})
```


```python
funs.plot_sil_score_grid(dscc)
```


![png](main_files/main_23_0.png)



```python
_n = 4
# _f = 2
_ss1 = funs.get_df_for_plot(_n, dscc)
```


![png](main_files/main_24_0.png)



![png](main_files/main_24_1.png)



```python
_ss1.plot(sharex=True,sharey=True, layout=(2, -1),subplots=True,figsize=(10,5),color=ucp.cc);
```


![png](main_files/main_25_0.png)



```python
_ss1.plot.area(legend=True, figsize=(12,6),color=ucp.cc)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fa2a7938f60>




![png](main_files/main_26_1.png)



```python
dscc
```




    <xarray.Dataset>
    Dimensions:                (CLUS_LENGTH_DIM: 23, R_CENTER: 36, TH_CENTER: 36, ZMID: 6, releases: 1062)
    Coordinates:
      * R_CENTER               (R_CENTER) float64 0.05613 0.06721 ... 25.53 30.57
      * TH_CENTER              (TH_CENTER) float64 0.08727 0.2618 ... 6.021 6.196
      * ZMID                   (ZMID) float64 250.0 1e+03 2.5e+03 ... 8.5e+03 2e+04
      * releases               (releases) datetime64[ns] 2017-12-06T01:30:00 ... 2018-05-31T21:30:00
      * CLUS_LENGTH_DIM        (CLUS_LENGTH_DIM) int64 2 3 4 5 6 ... 20 21 22 23 24
    Data variables:
        CONC                   (R_CENTER, TH_CENTER, ZMID, releases) float32 0.0 ... 0.0
        CONC_SUM               (R_CENTER, TH_CENTER, ZMID) float32 0.0 ... 19.822586
        LAB_CLUSTER_THRESHOLD  (R_CENTER, TH_CENTER, ZMID) bool False ... False
        CONC_NORMALIZED        (releases, R_CENTER, TH_CENTER, ZMID) float32 0.0 ... 0.0
        CONC_NORMS             (R_CENTER, TH_CENTER, ZMID) float32 1.0 ... 3.4963744
        KMEAN_LAB              (CLUS_LENGTH_DIM) object KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
           n_clusters=2, n_init=10, n_jobs=None, precompute_distances='auto',
           random_state=388345, tol=0.0001, verbose=0) ... KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
           n_clusters=24, n_init=10, n_jobs=None, precompute_distances='auto',
           random_state=388345, tol=0.0001, verbose=0)
        FLAG                   (CLUS_LENGTH_DIM, R_CENTER, TH_CENTER, ZMID) int32 1 ... 11
        SIL_SCORE              (CLUS_LENGTH_DIM) float64 0.1246 0.1374 ... 0.1661
        SIL_SAMPLE             (CLUS_LENGTH_DIM, R_CENTER, TH_CENTER, ZMID) float64 nan ... nan




```python
dscc = funs.add_lat_lon_to_dscc(dscc, selfFLP)
```


```python
funs.plot_clust_in_bolivia(_n, dscc)
```


![png](main_files/main_29_0.png)



```python
_n = 18
funs.plot_clust_in_lapaz(_n, dscc)
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

_n = 18
funs.plot_clust_bolivia_individual(_n, dscc)
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
_f = 2
_n = 18
funs.plot_distance_height_chc(_n, dscc)
```


![png](main_files/main_32_0.png)



![png](main_files/main_32_1.png)



![png](main_files/main_32_2.png)



![png](main_files/main_32_3.png)



![png](main_files/main_32_4.png)



![png](main_files/main_32_5.png)



![png](main_files/main_32_6.png)



![png](main_files/main_32_7.png)



![png](main_files/main_32_8.png)



![png](main_files/main_32_9.png)



![png](main_files/main_32_10.png)



![png](main_files/main_32_11.png)



![png](main_files/main_32_12.png)



![png](main_files/main_32_13.png)



![png](main_files/main_32_14.png)



![png](main_files/main_32_15.png)



![png](main_files/main_32_16.png)



![png](main_files/main_32_17.png)



```python
dscc = funs.add_dis_km_dscc(dscc)
```


```python
dsF[co.TOPO]
```




    <xarray.DataArray 'TOPOGRAPHY' (R_CENTER: 36, TH_CENTER: 36)>
    array([[4858.383 , 4967.62  , 5007.2373, ..., 4880.5156, 4789.8086, 4899.203 ],
           [4784.0117, 4850.6484, 4955.0063, ..., 5060.6313, 5098.8477, 4992.897 ],
           [4691.9575, 4718.7505, 4799.628 , ..., 5173.5557, 5367.306 , 5034.177 ],
           ...,
           [   0.    ,    0.    ,    0.    , ...,    0.    ,    0.    ,    0.    ],
           [   0.    ,    0.    ,    0.    , ...,    0.    ,    0.    ,    0.    ],
           [   0.    ,    0.    ,    0.    , ...,    0.    ,    0.    ,    0.    ]],
          dtype=float32)
    Coordinates:
      * R_CENTER    (R_CENTER) float64 0.05613 0.06721 0.08046 ... 21.33 25.53 30.57
      * TH_CENTER   (TH_CENTER) float64 0.08727 0.2618 0.4363 ... 5.847 6.021 6.196
        LON         (R_CENTER, TH_CENTER) float64 -68.08 -68.08 ... -38.6 -37.68
        LAT_00      (R_CENTER, TH_CENTER) float64 -16.3 -16.3 -16.3 ... 9.903 11.16
        LON_00      (R_CENTER, TH_CENTER) float64 -68.13 -68.12 ... -77.69 -72.98
        LAT_10      (R_CENTER, TH_CENTER) float64 -16.29 -16.29 ... 15.08 16.59
        LON_10      (R_CENTER, TH_CENTER) float64 -68.13 -68.12 ... -79.57 -73.94
        LAT_11      (R_CENTER, TH_CENTER) float64 -16.29 -16.29 -16.3 ... 16.59 17.1
        LON_11      (R_CENTER, TH_CENTER) float64 -68.12 -68.11 ... -73.94 -68.13
        LAT_01      (R_CENTER, TH_CENTER) float64 -16.3 -16.3 -16.31 ... 11.16 11.59
        LON_01      (R_CENTER, TH_CENTER) float64 -68.12 -68.11 ... -72.98 -68.13
        GRIDAREA    (R_CENTER, TH_CENTER) float64 1.178e+06 1.178e+06 ... 3.528e+11
        TOPOGRAPHY  (R_CENTER, TH_CENTER) float32 4858.383 4967.62 ... 0.0 0.0
        LAT         (R_CENTER, TH_CENTER) float64 -16.29 -16.3 -16.3 ... 13.18 14.1




```python
mpl.rcParams['figure.dpi'] = 300
_cols = 6
_rows = 3
fig, axs = plt.subplots(_rows,_cols,sharex=True,sharey=True,figsize=(3.5*_cols,2.5*_rows))
axsf = axs.flatten()

log.ger.setLevel(log.log.ERROR)
_ds = funs.plot_dis_height_quantiles_chc(_n, dsF, dscc,axs=axsf)
fig.tight_layout()
```

    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)



![png](main_files/main_35_1.png)



```python
mpl.rcParams['figure.dpi'] = 300
_cols = 6
_rows = 3
fig, axs = plt.subplots(_rows,_cols,sharex=True,sharey=True,figsize=(3.5*_cols,2.5*_rows))
axsf = axs.flatten()

log.ger.setLevel(log.log.ERROR)

```


```python
for _f in range(_n):
    ax = axsplot(figsize=(5,4))
    funs.plot_dis_height_quantiles_chc_single(_f,_n, dsF, dscc,axs=ax)
```

    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)



![png](main_files/main_37_1.png)



![png](main_files/main_37_2.png)



![png](main_files/main_37_3.png)



![png](main_files/main_37_4.png)



![png](main_files/main_37_5.png)



![png](main_files/main_37_6.png)



![png](main_files/main_37_7.png)



![png](main_files/main_37_8.png)



![png](main_files/main_37_9.png)



![png](main_files/main_37_10.png)



![png](main_files/main_37_11.png)



![png](main_files/main_37_12.png)



![png](main_files/main_37_13.png)



![png](main_files/main_37_14.png)



![png](main_files/main_37_15.png)



![png](main_files/main_37_16.png)



![png](main_files/main_37_17.png)



![png](main_files/main_37_18.png)



```python

```




    True




```python
!jupyter-nbconvert --to markdown main.ipynb
```

    [NbConvertApp] Converting notebook main.ipynb to markdown
    [NbConvertApp] Support files will be in main_files/
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Making directory main_files
    [NbConvertApp] Writing 44275 bytes to main.md



```python
dscc[co.CONC].sum([co.TH_CENTER,co.ZM,co.RL]).plot()
```




    [<matplotlib.lines.Line2D at 0x7fa2a6e30ef0>]




![png](main_files/main_40_1.png)



```python
dscc[co.CONC].sum([co.TH_CENTER,co.RL]).plot.line(x=co.R_CENTER);
```


![png](main_files/main_41_0.png)



```python
_n = 18
funs.plot_influences(_n, dscc)
```


![png](main_files/main_42_0.png)



```python
less_than = 1000000
more_than = 0
height_less_than = 100000000

_ds = dscc.loc[{co.CLUS_LENGTH_DIM: _n}].copy()
try: _ds = _ds.drop(co.KMEAN_OBJ)
except: pass

_dss = _ds.copy()
_ds[co.CONC] = _ds[co.CONC].where(dscc[co.R_CENTER] < less_than,
                                  0).where(
    dscc[co.R_CENTER] > more_than, 0).where(
    dscc[co.ZM] < height_less_than, 0)
_ds1 = _ds[[co.CONC, co.FLAG]]
_dss1 = _dss[[co.CONC, co.FLAG]]
_ds2 = _ds1.to_dataframe()
_dss2 = _dss1.to_dataframe()
_ds3 = _ds2[[co.CONC, co.FLAG]]
_dss3 = _dss2[[co.CONC, co.FLAG]]
_df = _ds3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],
                       drop=True).reset_index().set_index(
    [co.FLAG, co.RL])
_dff = _dss3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],
                         drop=True).reset_index().set_index(
    [co.FLAG, co.RL])
_df1 = _df.sort_index().groupby([co.FLAG, co.RL]).sum()
_dff1 = _dff.sort_index().groupby([co.FLAG, co.RL]).sum()
_df2 = _df1.unstack(co.FLAG)[co.CONC]
_dff2 = _dff1.unstack(co.FLAG)[co.CONC]
_df2 = 100 * (_df2.T / _dff2.T.sum()).T

```


```python
_f = 1 
for _f in range(_n):
    ax = axsplot()
    _df3 = _df2[_f]
    ax=_df3.plot( figsize=(15, 1.5),
              color=[[*ucp.cc, *ucp.cc][_f]])
    ax.set_title(f'{_f}')
    ax.set_ylabel('SRR [%]')

```


![png](main_files/main_44_0.png)



![png](main_files/main_44_1.png)



![png](main_files/main_44_2.png)



![png](main_files/main_44_3.png)



![png](main_files/main_44_4.png)



![png](main_files/main_44_5.png)



![png](main_files/main_44_6.png)



![png](main_files/main_44_7.png)



![png](main_files/main_44_8.png)



![png](main_files/main_44_9.png)



![png](main_files/main_44_10.png)



![png](main_files/main_44_11.png)



![png](main_files/main_44_12.png)



![png](main_files/main_44_13.png)



![png](main_files/main_44_14.png)



![png](main_files/main_44_15.png)



![png](main_files/main_44_16.png)



![png](main_files/main_44_17.png)



```python
_n = 18
less_than = .5
more_than = .05
height_less_than = 1000

funs.plot_target_distance_height_influence(_n, dscc, height_less_than,
                                           less_than, more_than)
```


![png](main_files/main_45_0.png)



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

    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/core/nanops.py:160: RuntimeWarning: Mean of empty slice
      return np.nanmean(a, axis=axis, dtype=dtype)



```python
_n = 18
funs.plot_influences(_n, _dscc)
```


![png](main_files/main_49_0.png)



```python
_n = 18
less_than = .3
more_than = .15
height_less_than = 1000

funs.plot_target_distance_height_influence(_n, _dscc, height_less_than,
                                           less_than, more_than)
```


![png](main_files/main_50_0.png)



```python
_ns = [0,2,8,9,11,14]

for _nn in _ns:

    funs.plot_hour_influence_targeted(_n, _nn, _dscc, height_less_than,
                                      less_than, more_than)
```


    ----------------------------------------

    KeyboardInterruptTraceback (most recent call last)

    <ipython-input-43-08f58a90871a> in <module>
          4 
          5     funs.plot_hour_influence_targeted(_n, _nn, _dscc, height_less_than,
    ----> 6                                       less_than, more_than)
    

    ~/saltena_2018/flexpart_management/flexpart_management/notebooks/run_2019-09-25_15-25-01_/funs.py in plot_hour_influence_targeted(_n, _nn, dscc, height_less_than, less_than, more_than)
        417     _dss3 = _dss2[[co.CONC, co.FLAG]]
        418     _df = _ds3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],
    --> 419                            drop=True).reset_index().set_index(
        420         [co.FLAG, co.RL])
        421     _dff = _dss3.reset_index([co.R_CENTER, co.TH_CENTER, co.ZM],


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/pandas/core/frame.py in reset_index(self, level, drop, inplace, col_level, col_fill)
       4610             new_obj = self
       4611         else:
    -> 4612             new_obj = self.copy()
       4613 
       4614         def _maybe_casted_values(index, labels=None):


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/pandas/core/generic.py in copy(self, deep)
       5994         dtype: object
       5995         """
    -> 5996         data = self._data.copy(deep=deep)
       5997         return self._constructor(data).__finalize__(self)
       5998 


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/pandas/core/internals/managers.py in copy(self, deep)
        786         else:
        787             new_axes = list(self.axes)
    --> 788         return self.apply("copy", axes=new_axes, deep=deep, do_integrity_check=False)
        789 
        790     def as_array(self, transpose=False, items=None):


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/pandas/core/internals/managers.py in apply(self, f, axes, filter, do_integrity_check, consolidate, **kwargs)
        442             return self.make_empty(axes or self.axes)
        443         bm = self.__class__(
    --> 444             result_blocks, axes or self.axes, do_integrity_check=do_integrity_check
        445         )
        446         bm._consolidate_inplace()


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/pandas/core/internals/managers.py in __init__(self, blocks, axes, do_integrity_check)
        143             self._verify_integrity()
        144 
    --> 145         self._consolidate_check()
        146 
        147         self._rebuild_blknos_and_blklocs()


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/pandas/core/internals/managers.py in _consolidate_check(self)
        653 
        654     def _consolidate_check(self):
    --> 655         ftypes = [blk.ftype for blk in self.blocks]
        656         self._is_consolidated = len(ftypes) == len(set(ftypes))
        657         self._known_consolidated = True


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/pandas/core/internals/managers.py in <listcomp>(.0)
        653 
        654     def _consolidate_check(self):
    --> 655         ftypes = [blk.ftype for blk in self.blocks]
        656         self._is_consolidated = len(ftypes) == len(set(ftypes))
        657         self._known_consolidated = True


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/pandas/core/internals/blocks.py in ftype(self)
        351         else:
        352             dtype = self.dtype
    --> 353         return "{dtype}:{ftype}".format(dtype=dtype, ftype=self._ftype)
        354 
        355     def merge(self, other):


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/numpy/core/_dtype.py in __str__(dtype)
         52         return dtype.str
         53     else:
    ---> 54         return dtype.name
         55 
         56 


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/numpy/core/_dtype.py in _name_get(dtype)
        317 
        318 
    --> 319 def _name_get(dtype):
        320     # provides dtype.name.__get__
        321 


    KeyboardInterrupt: 



![png](main_files/main_51_1.png)



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


```python
r1 = pd.Series(res[0],index=cols)
r1 = 100*r1/r1.sum()


ax = r1.plot.bar(color = [*ucp.cc,*ucp.cc])
ax.set_xlabel('cluster region')
ax.set_ylabel('weights [%]')
ax.figure.savefig('/tmp/meas_bar_abs.pdf')
```


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


```python





```
