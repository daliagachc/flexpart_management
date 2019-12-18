project name: flexpart_management
created by diego aliaga daliaga_at_chacaltaya.edu.bo


```python

```

imports


```python

from useful_scit.imps import *
# noinspection PyUnresolvedReferences
import matplotlib.colors
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
# noinspection PyUnresolvedReferences
import flexpart_management.modules.flx_array as fa
```

    reload


    2019-12-13 14:36:54,979 useful_scit  WARNING  rpy2 not installed. Everything works except functions requiring r



```python
from sklearn.preprocessing import RobustScaler , QuantileTransformer
from sklearn.cluster import KMeans

import flexpart_management.modules.clustering_funs as cfuns
```


```python

plt.rcParams[ 'figure.facecolor' ] = 'white'
```


```python

# def main() :
```


```python

```


```python

log.ger.setLevel( log.log.DEBUG )
```


```python
# noinspection SpellCheckingInspection
path = \
    '/homeappl/home/aliagadi/wrk/DONOTREMOVE' \
'/flexpart_management_data/runs/' \
'run_2019-10-02_13-42-52_/' \
'log_pol/run_2019-10-02_13-42-52_'
# flp = FLP.FlexLogPol(path,concat=True)
# flp_instance = FLP.FlexLogPol(path,concat=False)
selfFLP = FlexLogPol.FlexLogPol(
    path ,
    # concat=True,
    concat=False ,
    get_clusters=False ,
    # open_merged=False,
    open_merged=True ,
    # merge_ds=False ,
# merge_ds=True ,
    clusters_avail=False ,

    # postprocess set to false since we are opening the reinterpolated
# version
    postprocess=False ,

    use_new_merge_fun=True ,

    # set to false bc already done in the saved version
    filter_r_min_max=False ,
    )
```

    2019-12-13 14:37:02,424 useful_scit  DEBUG    opening the concat files from disk
    2019-12-13 14:37:02,570 useful_scit  DEBUG    opening the merged ds



```python
selfFLP.get_list_datasets_saved()
```




    ['/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-10-02_13-42-52_/log_pol/run_2019-10-02_13-42-52_/working_datasets/ds_clustered_18.nc',
     '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-10-02_13-42-52_/log_pol/run_2019-10-02_13-42-52_/working_datasets/ds_above_sea_level.nc']




```python
# ds = re_interpolate_merged_processed_ds_and_save( selfFLP )
ds = selfFLP.open_ds_version('ds_clustered_18.nc')
```


```python
# ds_small = ds[{co.RL:slice(None,None,100)}]
```


```python
n_clusters = 18
for i in range( n_clusters ) :
# for i in [  ] :
    cfuns.clus_plot( i ,
               ds ,
               # conc_lab= co.CC,
               conc_lab=co.CONC_SMOOTH_NORM ,
               )
```

    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_1.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_3.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_5.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_7.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_9.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_11.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_13.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_15.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_17.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_19.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_21.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_23.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_25.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_27.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_29.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_31.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_33.png)


    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/clustering_funs.py:1095: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      plot_threshold = lab_sum_th.max() * .05



![png](01_post_clustering_files/01_post_clustering_13_35.png)



```python
23
```




    23




```python

```


```python

```


```python

```


```python

```


```python

```
