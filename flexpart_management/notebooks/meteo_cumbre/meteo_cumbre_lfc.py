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
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
plt;
# %%
def import_time_series():
    data_path = pjoin(co.tmp_data_path, 'data_george_cc.xlsx')
    # df_ft = pd.read_excel(data_path)
    df_ts = pd.read_excel(data_path, sheet_name=1, skiprows=1)
    # %%
    df_ts = df_ts.set_index(pd.to_datetime(df_ts['time_utc']))
    df_ts = df_ts.drop('time_utc', axis=1)
    return df_ts