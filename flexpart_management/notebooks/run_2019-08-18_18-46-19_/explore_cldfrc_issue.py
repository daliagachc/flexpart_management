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
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FLP
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

plt.style.use('ggplot')

from IPython.display import set_matplotlib_formats
set_matplotlib_formats('png')

# %%
import wrf

# %%
file_path = '/private/tmp/wrfout_d04_2018-04-08_15:00:00'

# %%
ds = xr.open_dataset(file_path)

# %%
cf = 'CLDFRA'
bt = 'bottom_top'
sn = 'south_north'
we = 'west_east'
d1 = ds[cf].isel(Time=1)
d1

# %%
d1.mean(bt).plot();

# %%
d1.std(bt).plot();

# %%
d2 = d1.stack(com=(sn,we))

# %%
d2

# %%
d2[:,::1000].plot.line(hue='com',add_legend=False);

# %%
ds['SWDOWN']

# %%
ds['SWDOWN'][0].plot(x='XLONG',y='XLAT')

# %%

# %%
