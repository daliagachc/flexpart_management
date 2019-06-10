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
# this notebook was created to convert rectanfular coo

# %load_ext autoreload
# %autoreload 2

# %%
import flexpart_management.modules.FLEXOUT as FO
import flexpart_management.modules.flx_array as fa
from useful_scit.imps import *

# %%
# doms = ['d01','d02']
# root_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/*-*-*'
root_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-10_11-10-03_/*-*-*'
path_out = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-10_11-10-03_/log_pol'

root_path = sys.argv[1]
dom = sys.argv[2]
run_name = 'run_2019-06-10_11-10-03_'
paths = glob.glob(root_path)
paths.sort()

# %%
fo_base_dic = dict(
    # dom = 'd01',
    # folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
    folder_path_out=path_out,
    run_name=run_name,
)

# %%
for p in paths:
    print('starting', dom, p)
    new_dic = dict(dom=dom, folder_path=p)
    fo_dic = {**fo_base_dic, **new_dic}

    try:
        fo = FO.FLEXOUT(**fo_dic)
        fo.export_log_polar_coords(keep_z=True)
        print('done', dom, p)
    except:
        print('failed when', dom, p)
