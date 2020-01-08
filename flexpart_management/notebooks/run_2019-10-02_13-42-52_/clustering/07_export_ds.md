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
# main()
```


```python

```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-8-c1ddc717b0d7> in <module>
    ----> 1 dsum
    

    NameError: name 'dsum' is not defined



```python
N_CLUSTERS = 18
ds_lab_dic = { }
for ci in range( N_CLUSTERS ) :
    ds_lab = ds[ [ new_lab_p ] ].where( ds[ co.LAB ] == ci ).copy()
    ds_lab_dic[ ci ] = ds_lab.copy()
```


```python
i=0
ll = [] 
for i in range(N_CLUSTERS):
    dsum = ds_lab_dic[i].sum([co.R_CENTER,co.TH_CENTER,co.ZM])
    dsum = dsum.expand_dims(**{'lab':[i]})
    ll.append(dsum)

#
```


```python
mega_ds = xr.concat(ll,dim='lab')
```


```python
df_ = mega_ds.to_dataframe()
```


```python
df1 = df_.unstack(0)
```


```python
df1.to_excel(f'/Users/diego/flexpart_management/flexpart_management/presentations/{new_lab_p}.xls')
```


```python
N_CLUSTERS = 18
ds_lab_dic_t = { }
for ci in range( N_CLUSTERS ) :
    ds_lab = ds[ [ new_lab_p_t ] ].where( ds[ co.LAB ] == ci ).copy()
    ds_lab_dic_t[ ci ] = ds_lab.copy()
```


```python
i=0
ll_t = [] 
for i in range(N_CLUSTERS):
    dsum = ds_lab_dic_t[i].sum([co.R_CENTER,co.TH_CENTER,co.ZM])
    dsum = dsum.expand_dims(**{'lab':[i]})
    ll_t.append(dsum)

#
```


```python
mega_ds = xr.concat(ll_t,dim='lab')
```


```python
df_ = mega_ds.to_dataframe()
```


```python
df1 = df_.unstack(0)
```


```python
df1.to_excel(f'/Users/diego/flexpart_management/flexpart_management/presentations/{new_lab_p_t}.xls')
```


```python

```


```python
df_
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
      <th></th>
      <th></th>
      <th>conc_smooth_p</th>
    </tr>
    <tr>
      <th>lab</th>
      <th>releases</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="5" valign="top">0</td>
      <td>2017-12-06 00:00:00</td>
      <td>0.004653</td>
    </tr>
    <tr>
      <td>2017-12-06 01:00:00</td>
      <td>0.004448</td>
    </tr>
    <tr>
      <td>2017-12-06 02:00:00</td>
      <td>0.004073</td>
    </tr>
    <tr>
      <td>2017-12-06 03:00:00</td>
      <td>0.003590</td>
    </tr>
    <tr>
      <td>2017-12-06 04:00:00</td>
      <td>0.003074</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td rowspan="5" valign="top">152</td>
      <td>2018-05-31 19:00:00</td>
      <td>0.000051</td>
    </tr>
    <tr>
      <td>2018-05-31 20:00:00</td>
      <td>0.000073</td>
    </tr>
    <tr>
      <td>2018-05-31 21:00:00</td>
      <td>0.000096</td>
    </tr>
    <tr>
      <td>2018-05-31 22:00:00</td>
      <td>0.000116</td>
    </tr>
    <tr>
      <td>2018-05-31 23:00:00</td>
      <td>0.000127</td>
    </tr>
  </tbody>
</table>
<p>649944 rows × 1 columns</p>
</div>




```python

```
