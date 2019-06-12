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
# %load_ext autoreload
# %autoreload 2


# %%
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FLP
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

# %%
path = '/Volumes/mbProD/Downloads/flx_log_coor/run_2019-06-05_18-42-11_'
path = '/Volumes/mbProD/Downloads/flx_log_coor/run_2019-06-10_11-10-03_'
# flp = FLP.FlexLogPol(path,concat=True)
# self = FLP.FlexLogPol(path,concat=False)
self = FLP.FlexLogPol(
    path,
#     concat=True,
    concat=False,
    get_clusters=False,
    open_merged=True,
    clusters_avail=False
)

# %%

# %%
com=fa.get_dims_complement(self.merged_ds,[co.R_CENTER,co.TH_CENTER])
sds = self.merged_ds.sum(com)
ax = fa.get_ax_bolivia()
fa.logpolar_plot(sds[co.CONC],name=co.CONC,ax= ax, drop_zeros=False)

# %%
ax = fa.get_ax_bolivia()
fa.logpolar_plot(self.merged_ds[co.TOPO],name=co.TOPO,ax= ax, drop_zeros=False)

# %%
self.reset_z_levels()

# %%
com=fa.get_dims_complement(self.merged_ds,[co.R_CENTER,co.TH_CENTER])
sds = self.merged_ds.sum(com)
ax = fa.get_ax_bolivia()
fa.logpolar_plot(sds[co.CONC],name=co.CONC,ax= ax, drop_zeros=False)

# %%
self.python_cluster(n_cluster=15)

# %%
com=fa.get_dims_complement(self.merged_ds,[co.R_CENTER,co.TH_CENTER])
sds = self.merged_ds.sum(com)
ax = fa.get_ax_bolivia()
fa.logpolar_plot(sds[co.CONC],name=co.CONC,ax= ax, drop_zeros=False)

# %%
self.python_cluster(n_cluster=4)

# %%

for i in range(len(self.cluster_flags)):
# for i in range(1):
    fig = self.plot_cluster_grid(i,co.CPer)


# %%
self.plot_clusters_inlfuence(cols=1)

# %%
self.python_cluster(n_cluster=15)

# %%

for i in range(len(self.cluster_flags)):
# for i in range(1):
    fig = self.plot_cluster_grid(i,co.CPer)


# %%
self.plot_clusters_inlfuence(cols=3)

# %%
