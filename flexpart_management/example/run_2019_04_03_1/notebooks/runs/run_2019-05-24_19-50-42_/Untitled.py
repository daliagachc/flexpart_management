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
path = '/Volumes/mbProD/Downloads/flex_out/run_2019-05-24_17-45-51_/'
# path = '/Volumes/mbProD/Downloads/flex_out/run_2019-05-24_19-44-48_/'
path = '/Volumes/mbProD/Downloads/flex_out/run_2019-05-24_19-50-42_/'


# %%


# %%
files = glob.glob(path+'flxout_d02*')
files.sort()
files = files

# %%
files


# %%
ds = [xr.open_dataset(f1) for f1 in files]

# %%
dc = xr.concat(ds,dim='Time')

# %%
dc.CONC.sum(dim=['Time','bottom_top']).isel(ageclass=1,south_north=slice(360,480),west_east=slice(200,300)).plot(vmax=0.0000001)

# %%
dc.CONC.sum(dim = ['ageclass', 'species', 'bottom_top', 'south_north', 'west_east']).plot()

# %%
