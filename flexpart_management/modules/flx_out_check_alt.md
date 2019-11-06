```python
%load_ext autoreload
%autoreload 2
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload



```python
from useful_scit.imps import *
```


```python
import flexpart_management.modules.FlxOutCheckAlt as FCA
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
```


```python
path_pat = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/*-*-*/'
dom = 'd01'
out_path ='/tmp/z_ds.nc'

self = FCA.FlxOutCheckAlt(path_pat,dom=dom,out_z_path=out_path)




```


```python
self.save_z_sum_ds()
```


```python
dim2sum
```




    ['releases', 'ageclass', 'south_north', 'west_east', 'Time']




```python

```
