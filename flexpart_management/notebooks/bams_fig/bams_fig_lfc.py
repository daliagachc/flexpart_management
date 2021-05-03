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
from useful_scit.imps import *

import holoviews as hv
from holoviews import opts


plt;
# %%
def open_plot_save(CONC_ALL, CSV_FILE, D1, D2, DIRNAME):

    hv.extension('bokeh')
    # %%
    path = '/Users/diego/flexpart_management/flexpart_management/releases/v03/data/cluster_series_v3.nc'
    # %%
    ds = xr.open_dataset(path)
    da = ds[CONC_ALL].loc[
        {'z_column': 'LEV0', 'normalized': 1, 'releases': slice(D1, D2)}]
    _df = da.to_dataframe()[CONC_ALL]
    ly = hv.Curve(_df)
    ly(opts.Curve(height=300, width=900))
    # %%
    df = da.to_dataframe()[[CONC_ALL]]
    df.index.name = 'UTC'
    df['BOT'] = df.index + pd.Timedelta(hours=-4)
    df['H'] = df['BOT'].dt.hour
    gr = df[['H', CONC_ALL]].groupby('H')
    # %%
    # diu = pd.DataFrame()
    diu = gr[[CONC_ALL]].mean()
    diu = diu.rename({CONC_ALL: 'c_mean'}, axis=1)
    diu['c_med'] = gr[CONC_ALL].median()
    diu['p_05'] = gr[CONC_ALL].quantile(.05)
    diu['p_95'] = gr[CONC_ALL].quantile(.95)
    diu.plot()
    # %%
    p = DIRNAME
    p = pjoin(p, CSV_FILE)
    diu.to_csv(p)

    return ly