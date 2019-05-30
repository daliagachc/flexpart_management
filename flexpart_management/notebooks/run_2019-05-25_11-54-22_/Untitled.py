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
path = '/Volumes/mbProD/Downloads/flex_out/run_2019-05-25_23-19-34_'

# %%
head = os.path.join(path,'header*d01*')
head = glob.glob(head)[0]
head = xr.open_dataset(head)

# %%
files = os.path.join(path,'flxout_d01*')
files = glob.glob(files)
files.sort()
# files = [xr.open_dataset(f) for f in files[10:]]
ff = []
for f in files:
    try: ff.append(xr.open_dataset(f))
    except: pass

# %%
ds = xr.concat(ff,dim='Time')
ds = ds.assign_coords(ZTOP=head.ZTOP)
ds = ds.assign_coords(XLAT=head.XLAT)
ds = ds.assign_coords(XLONG=head.XLONG)

# %%
ds.CONC.isel(ageclass=1).mean(dim=['Time','bottom_top']).plot(x='XLONG',y='XLAT',vmax=.01)

# %%
ds['CONC'].isel(ageclass=1).mean(dim=['Time','south_north']).plot(x='west_east',y='ZTOP',vmax=.01)

# %%
ds['CONC'].isel(ageclass=1).mean(dim=['Time','west_east']).plot(x='south_north',y='ZTOP',vmax=.01)

# %%
ds.CONC.isel(ageclass=1).sum(dim=['west_east','south_north','bottom_top']).plot()

# %%
