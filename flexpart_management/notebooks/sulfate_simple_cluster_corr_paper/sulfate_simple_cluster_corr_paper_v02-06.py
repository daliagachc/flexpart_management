# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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
import sys
sys.path.insert(0,'../../../')
import flexpart_management.notebooks.sulfate_simple_cluster_corr_paper. \
    sulfate_simple_cluster_corr_paper_lfc as lfc
from flexpart_management.notebooks.sulfate_simple_cluster_corr_paper. \
    sulfate_simple_cluster_corr_paper_lfc import *

# %%
sul = 'Sulfate'
lab_name = 'lab_name'
# %%
acsm = lfc.get_acsm_data()
# %%
lfc.plot_distributions(acsm, sul)

# %%
ds = xr.open_dataset(
'../../releases/v03/data/cluster_series_v3.nc')

# %%
ar  = ds['conc_lab_nc06'].loc[
    {'z_column':'ALL','normalized':0}]

# %%
ar1 = ar.reset_coords(drop=True).to_dataframe().unstack(0)['conc_lab_nc06']

# %%
acsm['Organics'].groupby(acsm.index.hour).median().plot()

# %%
acsm['Sulfate'].groupby(acsm.index.hour).median().plot()

# %%
acsm.groupby(acsm.index.hour).median().plot()

# %%
labs = ar1.columns

# %%
acsm[ar1.columns.values] = ar1[ar1.columns.values]

# %%
ac1 = acsm.dropna(how='any')

# %%
import sklearn.preprocessing as sp

# %%
ac2 = ac1.copy()

# %%
ac2[ac1.columns] = sp.StandardScaler().fit_transform(ac1)

# %%
ac2.plot.scatter(x='08_PW',y='Sulfate',alpha=.2)
ax = plt.gca()
# ax.set_xlim(.1,1000000)
# ax.set_ylim(.1,10)
# ax.set_xscale('log')
# ax.set_yscale('log')

# %%
import scipy.stats

# %%
res = [scipy.stats.pearsonr(ac2[l],ac2['Sulfate']) for l in labs]


# %%
res1 = pd.DataFrame(res,index=labs,columns=['r','p'])

# %%
res1['r'].plot.bar()

# %%
res1['p'].plot.bar()
plt.gca().set_yscale('log')

# %%
res1

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
