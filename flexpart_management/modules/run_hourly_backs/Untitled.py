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

# %%
from useful_scit.imps import *
import datetime as dt

# %%
date_start_release = dt.datetime(2017,12,7,0,0)


# %%
def format_date(in_date):
    out_date=in_date.strftime('%Y%m%d %H%M%S')
    return out_date

# %%
