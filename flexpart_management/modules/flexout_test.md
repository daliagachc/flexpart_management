```python
%load_ext autoreload
%autoreload 2
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload



```python
import flexpart_management.modules.FLEXOUT as FO
import flexpart_management.modules.flx_array as fa
```


```python
fo_dic  = dict(
dom = 'd02',
folder_path = '/Volumes/mbProD/Downloads/failed_flx/2017-12-11',
folder_path_out = '/Volumes/mbProD/Downloads/flex_out/log_pol',
run_name= 'run_2019-06-02_20-42-05_',
)
```


```python

fo = FO.FLEXOUT(**fo_dic)
```

    /Volumes/mbProD/Downloads/failed_flx/2017-12-11/*header_*d02*
    /Volumes/mbProD/Downloads/failed_flx/2017-12-11/header_d02.nc
    /Volumes/mbProD/Downloads/failed_flx/2017-12-11/*flxout_*d02*
    ['/Volumes/mbProD/Downloads/failed_flx/2017-12-11/flxout_d02_20171207_000000.nc']
    cant open /Volumes/mbProD/Downloads/failed_flx/2017-12-11/flxout_d02_20171208_010000.nc
    cant open /Volumes/mbProD/Downloads/failed_flx/2017-12-11/flxout_d02_20171211_230000.nc



```python
fo.export_log_polar_coords()
```

    error in 2017-12-11 05:00:00
    error in 2017-12-11 06:00:00
    error in 2017-12-11 07:00:00
    error in 2017-12-11 08:00:00
    error in 2017-12-11 09:00:00
    error in 2017-12-11 10:00:00
    error in 2017-12-11 11:00:00
    error in 2017-12-11 12:00:00
    error in 2017-12-11 13:00:00
    error in 2017-12-11 14:00:00
    error in 2017-12-11 15:00:00
    error in 2017-12-11 16:00:00
    error in 2017-12-11 17:00:00
    error in 2017-12-11 18:00:00
    error in 2017-12-11 19:00:00
    error in 2017-12-11 20:00:00
    error in 2017-12-11 21:00:00
    error in 2017-12-11 22:00:00
    error in 2017-12-11 23:00:00





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
      <th>releases</th>
      <th>release_name</th>
      <th>release_path</th>
    </tr>
    <tr>
      <th>releases</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-12-11 00:00:00</th>
      <td>2017-12-11 00:00:00</td>
      <td>d02_2017-12-11_00-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 01:00:00</th>
      <td>2017-12-11 01:00:00</td>
      <td>d02_2017-12-11_01-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 02:00:00</th>
      <td>2017-12-11 02:00:00</td>
      <td>d02_2017-12-11_02-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 03:00:00</th>
      <td>2017-12-11 03:00:00</td>
      <td>d02_2017-12-11_03-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 04:00:00</th>
      <td>2017-12-11 04:00:00</td>
      <td>d02_2017-12-11_04-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 05:00:00</th>
      <td>2017-12-11 05:00:00</td>
      <td>d02_2017-12-11_05-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 06:00:00</th>
      <td>2017-12-11 06:00:00</td>
      <td>d02_2017-12-11_06-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 07:00:00</th>
      <td>2017-12-11 07:00:00</td>
      <td>d02_2017-12-11_07-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 08:00:00</th>
      <td>2017-12-11 08:00:00</td>
      <td>d02_2017-12-11_08-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 09:00:00</th>
      <td>2017-12-11 09:00:00</td>
      <td>d02_2017-12-11_09-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 10:00:00</th>
      <td>2017-12-11 10:00:00</td>
      <td>d02_2017-12-11_10-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 11:00:00</th>
      <td>2017-12-11 11:00:00</td>
      <td>d02_2017-12-11_11-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 12:00:00</th>
      <td>2017-12-11 12:00:00</td>
      <td>d02_2017-12-11_12-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 13:00:00</th>
      <td>2017-12-11 13:00:00</td>
      <td>d02_2017-12-11_13-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 14:00:00</th>
      <td>2017-12-11 14:00:00</td>
      <td>d02_2017-12-11_14-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 15:00:00</th>
      <td>2017-12-11 15:00:00</td>
      <td>d02_2017-12-11_15-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 16:00:00</th>
      <td>2017-12-11 16:00:00</td>
      <td>d02_2017-12-11_16-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 17:00:00</th>
      <td>2017-12-11 17:00:00</td>
      <td>d02_2017-12-11_17-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 18:00:00</th>
      <td>2017-12-11 18:00:00</td>
      <td>d02_2017-12-11_18-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 19:00:00</th>
      <td>2017-12-11 19:00:00</td>
      <td>d02_2017-12-11_19-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 20:00:00</th>
      <td>2017-12-11 20:00:00</td>
      <td>d02_2017-12-11_20-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 21:00:00</th>
      <td>2017-12-11 21:00:00</td>
      <td>d02_2017-12-11_21-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 22:00:00</th>
      <td>2017-12-11 22:00:00</td>
      <td>d02_2017-12-11_22-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
    <tr>
      <th>2017-12-11 23:00:00</th>
      <td>2017-12-11 23:00:00</td>
      <td>d02_2017-12-11_23-00-00.nc</td>
      <td>/Volumes/mbProD/Downloads/flex_out/log_pol/run...</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
