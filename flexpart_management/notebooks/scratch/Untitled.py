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
import xarray as xr
import cartopy as cy
import numpy as np

# %%
# open dataset 
ds = xr.open_dataset('/Volumes/mbProD/flexpart_management_data/flexpart_management/tmp_data/new_log_pol_ds_asl_v01.nc')
ds1 = xr.open_dataset('/Volumes/mbProD/flexpart_management_data/flexpart_management/tmp_data/new_log_pol_ds_agl.nc')

# %%
dss = ds.sum('ZMID')

# %%
d1 = dss['CONC'].values.flatten()
d1 = d1[d1>1]

# %%
xl = np.geomspace(1,1e4)

# %%
plt.hist(d1,bins=xl)
ax = plt.gca()
ax.set_xscale('log')
# ax.set_yscale('log')

# %%
ds.sum('ZMID').quantile([.5,.999])['CONC'].values

# %%
ds.sum('TH_CENTER').quantile([.5,.999])['CONC'].values

# %%
ds.sum('R_CENTER').quantile([.5,.999])['CONC'].values

# %%
import warnings
warnings.simplefilter("ignore", UserWarning)

# %%
dd=ds['CONC'].sum(['ZMID','releases'])

# %%
dd.plot(
    x='XLONG',y='XLAT',subplot_kws={'projection':cy.crs.PlateCarree()},
    cmap='Reds'
)
ax = plt.gca()
ax.add_feature(cy.feature.BORDERS)
ax.add_feature(cy.feature.COASTLINE);

# %%
dd=ds['CONC'].sum(['TH_CENTER','releases'])
dd.plot(
    x='R_CENTER',y='ZMID',
#     subplot_kws={'projection':cy.crs.PlateCarree()},
    cmap='Reds'
)

# %%
dd=ds1['CONC'].sum(['TH_CENTER','releases'])
dd.plot(
    x='R_CENTER',y='ZMID',
#     subplot_kws={'projection':cy.crs.PlateCarree()},
    cmap='Reds'
)

# %%
warnings.simplefilter('ignore',FutureWarning)

# %%
dd=ds['CONC'].sum(['R_CENTER','releases'])
dd = dd.roll({'TH_CENTER':18})

tt = np.mod(
    dd['TH_CENTER'] + np.pi,
    2*np.pi
) - np.pi
tt *=180/np.pi

dd = dd.assign_coords(tt=tt)

dd.plot(
    x='tt',y='ZMID',
#     subplot_kws={'projection':cy.crs.PlateCarree()},
    cmap='Reds'
)

# %%
dd=ds1['CONC'].sum(['R_CENTER','releases'])
dd = dd.roll({'TH_CENTER':18})

tt = np.mod(
    dd['TH_CENTER'] + np.pi,
    2*np.pi
) - np.pi
tt *=180/np.pi

dd = dd.assign_coords(North=tt)

dd.plot(
    x='North',y='ZMID',
#     subplot_kws={'projection':cy.crs.PlateCarree()},
    cmap='Reds'
)

# %%
# check dataset
ds

# %%
days=np.unique(ds['releases'].dt.strftime('%Y-%m-%d'))

# %%
day = days[36]
day

# %%
# select the day to plot



# select this day from the dataset
dday = ds.loc[{'releases':day}]

# %%
# select the variable CONC 
con = dday['CONC']

# sum over the vertical dimensions
consum = con.sum('ZMID')

#plot
p = consum.plot(
    x='XLONG',y='XLAT',
    #split the plot along the release dimension
    col='releases',
    #force con have a maximum of 6 element per column
    col_wrap=6,
    #use a sym log norm colorbar
    norm=mpl.colors.SymLogNorm(linthresh=1,vmin=500,vmax=10000),
    
    #projection for the map.
    subplot_kws={'projection':cy.crs.PlateCarree()},
    
    # use reds as the color 
    cmap = 'Reds',
    
    # image size
    figsize = (25,15)
    )

for ax in p.axes.flat:
    ax.coastlines()
    ax.add_feature(cy.feature.BORDERS)
#     ax.gridlines()
#     ax.borders()

# %%
# vertical plots. i.e. summing along the TH dimension. distance [dis] is in km
dday = ds.loc[{'releases':day}]
con = dday['CONC']
consum = con.sum('TH_CENTER')
condis = consum.assign_coords({'dis':consum['R_CENTER']*100})
condis.plot(
    x='dis',y='ZMID',
    col='releases',col_wrap=6,
    norm=mpl.colors.SymLogNorm(linthresh=1,vmin=500,vmax=10000),
    cmap = 'Reds',
    figsize = (25,10),
    xscale='log'
    )


# %%
# vertical plots. i.e. summing along the TH dimension. distance [dis] is in km
dday = ds1.loc[{'releases':day}]
con = dday['CONC']
consum = con.sum('TH_CENTER')
condis = consum.assign_coords({'dis':consum['R_CENTER']*100})
condis.plot(
    x='dis',y='ZMID',
    col='releases',col_wrap=6,
    norm=mpl.colors.SymLogNorm(linthresh=1,vmin=500,vmax=10000),
    cmap = 'Reds',
    figsize = (25,10),
    xscale='log'
    )

# %%
# vertical plots. i.e. summing along the TH dimension. distance [dis] is in km
dday = ds.loc[{'releases':day}]
con = dday['CONC']
consum = con.sum('R_CENTER').roll({'TH_CENTER':18})

tt = np.mod(
    consum['TH_CENTER'] + np.pi,
    2*np.pi
) - np.pi
tt *=180/np.pi

condis = consum.assign_coords(North=tt)
condis.plot(
    x='North',y='ZMID',
    col='releases',col_wrap=6,
    norm=mpl.colors.SymLogNorm(linthresh=1,vmin=500,vmax=10000),
    cmap = 'Reds',
    figsize = (25,10)
    )

# %%
# vertical plots. i.e. summing along the TH dimension. distance [dis] is in km

dday = ds1.loc[{'releases':day}]
con = dday['CONC']
consum = con.sum('R_CENTER').roll({'TH_CENTER':18})

tt = np.mod(
    consum['TH_CENTER'] + np.pi,
    2*np.pi
) - np.pi
tt *=180/np.pi

condis = consum.assign_coords(North=tt)
condis.plot(
    x='North',y='ZMID',
    col='releases',col_wrap=6,
    norm=mpl.colors.SymLogNorm(linthresh=1,vmin=500,vmax=10000),
    cmap = 'Reds',
    figsize = (25,10)
    )
