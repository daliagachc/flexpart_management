# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# %%
# %% [markdown]
# imports
# %%
from sklearn.preprocessing import QuantileTransformer
from useful_scit.imps import *
# noinspection PyUnresolvedReferences
import matplotlib.colors
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
# noinspection PyUnresolvedReferences
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.clustering_funs as cfuns
from sklearn.metrics import silhouette_samples
# %%

# ds = xr.open_mfdataset( [ co.latest_ds_mac ] , combine='by_coords' )

ds = fa.open_temp_ds_clustered_18()


# %%
ds

# %%
conc_var = 'conc_smooth_norm'
lab = 'lab'
above_thre = 'above_thre'
# labs = ds[lab]
# dsc = ds[conc_var].to_dataset(co.RL)
# %%
# dsc
# %%

# %%

sel = {
    co.RL:slice(None,None,1),
    co.R_CENTER:slice(None,None,1),
    co.TH_CENTER:slice(None,None,1),
    co.ZM:slice(None,None,1),
}
ds_reset = ds.reset_coords()[[conc_var, lab, above_thre]]
ds_reset = ds_reset[sel].assign_coords({lab:ds_reset[lab]})
ds_new = ds_reset.where(ds_reset[above_thre]).drop(above_thre)
da = ds_new[conc_var].drop(lab)
df = da.load().to_dataframe()[conc_var].dropna()
dfu = df.unstack(co.RL)
# %%

# %%
dl = ds_new[lab].reset_coords(drop=True)
dlf =dl.to_dataframe()
dlf
# %%

index = dfu.index
vals = dfu.loc[index]
labs = dlf.loc[index]
# %%

scaler = QuantileTransformer()
vals_quan = scaler.fit_transform( vals.T ).T * 1000
# vals_quan = vals*1000
# %%
tot = vals.sum(axis=1)
plt.hist(tot)
plt.hist(vals_quan.sum(axis=1))
plt.show()
# %%
out_dic = {}
for n in range(2,25):
    print(n)
    from sklearn.cluster import KMeans
    new_lab = KMeans(n_clusters=n).fit_predict(vals_quan,sample_weight=100*tot)
    res = silhouette_samples(vals_quan, new_lab)
    res2 = silhouette_samples(vals_quan, new_lab, metric='l1')
    from sklearn.metrics import silhouette_score

    # print(silhouette_score(vals_quan, new_lab))
    wss = (res*tot).sum()/tot.sum()
    ss = res.mean()
    
    wss2 = (res2*tot).sum()/tot.sum()
    ss2 = res2.mean()
    print(wss)
    print(ss)
    dic = {
        'ss':ss,'wss':wss,'res':res,'new_lab':new_lab,
        'ss2':ss2,'wss2':wss2,'res':res2
    }
    out_dic[n]=dic

# %%

# %%
df_dic = pd.DataFrame(out_dic).T
# %%
df_dic[['wss2','wss','ss','ss2']].plot()

# %%
# df_dic.to_pickle(co.silhouette_path)
df_dic.to_pickle('/Users/diego/flexpart_management/flexpart_management/tmp_data/silhouette_scores_non.pickle')
# %%
df_dic = pd.read_pickle(co.silhouette_path)

# %%
plt.scatter(df_dic.index,df_dic['wss'])
plt.scatter(df_dic.index,df_dic['ss'])
plt.show()
# %%
dlf['res']=np.nan
dlf['tot']=np.nan
dlf.loc[index,'res'] = res
dlf.loc[index,'tot'] = vals.sum(axis=1)

# %%
ndf = dlf.loc[index].sort_values(['lab','res']).reset_index()
(ndf['res']*ndf['tot']).plot()
plt.show()

# %%
import numpy as np
a=0.08046 
b=0.09633 
c=0.1153

# %%
al=np.log(a)
bl=np.log(b)
cl=np.log(c)

# %%
bl-al

# %%
cl-bl

# %%
np.exp(bl+.18)

# %%
np.exp(np.log(3))

# %%
4248 * 31 *36 * 30

# %%
31 *36 * 30

# %%
ds[above_thre].reset_coords(drop=True).to_dataframe()[above_thre].value_counts()
# %%
24900 + 8580
# %%
dc = ds['CONC']
dcs = dc.sum(co.RL)
a = dcs.where(dcs<=0).count().load()

b = dcs.where(~ds[above_thre]).count().load()
a/b
# %%
dcs.where(~ds[above_thre]).where(dcs>0).load().median()
# %%
dcs.where(ds[above_thre]).load().median()
# %%

dcs.where(ds[above_thre]).load().mean()
# %%
# %%
# %%
