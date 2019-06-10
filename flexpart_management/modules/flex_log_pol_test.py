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
# flp = FLP.FlexLogPol(path,concat=True)
self = FLP.FlexLogPol(path,concat=False,get_clusters=False)

# %%
i = 0
ax = self.plot_cluster_influence_i(colors=FLP.COLORS,i=i)

# %%
axfig=ax.figure.add_subplot(1,1,1)

# %%
axfig.set_ylabel('sdfsdf')
axfig.set_xticks([])
axfig.set_yticks([])
ax.figure

# %%
lab = '(# particles [%] * (residence time))'
fig = self.plot_clusters_inlfuence(ylab='')
fig.text(0.5, 0.1, 'release time (UTC)', ha='center', va='center');
fig.text(0.1, 0.5, lab, ha='center', va='center', rotation='vertical');

# %%

# %%
i = 0
ax = fa.get_ax_bolivia()
for i in range(len_clus):
    clus = self.cluster_flags[i]
    boo = self.merged_ds[co.ClusFlag]==clus
    #     fig,ax = plt.subplots()
    import warnings 
    warnings.simplefilter('ignore')
    ar = self.merged_ds.where(boo)[co.CPer].mean(dim=[co.RL])
    fa.logpolar_plot(ar,ax,name=co.CPer,perM=.15,quantile=False,colorbar=False,patch_args={'cmap':fa.get_custom_cmap(FLP.COLORS[i])})

# %%
i = 0
ax = fa.get_ax_lapaz()
for i in range(len_clus):
    clus = self.cluster_flags[i]
    boo = self.merged_ds[co.ClusFlag]==clus
    #     fig,ax = plt.subplots()
    import warnings 
    warnings.simplefilter('ignore')
    ar = self.merged_ds.where(boo)[co.CCPer].mean(dim=[co.RL])
    fa.logpolar_plot(ar,ax,name=co.CCPer,perM=.05,quantile=False,colorbar=False,patch_args={'cmap':fa.get_custom_cmap(FLP.COLORS[i])})
    fa.add_chc_lpb(ax)

# %%
# fig,axs = plt.subplots(3,4,sharex=True,sharey=True,figsize=(15,10))
axf = axs.flatten()
for i in range(len_clus):
    
#     if i==0:
#         ax = fig.add_subplot(3,4,i+1)
#         ax0 = ax
#     if i>0:
#         ax = fig.add_subplot(3,4,i+1,sharex=ax0,sharey=ax0)
#     ax = fa.get_ax_lapaz()
    ax = fa.get_ax_bolivia()

    clus = self.cluster_flags[i]
    boo = self.merged_ds[co.ClusFlag]==clus
#     fig,ax = plt.subplots()
    ar = self.merged_ds.where(boo)[co.CPer].mean(dim=[co.RL])
    fa.logpolar_plot(ar,ax,name=co.CPer,perM=.3,quantile=False)


# %%
# fig,axs = plt.subplots(3,4,sharex=True,sharey=True,figsize=(15,10))
axf = axs.flatten()
for i in range(len_clus):
    
#     if i==0:
#         ax = fig.add_subplot(3,4,i+1)
#         ax0 = ax
#     if i>0:
#         ax = fig.add_subplot(3,4,i+1,sharex=ax0,sharey=ax0)
    ax = fa.get_ax_lapaz()
#     ax = fa.get_ax_bolivia()

    clus = self.cluster_flags[i]
    boo = self.merged_ds[co.ClusFlag]==clus
#     fig,ax = plt.subplots()
    ar = self.merged_ds.where(boo)[co.CPer].mean(dim=[co.RL])
    fa.logpolar_plot(ar,ax,name=co.CPer,perM=.3,quantile=False)

# %%

# fig,axs = plt.subplots(3,4,sharex=True,sharey=True,figsize=(15,10))
axf = axs.flatten()
for i in range(len_clus):
    
#     if i==0:
#         ax = fig.add_subplot(3,4,i+1)
#         ax0 = ax
#     if i>0:
#         ax = fig.add_subplot(3,4,i+1,sharex=ax0,sharey=ax0)
#     ax = fa.get_ax_lapaz()
    ax = fa.get_ax_bolivia()

    clus = self.cluster_flags[i]
    boo = self.merged_ds[co.ClusFlag]==clus
#     fig,ax = plt.subplots()
    ar = self.merged_ds.where(boo)[co.CCPer].mean(dim=[co.RL])
    fa.logpolar_plot(ar,ax,name=co.CCPer,perM=.01,quantile=False)

# %%
colors = [*sns.color_palette('Set1',n_colors=9,desat=.5),sns.color_palette('Dark2',n_colors=6,desat=.8)[-1]]
fig,axs = plt.subplots(3,4,sharex=True,sharey=True,figsize=(15,10))
axf = axs.flatten()
for i in range(len_clus):
    
#     if i==0:
#         ax = fig.add_subplot(3,4,i+1)
#         ax0 = ax
#     if i>0:
#         ax = fig.add_subplot(3,4,i+1,sharex=ax0,sharey=ax0)
    ax = axf[i]
    color = colors[i]
    clus = self.cluster_flags[i]
    boo = self.merged_ds[co.ClusFlag]==clus
#     fig,ax = plt.subplots()
    self.merged_ds.where(boo)[co.CCPer].sum(dim=[co.R_CENTER,co.TH_CENTER]).plot(color=color,ax =ax)
fig.autofmt_xdate()

# %%
sns.choose_colorbrewer_palette('q')

# %%
sns.choose_colorbrewer_palette('q')

# %%

# %%
i = 1 
clus = self.cluster_flags[i]
boo = self.merged_ds[co.ClusFlag]==clus
self.merged_ds.where(boo)[co.CPer].sum(dim=[co.R_CENTER,co.TH_CENTER]).plot()

# %%

# %%
# cp = self.merged_ds[CCPer][{co.RL:5}]
ax = fa.get_ax_bolivia()
fa.logpolar_plot(cp,ax=ax,name=CCPer,perM=.95)

# %%
# cp = self.merged_ds[CPer][{co.RL:5}]
ax = fa.get_ax_bolivia()
fa.logpolar_plot(cp,ax=ax,name=CPer,perM=.95)

# %%

# %%



# %%

# %%

# %%

# %%





# %%

# %%

r,c

# %%
sns.distplot(trim_vals.flatten())

# %%

# %%

# %%

# %%
nar = ar.where(ar['flags']==10).sum(dim=co.RL)
ax = fa.get_ax_bolivia()
fa.logpolar_plot(nar,ax=ax)
ax = fa.get_ax_lapaz()
fa.logpolar_plot(nar,ax=ax)

# %%
nar = ar.sum(dim=co.RL)
ax = fa.get_ax_bolivia()
fa.logpolar_plot(nar,ax=ax)

# %%

# %%
plt.plot(np.linalg.norm(dfn,axis=1))

# %%
df['norm'] = np.linalg.norm(df,axis=1)

# %%
ax = fa.get_ax_bolivia()
ar2 = d2[co.CONC]
ar1 = d1[co.CONC][{co.R_CENTER:slice(l1m,l1M)}]
fa.logpolar_plot(ar2,ax=ax,quantile=False,perM = 1500)
fa.logpolar_plot(ar1,ax=ax,quantile=False,perM = 1500)
fa.add_chc_lpb(ax)
ax = fa.get_ax_lapaz()
ar2 = d2[co.CONC][{co.R_CENTER:slice(l2m,l2M)}]
ar1 = d1[co.CONC][{co.R_CENTER:slice(l1m,l1M)}]
fa.logpolar_plot(ar2,ax=ax,quantile=False,perM = 1500)
fa.logpolar_plot(ar1,ax=ax,quantile=False,perM = 1500)
fa.add_chc_lpb(ax)

# %%
mer = xr.merge([ar1,ar2])

# %%
mer[co.CONC].plot()

# %%
ar2

# %%
i = 240 
dss = [xr.open_dataset(d) for d in ls[:i]]


# %%
xr.concat(dss,dim=co.RL)

# %%
xr.open_mfdataset(ls[:],concat_dim=co.RL,chunks={co.RL:10},decode_cf=False)

# %%
dat = 'date'
flp.dask_ds_01[dat]=flp.dask_ds_01[co.RL].dt.round('D')

# %%
fd = flp.dask_ds_01[[dat]]

# %%
fd.swap_dims({co.RL:dat}).reset_coords(co.RL).groupby(dat).count()[co.RL].plot()

# %%
