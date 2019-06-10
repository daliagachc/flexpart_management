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
import flexpart_management.modules.constants as co
from useful_scit.imps import *

# %%
# doms = ['d01','d02']
# root_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/*-*-*'
# root_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/*-*-*'
# path_out = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-05_18-42-11_/log_pol'

# run_name = 'run_2019-06-05_18-42-11_'
# paths = glob.glob(root_path)
# paths.sort()

# %%
# fo_base_dic  = dict(
# # dom = 'd01',
# # folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
# folder_path_out = path_out,
# run_name= run_name,
# )

# %%
# for p in paths:
#     for d in doms:
#         print('starting',d,p)
#         new_dic = dict(dom=d,folder_path=p)
#         fo_dic = {**fo_base_dic,**new_dic}
        
#         try:
#             fo = FO.FLEXOUT(**fo_dic)
#             fo.export_log_polar_coords()
#             print('done',d,p)
#         except:
#             print('failed when',d,p)
        

# %%
fo_dic = dict(
folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
dom = 'd02',
folder_path_out = '/Volumes/mbProD/Downloads/flex_out/log_pol',
run_name = 'run_2019-06-02_20-42-05_',
)


# %%
self = FO.FLEXOUT(**fo_dic)

# %%
self.export_log_polar_coords(keep_z=True)

# %%

# %%

# %%

# %%

# %%
fa.compressed_netcdf_save(lp_ds,'/tmp/borrar1.nc')

# %%
