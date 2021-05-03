# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% {"pycharm": {"is_executing": false}}
# this notebook was created to convert rectanfular coo

# %% {"pycharm": {"is_executing": false}}
import flexpart_management.modules.FLEXOUT as FO
import flexpart_management.modules.flx_array as fa
from useful_scit.imps import *

# %%
log.ger.setLevel(log.log.DEBUG)

# %% {"pycharm": {"name": "#%%\n", "is_executing": false}, "jupyter": {"outputs_hidden": false}}
# def main():

# %% {"pycharm": {"name": "#%%\n"}, "jupyter": {"outputs_hidden": false}}
# res = !pwd
doms = ['d01', 'd02']
root_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/*-*-*'
root_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/*-*-*'
path_out = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/log_pol'

run_name = 'run_2019-10-02_13-42-52_'
# run_name = os.path.basename(res[0])

base_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/'

path_run = os.path.join(base_path, run_name)
root_path = os.path.join(path_run, '*-*-*')
path_out = os.path.join(base_path, 'log_pol')
paths = glob.glob(root_path)
paths.sort()

# %%
run_name

# %% {"pycharm": {"name": "#%%\n"}, "jupyter": {"outputs_hidden": false}}
fo_base_dic = dict(
    # dom = 'd01',
    # folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
    folder_path_out=path_out,
    run_name=run_name,
)

# %% {"pycharm": {"name": "#%%\n"}, "jupyter": {"outputs_hidden": false}}
for p in paths:
    for d in doms:
        p, doms

# %%
p, doms

# %% {"pycharm": {"name": "#%%\n"}, "jupyter": {"outputs_hidden": false}}
#         print('starting',d,p)
#         new_dic = dict(dom=d,folder_path=p)
#         fo_dic = {**fo_base_dic,**new_dic}

# %% {"pycharm": {"name": "#%%\n"}, "jupyter": {"outputs_hidden": false}}
#         try:

# %% {"pycharm": {"name": "#%%\n"}, "jupyter": {"outputs_hidden": false}}
#             fo = FO.FLEXOUT(**fo_dic)

# %% {"pycharm": {"name": "#%%\n"}, "jupyter": {"outputs_hidden": false}}
#             fo.export_log_polar_coords()
# print('done',d,p)

# %% {"pycharm": {"name": "#%%\n"}, "jupyter": {"outputs_hidden": false}}
#         except:

# %% {"pycharm": {"name": "#%%\n"}, "jupyter": {"outputs_hidden": false}}
#             print('failed when',d,p)

# %%
