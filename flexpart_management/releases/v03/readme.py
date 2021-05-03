# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] pycharm={"name": "#%%\n", "is_executing": false} jupyter={"outputs_hidden": false}
# This notebook contains information regarding the release v03 of the timeseries for the cluster analysis performed at CHC station during the SALTENA campaign
# ## info
#
# - the data folder contains the following files:
#   - description_cluster_series_v3.csv  
#   description of all dimensions variables contained in cluster_series_v3.nc
#   - cluster_series_v3.nc  
#   dataset for the cluster timeseries and pathway series
#   - pol6.kml  
#   google earth polygones for the 6 pathways
#   - pol18.kml  
#   google earth polygones for the 18 clusters
#
#   - csv folder  
#     - a csv "version" of the nc (netCDF) file.
#     - for metadata please refer to the description_cluster_series_v3.csv file.
#     
#     
# ## donwload
#
# download all files from this release in a zip document:
# - [../v03.zip](../v03.zip)
#
#     
# ## below are some examples on how to use the dataset

# %% [markdown]
# open the dataset

# %% pycharm={"is_executing": false}
import xarray as xr

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
# plot BL normalized SRR timeseries for cluster '11_SR'

# %%
ds['conc_lab_nc18'].loc[
    {'z_column':'BL','lab_nc18':'11_SR','normalized':1}
].plot()

# %% [markdown]
# plot ratio column normalized SRR timeseries for cluster '11_SR'

# %%
dall = ds['conc_lab_nc18'].loc[
    {'z_column':'ALL','lab_nc18':'11_SR','normalized':1}
]
dsurf = ds['conc_lab_nc18'].loc[
    {'z_column':'BL','lab_nc18':'11_SR','normalized':1}
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

# %% tags=[]
# !jupyter-nbconvert --to markdown readme.ipynb


# %% tags=[]
# !zip -vr ../v03.zip ../v03/ -x "*.DS_Store"

# %%
