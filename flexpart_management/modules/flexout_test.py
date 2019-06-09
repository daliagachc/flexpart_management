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
dom = 'd01',
folder_path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10',
folder_path_out = '/Volumes/mbProD/Downloads/flex_out/log_pol',
run_name= 'run_2019-06-02_20-42-05_',
)
# %%

fo = FO.FLEXOUT(**fo_dic)

# %%
rels = fo.flexout_hour_ds[fa.RL].to_dataframe()

# %%
rdf = fo.export_log_polar_coords()

# %%
for k,r in rdf.iterrows():
    v  = r

# %%
v[fa.RL]

# %%
rels.dt.strftime('%Y')

# %%
r0 = rels[0].to_series()

# %%
r0.dt.str

# %%
res = fo.get_log_polar_coords(rels[1])

# %%
fa.compressed_netcdf_save(res,'/tmp/borrar.nc')

# %%
res.sum()/96

# %%
ax = fa.get_ax_bolivia()
fa.logpolar_plot(res,ax=ax)

# %%
