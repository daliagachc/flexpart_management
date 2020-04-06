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
import flexpart_management.notebooks.sulfate_simple_cluster_corr_paper.\
    sulfate_simple_cluster_corr_paper_lfc as lfc
from flexpart_management.notebooks.sulfate_simple_cluster_corr_paper. \
    sulfate_simple_cluster_corr_paper_lfc import *

# %%
def main():
    # %%
    path = 'CHC_QACSM.xlsx'
    path = pjoin(co.tmp_data_path, path)
    acsm = pd.read_excel(path)
    acsm = acsm.set_index('Date UTC')
    acsm = acsm[1:]
    # acsm = acsm['2018-04-01':]
    acsm = acsm.resample('1H').median()
    acsm.index.name = co.RL
    sul = 'Sulfate'
    # %%
    f, axs = plt.subplots(2,2,dpi=300)
    f:plt.Figure
    sul_ = acsm[sul]
    sul_[sul_ <= 0] = 0.01
    sul_.plot(ax=axs[0, 0])
    from sklearn.preprocessing import PowerTransformer, QuantileTransformer
    spt = PowerTransformer(standardize=False).fit_transform(acsm[[sul]])
    spt2 = PowerTransformer(standardize=True,method='box-cox').fit_transform(acsm[[sul]])
    sns.distplot(sul_,ax=axs[1,0])
    axs[1,0].set_title('normal')
    sns.distplot(spt,ax=axs[1,1])
    axs[1,1].set_title('power transform')
    sns.distplot(spt2,ax=axs[0,1])
    axs[0,1].set_title('power transform Box-Cox')
    f.tight_layout()
    plt.show()

    # %%
    ds = fa.open_temp_ds('ds_clustered_18_agl.nc')
    # ds['lab_name'] = ds['lab_name'][{co.RL: 0}]
    # %%
    lab_name = 'lab_name'
    df3 = get_lab_df(ds, lab_name,zM=3)
    df33 = get_lab_df(ds,lab_name,zM=None)
    # %%
    dj = df3.join(acsm,how='inner')
    df4 = dj[df3.columns]
    dj3 = df33.join(acsm,how='inner')
    df44 = dj3[df33.columns]
    ac = dj[[sul]].copy()
    ac.loc[ac[sul]<=0,sul]=.001
    # %%
    ac['pt'] = PowerTransformer(standardize=True,method='box-cox').fit_transform(ac)

    # %%
    ac['pt'].describe()
    res = (df4.T*ac['pt']).T.sum()/df4.sum()
    res2 = (df44.T * ac['pt']).T.sum() / df44.sum()
    # %%
    f, axs = plt.subplots(1,4,figsize=(20,10))
    axf = axs.flatten()

    res.plot.barh(ax=axf[0])
    axf[0].set_xlabel('prediction surface')
    res2.plot.barh(ax=axf[1])
    axf[1].set_xlabel('prediction all')
    df4.sum().plot.barh(ax=axf[2])
    axf[2].set_xlabel('sum surface')
    df44.sum().plot.barh(ax=axf[3])
    axf[3].set_xlabel('sum total')
    plt.tight_layout()
    plt.show()

    # %%
    f, ax = plt.subplots(2,2)
    sm = ac[sul] / ac[sul].mean()
    sns.distplot(sm, ax=ax[0, 0])
    _lab = '09_MR'
    fm = df4[_lab] / df4[_lab].mean()
    sns.distplot(fm, ax=ax[1, 0])
    plt.show()
    # %%
    from sklearn.linear_model import LinearRegression
    from sklearn import metrics
    xy = pd.DataFrame(fm).join(sm).dropna().copy()
    xy.loc[xy[_lab]<=0,_lab]=0.00001

    # %%
    from scipy import stats
    pt = PowerTransformer(standardize=True, method='box-cox')
    X  = xy[sul]
    Y = xy[_lab]
    # X = pt.fit_transform(xy[[sul]])[:,0]
    # Y = pt.fit_transform(xy[[_lab]])[:,0]
    res = stats.linregress(X, Y)
    sns.jointplot(X,Y,kind='hex',xlim=(0,2),ylim=(0,2))
    plt.show()


    # %%


# %%


def get_lab_df(ds, lab_name,*, zM):
    # %%
    # zM=3
    ds_ = ds[[co.CONC, lab_name]][{co.ZM: slice(0, zM)}]
    # %%
    labs = np.unique(ds[lab_name][{co.RL:0}])
    labs = list(set(labs) - {'nan'})
    labs.sort()

    # %%
    ll = []
    for l in labs:
        r = ds_[co.CONC].where(ds_[lab_name]==l).sum([co.TH_CENTER,co.R_CENTER,co.ZM])
        r.name=l
        ll.append(r)
    lld = xr.merge(ll)
    df = lld.to_dataframe()


    # %%
    # %%

    # df = ds_.to_dataframe()
    return df

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


