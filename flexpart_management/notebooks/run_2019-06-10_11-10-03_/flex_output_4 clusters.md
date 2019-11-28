```python
%load_ext autoreload
%autoreload 2
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload



```python
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FLP
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
```


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
self.python_cluster(n_cluster=4)
```


```python

for i in range(len(self.cluster_flags)):
# for i in range(1):
    fig = self.plot_cluster_grid(i,co.CPer)
```


![png](flex_output_4%20clusters_files/flex_output_4%20clusters_5_0.png)



![png](flex_output_4%20clusters_files/flex_output_4%20clusters_5_1.png)



![png](flex_output_4%20clusters_files/flex_output_4%20clusters_5_2.png)



![png](flex_output_4%20clusters_files/flex_output_4%20clusters_5_3.png)



```python
self.plot_clusters_inlfuence(cols=1)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x20e0581d0>




![png](flex_output_4%20clusters_files/flex_output_4%20clusters_6_1.png)
