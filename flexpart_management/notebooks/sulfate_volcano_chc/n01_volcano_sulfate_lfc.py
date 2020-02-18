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
import pandas
from flexpart_management.modules import constants as co
from matplotlib import pyplot
from scipy.optimize import nnls as nnls
from useful_scit.imps import *

# %%
from useful_scit.imps import pjoin


def plot_nnls_results(res_df):
    f, ax = plt.subplots()
    ax:plt.Axes
    res_df.plot.barh()
    plt.show()
    ax.set_ylabel('cluster')
    ax.set_xlabel('% of the cluster')


def non_negative_least_square_solver(clus_cols, sulf, ts_merged):
    res = nnls(ts_merged[clus_cols], ts_merged[sulf])
    ls, num = res
    # %%
    res_df = pd.Series(ls / ls.sum() * 100,
                       index=clus_cols)
    return res_df, ls.sum(), pd.Series(ls,index=clus_cols)


def import_merged_data(sulf):
    path = 'CHC_QACSM.xlsx'
    path = pjoin(co.tmp_data_path, path)
    acsm = pd.read_excel(path)
    acsm = acsm.set_index('Date UTC')
    acsm = acsm[1:]
    # acsm = acsm['2018-04-01':]
    acsm = acsm.resample('1H').median()
    acsm.index.name = co.RL
    # %%
    clus_ts = pd.read_csv(pjoin(co.tmp_data_path, 'conc_ts_cluster.csv'))
    clus_ts = clus_ts.set_index(co.RL)
    # %%
    clus_cols = clus_ts.columns
    # %%
    ts_merged = pd.merge(clus_ts, acsm, left_index=True, right_index=True)
    ts_merged = ts_merged[~ts_merged[sulf].isna()]
    return clus_cols, ts_merged