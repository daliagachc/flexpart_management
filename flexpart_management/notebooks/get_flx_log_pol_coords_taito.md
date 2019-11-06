```python
# this notebook was created to convert rectanfular coo

%load_ext autoreload
%autoreload 2
```


```python
import flexpart_management.modules.FLEXOUT as FO
import flexpart_management.modules.flx_array as fa
from useful_scit.imps import *
```


```python
doms = ['d01','d02']
root_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/*-*-*'
root_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/*-*-*'
path_out = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/log_pol'

run_name = 'run_2019-06-05_18-42-11_'
paths = glob.glob(root_path)
paths.sort()
```


```python
fo_base_dic  = dict(
# dom = 'd01',
# folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
folder_path_out = path_out,
run_name= run_name,
)
```


```python
for p in paths:
    for d in doms:
        print('starting',d,p)
        new_dic = dict(dom=d,folder_path=p)
        fo_dic = {**fo_base_dic,**new_dic}
        
        try:
            fo = FO.FLEXOUT(**fo_dic)
            fo.export_log_polar_coords()
            print('done',d,p)
        except:
            print('failed when',d,p)
        
```
