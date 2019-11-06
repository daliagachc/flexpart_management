# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import (
    pd,np,xr,za,mpl,plt,sns, pjoin, os,glob,dt,sys,ucp,log, splot, crt) 
import re

# %%
path =\
    '/homeappl/home/aliagadi/wrk/DONOTREMOVE/'+\
    'flexpart_management_data/runs/run_2019-08-18_18-46-19_'

# %%
files = glob.glob(path+'/*/output*txt')
files.sort()

# %%
fdf = pd.DataFrame(files,columns=['path'])

# %%
_p1 = fdf.iloc[0]['path']

# %%
_str = ''
for i,r in fdf.iterrows():
    _p1 = r['path']
    with open(_p1,'r') as f:
        text = f.read()

    _iter=re.finditer('\nfile\ =.{5,1000}?Diego.{0,80}',text,flags=re.S)
    for i in _iter:
        _str += text[i.start():i.end()]

# %%
cases = re.findall('\d+?-\d+?-\d+?_\d+?:00:00',_str)

# %%
cas = 'cases'
dtime = 'dtime'
cdf = pd.DataFrame(cases,columns=[cas])
cdf[dtime]=pd.to_datetime(cdf[cas].str.replace('_',' '))
cdf = cdf[~cdf.duplicated(subset=cas)].reset_index(drop=True)
cdf['y']=1

# %%
path = '/proj/atm/saltena/runs/run_2019_05_15/wrf/wrfout_d04*'

# %%
_wrf_files = glob.glob(path)
_wrf_files.sort()

# %%
path='path'
wrf_df = pd.DataFrame(_wrf_files,columns=['path'])

# %%
mod_time = 'mod_time'
wrf_df[mod_time]=wrf_df.apply(lambda r: os.path.getmtime(r['path']),axis=1)
wrf_df[mod_time]=pd.to_datetime(wrf_df[mod_time],unit='s')

# %%
_mt = wrf_df[mod_time]

# %%
_res = (_mt-_mt.shift(1)).apply(lambda x: x.total_seconds()/3600)
time_delta = 'time_delta [hours]'
wrf_df[time_delta] = _res

# %%
_p = wrf_df[path]
file_time = 'file_model_time'
_p = _p.str.slice(-19,None)
_p = _p.str.replace('_',' ')
_p = pd.to_datetime(_p)
wrf_df[file_time]=_p

# %%
f,ax=splot()
# cdf.plot(x=dtime,y='y',style='o',ax=ax)
# ax.vlines(cdf.set_index(dtime),.1,1e5)
# f,ax=splot()
ax.vlines(cdf.set_index(dtime).index,.1,1e5,label='k==nvz')

print(ax.get_xlim())
ucp.set_dpi(200)
ax.plot_date(wrf_df[file_time],wrf_df[time_delta],ls='-',fmt=',',
#                  figsize=(10,3),
             label = 'd time'
                )
ax.set_yscale('log')
ax.legend()
f.autofmt_xdate()


# %%
# !jupyter-nbconvert --to markdown check_ric_not_found_files.ipynb

# %%
