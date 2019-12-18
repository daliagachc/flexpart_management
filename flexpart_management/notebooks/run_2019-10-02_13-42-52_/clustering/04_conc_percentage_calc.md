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



<div class="bk-root">
    <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
    <span id="1001">Loading BokehJS ...</span>
</div>




    reload



```python
import flexpart_management.modules.clustering_funs as cfuns
from flexpart_management.modules.clustering_funs import (
    add_total_per_row ,
    add_time_per_row ,
    )

plt.rcParams[ 'figure.facecolor' ] = 'white'
co.LAB = 'lab'

plt.style.use('seaborn-whitegrid')
plt.rcParams["legend.frameon"] = True
plt.rcParams["legend.fancybox"] = True
```


```python
# def main() :

log.ger.setLevel( log.log.DEBUG )
```


```python
# noinspection PyUnusedLocal,PyShadowingNames
def open_if_taito() :
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

                 # postprocess set to false since we are opening the re interpolated
                 # version
                 postprocess=False ,

                 use_new_merge_fun=True ,

                 # set to false bc already done in the saved version
                 filter_r_min_max=False ,
                 )
                 selfFLP.get_list_datasets_saved()
                 # noinspection PyUnresolvedReferences
                 ds = selfFLP.open_ds_version( 'ds_clustered_18.nc' )
                 return selfFLP , ds
```


```python
# selfFLP,ds = open_if_taito()
path = '/Users/diego/flexpart_management/flexpart_management/tmp_data' \
   '/ds_clustered_18.nc'
ds = xr.open_dataset( path )
```


```python

```


```python

```


```python
conc_lab = 'CONC_smooth_t_300_z_25_r_100_th_50'
new_lab_p = 'conc_smooth_p'
new_lab_p_t = 'conc_smooth_p_t'
add_total_per_row( ds , conc_lab , new_lab_p )
add_time_per_row( ds , conc_lab , new_lab_p_t )
# print( da_tot )
```


```python
# ds[new_lab_p].sum([co.RL,co.ZM],keep_attrs=True).plot()
# plt.show()
# ds[new_lab_p_t].sum(fa.get_dims_complement(ds,co.RL),keep_attrs=True).plot()
# plt.show()
```


```python
n_clusters = 18
for i in range(n_clusters) :
    # for i in [  ] :
    cfuns.clus_plot( i ,
                     ds ,
                     # conc_lab= co.CC,
                     conc_lab=new_lab_p ,
                     figure_size=12,
                     dpi=100,
                     conc_lab_ts = new_lab_p_t
                     )

plt.show()
```

    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_2.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_5.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_8.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_11.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_14.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_17.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_20.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_23.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_26.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_29.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_32.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_35.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_38.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_41.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_44.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_47.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_50.png)


    {'long_name': 'source receptor relationships (SRR)', 'total': 1336599876.6291237, 'units': '% of total'}
    -90.0


    /Users/diego/flexpart_management/flexpart_management/modules/clustering_funs.py:1109: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      f.tight_layout()



![png](04_conc_percentage_calc_files/04_conc_percentage_calc_12_53.png)



```python
# main()
```


```python

```


```python


#
```


```python

```


```python

```


```python

```
