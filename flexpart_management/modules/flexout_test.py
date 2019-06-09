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
import flexpart_management.modules.FLEXOUT as FO
import flexpart_management.modules.flx_array as fa
# %%
fo_dic  = dict(
dom = 'd02',
folder_path = '/Volumes/mbProD/Downloads/failed_flx/2017-12-11',
folder_path_out = '/Volumes/mbProD/Downloads/flex_out/log_pol',
run_name= 'run_2019-06-02_20-42-05_',
)
# %%

fo = FO.FLEXOUT(**fo_dic)

# %%
fo.export_log_polar_coords()

# %%
