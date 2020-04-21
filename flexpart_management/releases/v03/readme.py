# ---
# jupyter:
#   jupytext:
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

# %% pycharm={"is_executing": false}
import xarray as xr

# %% [markdown] pycharm={"name": "#%%\n", "is_executing": false} jupyter={"outputs_hidden": false}
# This notebook contains information regarding the release v03 of the timeseries for the cluster analysis performed at CHC station during the SALTENA campaign
#
#
# This is release v03 of the clusters for CHC for the Saltena campaign
# - the data folder contains the following datasets:
#   - description_cluster_series_v3.csv  
#   description of all dimensions variables contained in cluster_series_v3.nc
#   - cluster_series_v3.nc  
#   dataset for the cluster timeseries and pathway series
#   - pol6.kml  
#   google earth polygones for the 6 pathways
#   - pol18.kml  
#   google earth polygones for the 18 clusters
#
#

# %% [markdown]
# open the dataset

# %%
ds = xr.open_dataset('./data/cluster_series_v3.nc')
ds

# %% [markdown]
# plot all column not normalized SRR timeseries for cluster '11_SR'

# %%
ds['conc_lab_nc18'].loc[
    {'z_column':'ALL','lab_nc18':'11_SR','normalized':0}
].plot()

# %% [markdown]
# plot all column normalized SRR timeseries for cluster '11_SR'

# %%
ds['conc_lab_nc18'].loc[
    {'z_column':'ALL','lab_nc18':'11_SR','normalized':1}
].plot()

# %% [markdown]
# plot surface normalized SRR timeseries for cluster '11_SR'

# %%
ds['conc_lab_nc18'].loc[
    {'z_column':'SURF','lab_nc18':'11_SR','normalized':1}
].plot()

# %% [markdown]
# plot ratio column normalized SRR timeseries for cluster '11_SR'

# %%
dall = ds['conc_lab_nc18'].loc[
    {'z_column':'ALL','lab_nc18':'11_SR','normalized':1}
]
dsurf = ds['conc_lab_nc18'].loc[
    {'z_column':'SURF','lab_nc18':'11_SR','normalized':1}
]
(dsurf/dall).plot()

# %% [markdown]
# plot age [hours] all column timeseries for cluster '11_SR'

# %%
ds['age_lab_nc18'].loc[
    {'z_column':'ALL','lab_nc18':'11_SR',}
].plot()

# %% [markdown]
# plot all column mean height above sea level timeseries for all domain

# %%
ds['ZSL_all'].loc[
    {'z_column':'ALL'}
].plot()

# %% [markdown]
# plot all column not normalized SRR timeseries for all domain
# - Notice that the SRR is not consants (as it should be) since there are times where fast moving particles leave the modeling domain before 4 days have passed. 

# %%
ds['conc_all'].loc[
    {'z_column':'ALL','normalized':0}
].plot(ylim=(0,None))

# %%
ds['conc_all'].loc[
    {'z_column':'ALL','normalized':0,'releases':slice('2018-05-09','2018-05-11')}
].plot(ylim=(0,None))

# %%
    
