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
path = '/Volumes/mbProD/Downloads/flx_log_coor/run_2019-06-05_18-42-11_'
path = '/Volumes/mbProD/Downloads/flx_log_coor/run_2019-06-10_11-10-03_'

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
```

    'using vol for conc'



```python
self.reset_z_levels()
```

    'using vol for conc'



```python
self.python_cluster(n_cluster=15)
```


```python

for i in range(len(self.cluster_flags)):
# for i in range(1):
    fig = self.plot_cluster_grid(i,co.CPer)
```


![png](flex_output_15_clusters_files/flex_output_15_clusters_5_0.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_1.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_2.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_3.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_4.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_5.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_6.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_7.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_8.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_9.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_10.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_11.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_12.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_13.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_5_14.png)



```python
self.plot_clusters_inlfuence(cols=3)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x21d967320>




![png](flex_output_15_clusters_files/flex_output_15_clusters_6_1.png)



```python
# i = 5 
for i in range(len(self.cluster_flags)):
# for i in [i]:
    ax = self.plot_hout_influence(i,log=True)
```


![png](flex_output_15_clusters_files/flex_output_15_clusters_7_0.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_1.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_2.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_3.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_4.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_5.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_6.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_7.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_8.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_9.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_10.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_11.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_12.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_13.png)



![png](flex_output_15_clusters_files/flex_output_15_clusters_7_14.png)



```python

```
