```python
%load_ext autoreload
%autoreload 2
```


```python
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FLP
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
import pandas as pd
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
self.python_cluster(n_cluster=15)
```


```python
i = 5 
```


```python

```


```python
fig = self.plot_cluster_grid(i=i,par_to_plot=co.CPer)
```


![png](lapaz_cluster_15_files/lapaz_cluster_15_7_0.png)



```python
i=5
self.plot_hout_influence(i)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x196d5bcc0>




![png](lapaz_cluster_15_files/lapaz_cluster_15_8_1.png)



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




    <matplotlib.axes._subplots.AxesSubplot at 0x1a15027f0>




![png](lapaz_cluster_15_files/lapaz_cluster_15_13_1.png)



```python
ds = self.merged_ds.where(self.merged_ds[co.FLAGS]==i)
```


```python
ds1 = ds.groupby(co.RL).sum()
```


```python
dfF = ds1.to_dataframe().drop(columns=lt)
```


```python
res = pd.merge(df,dfF,left_index=True,right_index=True)[[bc,co.CPer,CO,lh]]
```


```python
p1,p2,p3 = ['25%','50%','75%']
desc = res.groupby(lh)[bc].describe()
```


```python
fig,ax = plt.subplots()
ax.plot(desc[p2],color='k',label=p2)
ax.fill_between(desc.index,desc[p1],desc[p3],alpha=.2,label='{}-{}'.format(p1,p3))
ax.grid(True)
ax.legend()
tickrange = np.arange(0,25,3)
ax.set_xticks(tickrange);
ax.set_ylabel(bc)
ax.set_yscale('log')

```


![png](lapaz_cluster_15_files/lapaz_cluster_15_19_0.png)



```python
ax.legend()
```




    <matplotlib.legend.Legend at 0x1a4ec1da0>




```python

```
