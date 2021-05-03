# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.7.0-rc1
#   kernelspec:
#     display_name: Python [conda env:b36]
#     language: python
#     name: conda-env-b36-py
# ---

# %%
from useful_scit.imps2.defs import *

# %%
ds = xr.open_dataset('/Volumes/mbProD/flexpart_management_data/'
                     'flexpart_management/tmp_data/new_log_pol_ds_asl_v01.nc')

# %%
ds1 = ds.rename({
    'R_CENTER':'x',
    'TH_CENTER':'y',
    'XLAT':'lat',
    'XLONG':'lon',
    'ZMID': 'z',
    'releases':'release_time'
})

# %%
dy = dict(
  standard_name = "projection_y_coordinate",
  long_name = "y-coordinate in projected coordinate system",
  units = "km",
  axis = "Y"
)

dx = dict(
  standard_name = "projection_x_coordinate",
  long_name = "x-coordinate in projected coordinate system",
  units = "km",
  axis = "X"
)

dlo = dict(
  standard_name = "longitude",
  long_name = "longitude",
  units = "degrees_east",
)

dla = dict(
  standard_name = "latitude",
  long_name = "latitude",
  units = "degrees_north",
)

dz = dict(
  axis = "Z",
  standard_name = "altitude",
  positive = "up",
  units = "m",
)

dt = dict(
#   units = "hours since 2021-02-18 00:00",
  standard_name = "time",
  long_name = "time",
  axis = "T",
)


atrs = dict(
    y   = dy,
    x   = dx,
    lon = dlo,
    lat = dla,
    z   = dz,
    release_time = dt
)

# %%
for l,v in atrs.items():
    ds1[l] = ds1[l].assign_attrs(v)

# %%
ds2 = ds1.transpose('release_time','z','y','x')
ds2 = ds2[{'release_time':[1000,1001]}]

# %%
ds2['z'].attrs={'units': 'hPa',
 'axis': 'Z',
 'standard_name': 'air_pressure',
 'positive': 'down'}

# %%
ds3 = ds2.reset_coords(drop=True)[['CONC']]

# %%
ds3['CONC'].coords

# %%

# %%
ds3.load()

# %%
ds2['TOPOGRAPHY']

# %%
ds3['topo']=xr.zeros_like(ds2['TOPOGRAPHY'].reset_coords(drop=True)) + ds2['TOPOGRAPHY'].values

# %%
ds3['Temperature'] = xr.zeros_like(ds3['CONC'])+ds3['CONC'].values

# %%
ds3['Temperature']=ds3['Temperature'].where(~ds3['Temperature'].isnull(),0)

# %%
ds3['Temperature'].max()

# %%
ds3['Temperature'].min()

# %%
ds4 = ds3[['Temperature','topo']]

# %%
ds4['topo']

# %%
ds4 = ds4.assign_coords({'lat':ds2['lat'].reset_coords(drop=True)})
ds4 = ds4.assign_coords({'lon':ds2['lon'].reset_coords(drop=True)})

# %%
ds4.to_netcdf('test12.nc',format='NETCDF3_CLASSIC')

# %%

# %%

# %%
ds3.to_netcdf('test6.nc')

# %%
ds2.load()

# %%
ds2['CONC'].attrs

# %%
ds2.to_netcdf('test_del1.nc')

# %%
ff = '/Volumes/Transcend/scratch/forecast_model.nc'

dm = xr.open_dataset(ff)
dm.attrs={}
dm = dm.drop('lambert_projection')

# %%
dm['Temperature'].attrs={}

# %%
dm['pressure'].attrs

# %%
dm.to_netcdf('ex3.nc')

# %%
dm['Temperature'].attrs

# %%
dm.reset_coords()

# %%
