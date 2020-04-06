# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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

# %%
import flexpart_management.notebooks.compare_6_vs_18.compare_6_vs_18_lfc as lfc
from flexpart_management.notebooks.compare_6_vs_18.compare_6_vs_18_lfc import *


# %%
# def main():
# %%
ds = fa.open_temp_ds_clustered_18()
# %%

ds[CS].plot.hist(log=True)
plt.hist
plt.show()
# %%
dat = lfc.trim_ds(ds=ds)
# %%
dat.plot.hist(log=True)
plt.show()

# %%
dat1 = lfc.add_total_cs(dat=dat)
# %%
dat1[TOT_CS].plot.hist(log=True)
plt.show()
# %%
nds = getQT(dat=dat1)
# %%
nds[CQT].plot.hist(log=True)
plt.show()

nds[CQT][{SD:20}].plot.hist()
plt.show()
# %%
nds1 = lfc.get18(ds=nds,random_state=19)
# %%
nds1[LAB18].to_series().plot.hist()
plt.show()
# %%
nds2 = lfc.get6(ds=nds1,random_state=7)
# %%
plot_heatmap_6_vs_18(nds2)
# %%
nds1[lfc.TOT_CS].sum()
# %%
# %%
nds3 = lfc.get_18_6(nds2=nds2)
# %%
nds3 = lfc.cluster(ds=nds3,n_clusters=2,lab_name=lfc.LAB2,random_state=2)
# %%
nds3
# %%
ds66 = lfc.get_6_6_ds(nds3=nds3)
# %%
var = CQT
X = nds3[var].transpose(SD, co.RL)
from sklearn.metrics import pairwise_distances
diss = pairwise_distances(X,metric='euclidean')
# %%
f, ax = plt.subplots()
ax:plt.Axes

lab = lfc.LAB6
lfc.plot_sil_weighted_hist(lab=lab,ax=ax,nds3=nds3,diss=diss)

lab = lfc.LAB18
lfc.plot_sil_weighted_hist(lab=lab,ax=ax,nds3=nds3,diss=diss)

lab = lfc.LAB_18_6
lfc.plot_sil_weighted_hist(lab=lab,ax=ax,nds3=nds3,diss=diss)

lab = lfc.LAB
lfc.plot_sil_weighted_hist(lab=lab,ax=ax,nds3=nds3,diss=diss)

lab = lfc.LAB2
lfc.plot_sil_weighted_hist(lab=lab,ax=ax,nds3=nds3,diss=diss)

ax.legend()
plt.show()
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
