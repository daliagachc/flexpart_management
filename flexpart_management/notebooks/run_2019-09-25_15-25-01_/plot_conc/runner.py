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
# !srun --mem=4000 -t30 -c1 -n1 -ptest python3 -u ./run_me.py \
# /homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-09-25_15-25-01_/2018-01-01/ \
# /homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-09-25_15-25-01_/check_plots \
# 1

# %%
from useful_scit.imps import (pd,np,xr,za,mpl,plt,sns, pjoin, os,glob,dt,
    sys,ucp,log, splot, crt,axsplot)

# %%
PATH_IN = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/'+\
'runs/run_2019-09-25_15-25-01_/*-*-*'
PATH_OUT = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-09-25_15-25-01_/check_plots'

# %%
DOMS = [1,2]

# %%
paths = glob.glob(PATH_IN)
paths.sort()

# %%
ds = pd.Series(paths)

# %%
ds.str.match('.*\d')

# %%
for path in paths:
    for dom in DOMS:
        print(path)
        print(dom)
        
        

# %%
