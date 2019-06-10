# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

# %%
from useful_scit.imps import *

# %%
import flexpart_management.modules.FlxOutCheckAlt as FCA
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

# %%
path_pat = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/*-*-*/'
path_pat = \
    '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/*-*-*'
dom = 'd01'
out_path ='./z_ds'+dom+'.nc'

self = FCA.FlxOutCheckAlt(path_pat,dom=dom,out_z_path=out_path)
self.save_z_sum_ds()


path_pat = \
    '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/*-*-*'
dom = 'd02'
out_path ='./z_ds'+dom+'.nc'

self = FCA.FlxOutCheckAlt(path_pat,dom=dom,out_z_path=out_path)
self.save_z_sum_ds()

# %%


# %%
dim2sum

# %%
