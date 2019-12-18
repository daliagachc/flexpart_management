# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# %%
from useful_scit.imps import *
import funs_check

path = '/homeappl/home/aliagadi/wrk/' \
       'DONOTREMOVE/flexpart_management_data/' \
       'runs/run_2019-10-02_13-42-52_/'


# %%
funs_check.get_plot_save_rect(dom='d01',path = path , i_reduction=5000)

# %%
funs_check.get_plot_save_rect(dom='d02',path = path , i_reduction=5000)

# %%
