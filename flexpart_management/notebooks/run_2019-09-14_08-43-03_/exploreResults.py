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
from useful_scit.imps import (pd,np,xr,za,mpl,plt,sns, pjoin, os,glob,dt,sys,
                              ucp,log, splot, crt)
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co

from exploreResults_funs import plot_multiple_foot_prints

mpl.rcParams['figure.dpi'] = 100
# # %matplotlib notebook


# %%
log.ger.setLevel(log.log.INFO)

# %%
dir_path = \
    '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/'+\
    'run_2019-09-14_08-43-03_/2018-01-01'

# %%

# %%
DD = co.D2
nds = fa.euristic_import_flexpart(dir_path, DD)

# %%
plot_multiple_foot_prints(nds)


# %%
DD = co.D1
nds = fa.euristic_import_flexpart(dir_path, DD)

# %%
plot_multiple_foot_prints(nds, pad_chc=2)

# %%
import wrf

wrf.getvar()