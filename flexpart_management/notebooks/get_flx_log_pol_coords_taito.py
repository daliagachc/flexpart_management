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
from useful_scit.imps import *

# %%
doms = ['d01','d02']
root_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/*-*-*'
path_out = '/Volumes/mbProD/Downloads/flex_out/log_pol'
run_name = 'run_2019-06-02_20-42-05_'
paths = glob.glob(root_path)

# %%
fo_base_dic  = dict(
# dom = 'd01',
# folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
folder_path_out = path_out,
run_name= run_name,
)

# %%
for p in paths:
    for d in doms:
        new_dic = dict(dom=d,folder_path=p)
        fo_dic = {**fo_base_dic,**new_dic}
        fo = FO.FLEXOUT(**fo_dic)
        fo.export_log_polar_coords()
        
