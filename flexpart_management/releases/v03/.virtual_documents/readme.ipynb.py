import xarray as xr


ds = xr.open_dataset('./data/cluster_series_v3.nc')
ds


ds['conc_lab_nc18'].loc[
    {'z_column':'ALL','lab_nc18':'11_SR','normalized':0}
].plot()


ds['conc_lab_nc18'].loc[
    {'z_column':'ALL','lab_nc18':'11_SR','normalized':1}
].plot()


ds['conc_lab_nc18'].loc[
    {'z_column':'BL','lab_nc18':'11_SR','normalized':1}
].plot()


dall = ds['conc_lab_nc18'].loc[
    {'z_column':'ALL','lab_nc18':'11_SR','normalized':1}
]
dsurf = ds['conc_lab_nc18'].loc[
    {'z_column':'BL','lab_nc18':'11_SR','normalized':1}
]
(dsurf/dall).plot()


ds['age_lab_nc18'].loc[
    {'z_column':'ALL','lab_nc18':'11_SR',}
].plot()


ds['ZSL_all'].loc[
    {'z_column':'ALL'}
].plot()


ds['conc_all'].loc[
    {'z_column':'ALL','normalized':0}
].plot(ylim=(0,None))


ds['conc_all'].loc[
    {'z_column':'ALL','normalized':0,'releases':slice('2018-05-09','2018-05-11')}
].plot(ylim=(0,None))


get_ipython().getoutput("jupyter-nbconvert --to markdown readme.ipynb")



