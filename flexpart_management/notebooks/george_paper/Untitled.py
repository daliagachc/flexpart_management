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
from useful_scit.imps import *

# %%
lt = "local time"

# %%
path = '/Users/diego/flexpart_management/flexpart_management/releases/v03/data/cluster_series_v3.nc'

# %%
ds = xr.open_dataset(path)

# %%
c45_path = '/Users/diego/flexpart_management/flexpart_management/notebooks/george_paper/c45_timeseries.xlsx'
da = pd.read_excel(c45_path)

# %%
da[lt] = pd.to_datetime(da['Time_LT'],format='%d/%m/%Y %H:%M:%S')

# %%
da[lt]

# %%
da1 = da.set_index(lt).drop('Time_LT',axis=1)

# %%
da2 = da1.resample('h').mean()

# %%
da2.hist();
plt.gcf().tight_layout()

# %%

# %%

d = ds.loc[{'normalized':0}]
d[lt] = d['releases'] - pd.Timedelta(hours=3.5)
d = d.swap_dims({'releases':lt})

# %%
ts = slice('2018-01-10 10','2018-01-12 12')

# %%
d1 = d.loc[{lt:ts}]['conc_lab_nc18']

# %%
d1

# %%
d1.plot.line(x=lt,col='lab_nc18',hue='z_column',
#              sharey=False,
             col_wrap=4,aspect=2
            )

# %%
(d1/d['conc_lab_nc18'].mean([lt,'z_column'])).plot.line(x=lt,col='lab_nc18',hue='z_column',
#              sharey=False,
             col_wrap=4,aspect=2
            )

# %%
d.loc[{lt:ts}]['age_all'].plot(x=lt,hue='z_column')

# %%
d.loc[{lt:ts}]['conc_all'].plot(x=lt,col='z_column',sharey=False,ylim=(0,None))

# %%
d['lab_nc18']

# %%
SR = ['12_SR', '10_SR', '04_SR','07_SR','11_SR', '02_SR']
SM = ['03_SM', '12_SM' ,'06_SM', '08_SM']
d2 = d1.loc[{'lab_nc18':[*SR,*SM]}]
d2.sum('lab_nc18').plot(hue='z_column')

# %%
d2 = d1.loc[{'lab_nc18':[*SR]}]
d2.sum('lab_nc18').plot(hue='z_column')

# %%

# %%

# %%
