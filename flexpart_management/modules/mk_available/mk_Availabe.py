# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import os
import pandas as pd
import xarray as xr
import datetime as dt

# %% [markdown]
# lets create the dataframe for the files. it should include:
# - name
# - datetime 
# - path

# %% [markdown]
# now lets get the dates from one file 

# %%
HEAD = '''XXXXXX EMPTY LINES XXXXXXXXX
XXXXXX EMPTY LINES XXXXXXXX
YYYYMMDD HHMMSS   name of the file(up to 80 characters)'''


# %%
def get_times(path):
    xds = xr.open_dataset(path)
    xds.close()
    times = xds.XTIME.to_series()
    times = pd.DatetimeIndex(times)
    times = times.strftime('%Y%m%d %H%M%S')
    times = times.tolist()
    return times


# %%
def row_to_strings(row):
    strs = []
    for t in row['times']:
        st = "{}      '{}'      ' '"
        lin = st.format(t, row['name'])
        strs.append(lin)
    return '\n'.join(strs)


# %%
def get_master_string(df):
    vals = df['strings'].values
    strs = '\n'.join(vals)
    strs = HEAD + '\n' + strs
    return strs


def export_file(path, string):
    file = open(path, 'w')
    file.write(string)
    file.close()


# %%


def create_avail_file(path_files, ex_path, prefix, d1=False, d2=False):
    """

    Parameters
    ----------
    path_files: str
        source of wrf files
    ex_path: str
        path of the output available file
    prefix: str
        start of wrf files to be consifered
    d1: dt.datetime
        start of simulation (no needed)
    d2: dt.datetime
        end of sumulation (not needed)

    Returns
    -------
    int
        0 if sucess
    """
    df = get_files_df(path_files, prefix, d1, d2)
    string = get_master_string(df)
    export_file(ex_path, string)
    return 0


def get_files_df(path_files, prefix,
                 d1: dt.datetime = False,
                 d2: dt.datetime = False,
                 ):
    files = os.listdir(path_files)
    df = pd.DataFrame(files, columns=['name'])
    _boo = df.name.str.startswith(prefix)
    df = df.loc[_boo]
    df['dt'] = df.name.str[-19:]
    df['dt'] = pd.to_datetime(df.dt, format='%Y-%m-%d_%H:%M:%S')
    df['path'] = df.name.apply(lambda n: os.path.join(path_files, n))
    df = df.sort_values('dt')
    df = df.reset_index(drop=True).reset_index()
    df = df.rename(index=str, columns={'index': 'i'})
    df = df.set_index('dt')
    if d1:
        i0 = df.i[df.index >= d1][0]
        if i0 > 0:
            i0 = i0 - 1
        df = df.iloc[i0:]
    if d2:
        i1 = df.i[df.index <= d2][-1]
        if i1 < df.i[-1]:
            i1 = i1 + 1
        df = df.iloc[:i1]

    times = df.path.apply(lambda p: get_times(p))
    df['times'] = times
    strings = df.apply(lambda row: row_to_strings(row), axis=1)
    df['strings'] = strings
    return df


# %%
def is_interactive():
    import __main__ as main
    return not hasattr(main, '__file__')


# %%
print('interactive', is_interactive())

# %%
if __name__ == "__main__" and is_interactive() == False:
    import sys

    print('starting program')
    path_files = sys.argv[1]
    prefix = sys.argv[2]
    ex_path = sys.argv[3]
    create_avail_file(path_files, ex_path, prefix)
