```python
# this notebook was created to convert rectanfular coo

%load_ext autoreload
%autoreload 2
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload



```python
import flexpart_management.modules.FLEXOUT as FO
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co
from useful_scit.imps import *
```


```python
# doms = ['d01','d02']
# root_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/*-*-*'
# root_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/*-*-*'
# path_out = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/log_pol'

# run_name = 'run_2019-06-05_18-42-11_'
# paths = glob.glob(root_path)
# paths.sort()
```


```python
# fo_base_dic  = dict(
# # dom = 'd01',
# # folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
# folder_path_out = path_out,
# run_name= run_name,
# )
```


```python
# for p in paths:
#     for d in doms:
#         print('starting',d,p)
#         new_dic = dict(dom=d,folder_path=p)
#         fo_dic = {**fo_base_dic,**new_dic}
        
#         try:
#             fo = FO.FLEXOUT(**fo_dic)
#             fo.export_log_polar_coords()
#             print('done',d,p)
#         except:
#             print('failed when',d,p)
```


```python
fo_dic = dict(
folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
dom = 'd02',
folder_path_out = '/Volumes/mbProD/Downloads/flex_out/log_pol',
run_name = 'run_2019-06-02_20-42-05_',
)
```


```python
self = FO.FLEXOUT(**fo_dic)
```

    /Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10/*header_*d02*
    /Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10/header_d02.nc
    /Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10/*flxout_*d02*
    ['/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10/flxout_d02_20171206_000000.nc']



```python
self.export_log_polar_coords(keep_z=True)
```

    done saving 2017-12-10 00:00:00
    done saving 2017-12-10 01:00:00
    done saving 2017-12-10 02:00:00
    done saving 2017-12-10 03:00:00
    done saving 2017-12-10 04:00:00
    done saving 2017-12-10 05:00:00
    done saving 2017-12-10 06:00:00
    done saving 2017-12-10 07:00:00
    done saving 2017-12-10 08:00:00
    done saving 2017-12-10 09:00:00
    done saving 2017-12-10 10:00:00
    done saving 2017-12-10 11:00:00
    done saving 2017-12-10 12:00:00
    done saving 2017-12-10 13:00:00
    done saving 2017-12-10 14:00:00
    done saving 2017-12-10 15:00:00
    done saving 2017-12-10 16:00:00
    done saving 2017-12-10 17:00:00
    done saving 2017-12-10 18:00:00
    done saving 2017-12-10 19:00:00
    done saving 2017-12-10 20:00:00
    done saving 2017-12-10 21:00:00
    done saving 2017-12-10 22:00:00
    done saving 2017-12-10 23:00:00
    save path /Volumes/mbProD/Downloads/flex_out/log_pol/run_2019-06-02_20-42-05_/d02_2017-12-10_00-00-00.nc
    length arr 24



```python

```


```python

```


```python

```


```python

```




    <xarray.Dataset>
    Dimensions:    (R_CENTER: 29, TH_CENTER: 36, ZTOP: 22, releases: 1)
    Coordinates:
      * R_CENTER   (R_CENTER) float64 0.006474 0.00775 0.009279 ... 1.0 1.197 1.433
      * TH_CENTER  (TH_CENTER) float64 0.08727 0.2618 0.4363 ... 5.847 6.021 6.196
      * releases   (releases) datetime64[ns] 2017-12-10T05:00:00
      * ZTOP       (ZTOP) float64 50.0 100.0 200.0 300.0 ... 9e+03 1e+04 2e+04 3e+04
        LAT        (R_CENTER, TH_CENTER) float64 -16.34 -16.34 ... -14.97 -14.92
        LON        (R_CENTER, TH_CENTER) float64 -68.12 -68.13 ... -66.75 -66.7
        LAT_00     (R_CENTER, TH_CENTER) float64 -16.34 -16.34 ... -15.12 -15.06
        LON_00     (R_CENTER, TH_CENTER) float64 -68.13 -68.13 ... -68.58 -68.36
        LAT_10     (R_CENTER, TH_CENTER) float64 -16.34 -16.34 ... -14.88 -14.81
        LON_10     (R_CENTER, TH_CENTER) float64 -68.13 -68.13 ... -68.67 -68.4
        LAT_11     (R_CENTER, TH_CENTER) float64 -16.34 -16.34 ... -14.81 -14.78
        LON_11     (R_CENTER, TH_CENTER) float64 -68.13 -68.13 ... -68.4 -68.13
        LAT_01     (R_CENTER, TH_CENTER) float64 -16.34 -16.34 ... -15.06 -15.04
        LON_01     (R_CENTER, TH_CENTER) float64 -68.13 -68.13 ... -68.36 -68.13
        GRIDAREA   (R_CENTER, TH_CENTER) float64 1.566e+04 1.566e+04 ... 7.731e+08
    Data variables:
        CONC       (R_CENTER, TH_CENTER, releases, ZTOP) float32 0.0 0.0 ... 0.0 0.0




```python
fa.compressed_netcdf_save(lp_ds,'/tmp/borrar1.nc')
```


```python

```
