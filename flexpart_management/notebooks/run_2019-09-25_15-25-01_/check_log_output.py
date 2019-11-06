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

# %% [markdown]
# # Readme
# lets try to check the output from the flexpart running
# - make sure the run is finished for all 
# - check if there are any Diego comments
#

# %%
from useful_scit.imps import (
    pd,np,xr,za,mpl,plt,sns, pjoin, 
    os,glob,dt,sys,ucp,log, splot, crt,axsplot)
import re

# %%
path_flx = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-09-25_15-25-01_'

# %%
files = glob.glob(pjoin(path_flx,'*-*-*/output*.txt'))
files.sort()

# %%
PATH = 'PATH'
NAME = 'NAME'
DATE = 'DATE'
NPDATE = 'NPDATE'

# %%
df_files = pd.DataFrame(files,columns=[PATH])

# %%
df_files[NAME]=df_files.apply(lambda r: os.path.basename(os.path.dirname(r[PATH])), axis=1)
df_files[DATE]=pd.to_datetime(df_files[NAME])
df_files = df_files.set_index(DATE)

# %%
n_per_date = df_files.groupby(DATE).count()[NAME]
n_per_date.name = NPDATE
df_files = df_files.join(n_per_date)

# %%
df_files.reset_index().plot(DATE,NPDATE,style='.')

# %%
DIEGO_WARN = 'DIEGO_WARN'
DIEGO_WARN_PPLEV = 'DIEGO_WARN_PPLEV'
DONE = 'DONE'


# %%
def _check_diego_warning(row):
    with open(row[PATH],'r') as f:
        txt = f.read()
    res = re.findall('(?!Diego: pplev)Diego.+',txt)
    return len(res)

def _check_diego_warningPP(row):
    with open(row[PATH],'r') as f:
        txt = f.read()
    res = re.findall('Diego: pplev',txt)
    return len(res)

def _check_done(row):
    with open(row[PATH],'r') as f:
        txt = f.read()
    res = re.findall('CONGRATULATIONS: YOU HAVE SUCCESSFULLY COMPLETED A FLEXPART_WRF MODEL RUN!',txt)
    return len(res)


# %%
df_files[DIEGO_WARN]=df_files.apply(lambda r: _check_diego_warning(r), axis=1)

# %%
df_files[DIEGO_WARN_PPLEV]=df_files.apply(lambda r: _check_diego_warningPP(r), axis=1)

# %%
df_files[DONE]=df_files.apply(lambda r: _check_done(r), axis=1)

# %%
df_files.reset_index().plot(DATE,DIEGO_WARN,style='.')

# %%
df_files.reset_index().plot(DATE,DIEGO_WARN_PPLEV,style='.')

# %%
df_files.reset_index().plot(DATE,DONE,style='.')

# %%
# !conda env list

# %%
