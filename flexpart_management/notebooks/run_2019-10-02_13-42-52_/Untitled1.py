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

# %%
from useful_scit.imps import *

# %%
import flexpart_management.modules.flx_array as fa

# %%
res = !pwd

run_name = os.path.basename(res[0])

base_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/'

path_run = os.path.join(base_path,run_name)
root_path = os.path.join(path_run,'*-*-*')
path_out = os.path.join(base_path,'log_pol')
paths = glob.glob(root_path)
paths.sort()

# %%
path = paths[10]
files = glob.glob( os.path.join( path, '*d01*.nc' ) )

# %%
file = files[10]

# %%
ds = xr.open_dataset (file)

# %%
head = !ls -uh {path}/*head*d01*.nc
head = head[0]

# %%
head_ds = xr.open_dataset(head)

# %%
ds1 = fa.convert_ds_time_format(ds)

# %%
tuned_flx_out = fa.get_and_tune_flexout_from_ds_and_head(ds1,head_ds)

# %%
fa.data_array_to_logpolar( tuned_flx_out['CONC'],
                           1,
                           10
                         )

# %%
