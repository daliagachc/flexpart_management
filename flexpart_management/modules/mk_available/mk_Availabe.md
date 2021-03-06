```python
import os
import pandas as pd
import xarray as xr
```

lets create the dataframe for the files. it should include:
- name
- datetime 
- path

now lets get the dates from one file 


```python
HEAD = '''XXXXXX EMPTY LINES XXXXXXXXX
XXXXXX EMPTY LINES XXXXXXXX
YYYYMMDD HHMMSS   name of the file(up to 80 characters)'''
```


```python
def get_times(path):
    xds = xr.open_dataset(path)
    xds.close()
    times = xds.XTIME.to_series()
    times = pd.DatetimeIndex(times)
    times = times.strftime('%Y%m%d %H%M%S') 
    times = times.tolist()
    return times
```


```python
def row_to_strings(row):
    strs = []
    for t in row['times']:
        st = "{}      '{}'      ' '"
        lin = st.format(t,row['name'])
        strs.append(lin)
    return '\n'.join(strs) 
   
```


```python
def get_master_string(df):
    vals = df['strings'].values
    strs = '\n'.join(vals)
    strs = HEAD+'\n'+strs
    return strs

def export_file(path,string):
    file = open(path,'w')
    file.write(string)
    file.close()
```


```python
def create_avail_file(path_files, ex_path, prefix):
    files = os.listdir(path_files)
    df = pd.DataFrame(files,columns=['name'])
    _boo = df.name.str.startswith(prefix)
    df = df.loc[_boo]
    df['dt'] = df.name.str[-19:]
    df['dt'] = pd.to_datetime(df.dt,format='%Y-%m-%d_%H:%M:%S')
    df['path'] = df.name.apply(lambda n: os.path.join(path_files,n))
    df = df.sort_values('dt')
    df = df.set_index('dt')

    times = df.path.apply(lambda p: get_times(p))
    df['times'] = times

    strings = df.apply(lambda row: row_to_strings(row),axis=1) 
    df['strings'] = strings

    string = get_master_string(df)
    export_file(ex_path,string)
    return 0 
```


```python
def is_interactive():
    import __main__ as main
    return not hasattr(main, '__file__')
```


```python
print('interactive',is_interactive())
```




    True




```python
if __name__ == "__main__" and is_interactive() == False:
    import sys
    print('starting program')
    path_files=sys.argv[1]
    prefix = sys.argv[2]
    ex_path = sys.argv[3]
    create_avail_file(path_files, ex_path, prefix)
    
```
