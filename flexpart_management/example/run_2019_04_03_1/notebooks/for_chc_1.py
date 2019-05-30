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
path = '../data_out/for_chc_1/'
path = '../data_out/for_chc_1_mpi/'

# %%


# %%
files = glob.glob(path+'flxout_d01*')
files.sort()
files = files

# %%


# %%
ds = [xr.open_dataset(f1) for f1 in files]

# %%
dc = xr.concat(ds,dim='Time')

# %%
d11 = dc.CONC.sum(dim=['Time','bottom_top'])


# %%
d11.plot(x='west_east',y='south_north',col='ageclass')

# %%
_t = d11.isel(west_east=slice(170,230),south_north=slice(110,150))
_t.plot(x='west_east',y='south_north',col='ageclass',vmin=0,vmax=5)

# %%



# %%
d11 = dc.CONC.sum(dim=['Time','west_east'])

# %%
d11.plot(x='south_north',y='bottom_top',col='ageclass')

# %%
_t = d11.isel(south_north=slice(110,150))
_t.plot(x='south_north',y='bottom_top',col='ageclass',vmin=0,vmax=50)

# %%
h1 = xr.open_dataset('../data_out/bac_chc_1/header_d01.nc')


# %%
dc.CONC.sum()


# %%



# %%
dc1 = dc.isel(ageclass=1).CONC.sum(dim=['bottom_top']).isel(west_east=slice(170,230),south_north=slice(110,150))


# %%
dc1.plot(x='west_east',y='south_north',col='Time',vmin=0,vmax=1,col_wrap=12)


# %%
dc.CONC.sum(dim=['ageclass', 'bottom_top', 'south_north', 'west_east']).plot()


# %%
dc.Times


# %%



# %%



# %%



# %%



# %%



# %%



# %%



# %%



# %%




# %%


# %%


# %%


# %%


# %%


# %%

