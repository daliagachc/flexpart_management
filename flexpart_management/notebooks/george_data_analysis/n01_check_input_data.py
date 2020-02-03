# ---
# jupyter:
#   jupytext:
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

# %%
# local functions and constants
import \
    flexpart_management.notebooks.george_data_analysis.n01_check_input_data_lfc as lfc
# from flexpart_management.notebooks.george_data_analysis.n01_check_input_data_lfc import \
# create_ds
from useful_scit.imps import *

# noinspection PyStatementEffect
np, lfc


# %%
def main():
    # %%
    df_ft, df_ts = lfc.import_time_series()
    # df_ts, df_ft
    # %%
    df_ts.columns
    cols = ['BC', 'SA', 'C4_C5_compounds', 'C6_C8_compounds',
            'C9_C13_compounds',
            'NP']
    yscale = 'linear'
    xscale = 'linear'
    lfc.plot_cols(cols, df_ts, xscale, yscale)
    # %%
    yscale = 'linear'
    xscale = 'log'
    lfc.plot_cols(cols, df_ts, xscale, yscale)
    # %%
    data = lfc.Data()
    data.import_time_seres()
    data.create_ds()
    # %%
    data.add_ratios()
    data.jan_ds_slice()
    # %%
    data.add_quantiles(ds_s='ds_jan')
    # %%
    log.ger.setLevel(log.log.DEBUG)
    fit,da = data.cluster_ds(ds_s='ds_jan',num_of_c=12)
    da['labs'].plot.hist()
    plt.show()
    df = da.to_dataframe().reset_index()

    # f, ax = plt.subplots(figsize=(20,5))
    g = sns.FacetGrid(data=df,row='labs',aspect=5,ylim=(0,1))
    g.map(sns.violinplot,'cluster_vars','quan_value',bw=.1)
    plt.show()

    # %%
    data.ds['labs'] = da['labs']
    data.ds = data.ds.set_coords('labs')
    df=data.ds[data.c_cols].to_array(dim='c_cols',name='vals').to_dataframe().reset_index()
    g = sns.FacetGrid(data=df,row='labs',aspect=1/2,
                      sharey=False,col='c_cols')
    g.map(sns.violinplot,'c_cols','vals',bw=.1)
    plt.show()


    # %%
    da['labs'].plot(figsize=(40,5),linewidth=0,marker='o')
    plt.show()

    # %%
    ds = data.ds
    from sklearn_xarray import wrap
    from sklearn.preprocessing import QuantileTransformer
    from sklearn_xarray.datasets import load_dummy_dataarray
    # %%
    dd = load_dummy_dataarray()
    dd
    # %%
    ds1 = ds.expand_dims(dummy=[0])
    # %%
    d_in = ds1[lfc.c45].transpose('time_utc', 'dummy')
    res = wrap(QuantileTransformer).fit_transform(d_in)
    res.plot.hist()
    plt.show()
    res.where(res['jan']).plot.hist();
    plt.show()
    # %%
    jan:xr.Dataset =ds[ds['jan']]
    ds[ds['jan']]
    ds[{'time_utc':ds['jan']}]
    # %%
    data.candidate_ft_ts
    data.ds
    # %%
    # %%
    # %%

    # %%

    data.add_ratios_quantiles()
    # %%
    data.ds.where(data.ds['jan']).plot.scatter(
        x=lfc.c45, y=lfc.c68, marker='o',
        facecolor='none',
        edgecolor='k',
        alpha = .1
    )
    plt.show()
    # %%

    # %%
    # %%
    # %%
if __name__ == '__main__':
    main()