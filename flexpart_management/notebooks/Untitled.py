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
from useful_scit.imps import *

# %%
path = '/Users/diego/Downloads/error/flxout_d02_20171224_080000.nc'

# %%

# %%
# %load_ext autoreload
# %autoreload 2

# %%
import useful_scit.util.list_manipulation as lm

# %%
l1,n1 = [1,2,3,4],100

# %%
lm.partition(l1,n1)

# %%
lm.partition(l1,n1,up2=True)

# %%
