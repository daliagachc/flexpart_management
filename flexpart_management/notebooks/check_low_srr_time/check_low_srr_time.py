# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import flexpart_management.notebooks.check_low_srr_time.check_low_srr_time_lfc as lfc
from flexpart_management.notebooks.check_low_srr_time.check_low_srr_time_lfc import *

# %%

path = '/tmp/fxp'
files = glob.glob(path+'/flxout*')
files.sort()
ds = xr.open_mfdataset(files,concat_dim='Time')
# %%
ds1 = ds['CONC'][{'releases':0}].sum(['bottom_top','ageclass'])
ds1.load()
# %%

# %%
ds1[{'Time':slice(0,96,5)}].plot(col='Time',col_wrap=5,vmax=5)
plt.show()
# %%
ds1.sum(['south_north','west_east']).plot()
plt.show()
# %%
ds1.sum()
# %%
# %%
# %%
# %%
# %%
# %%
# %%


