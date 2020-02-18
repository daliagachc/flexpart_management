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
import add_quantiles_to_medeoids_lfc as lfc
from add_quantiles_to_medeoids_lfc import *


# %%

def main():
    # %%
    ds = fa.open_temp_ds_clustered_18()
    da_load = ds[co.CONC].load()
    # %%
    tab_name = 'tmp'
    tmp_dir = '/tmp'
    engine = create_db(ds, tab_name)
    # %%
    while True:
        row = get_last_row(engine, tab_name)
        # %%
        mega_ds = get_the_stats(da_load, row)
        # %%
        path_out = pjoin(tmp_dir, row['file_name'])
        mega_ds.to_netcdf(path_out)
        # %%
        update_tab_success(engine, row, tab_name)

    # %%

    name_out = 'cluster_stat_ts.nc'
    path_out = pjoin(co.tmp_data_path,name_out)
    # save_the_multiple_files(path_out, tab_name, tmp_dir)
    engine = get_engine()
    sql = f'select * from {tab_name} where ran=1'
    df = pd.read_sql(sql, engine)
    df['path'] = tmp_dir + '/' + df['file_name']
    mds = xr.open_mfdataset(df['path'], concat_dim=co.RL, combine='nested')
    mds.load()
    # %%
    # mds.to_netcdf(path_out)
    clust_ts = open_clus_ts()
    prop_df = open_prop_df()

    # %%

    i2n_dic = prop_df['short_name'].to_dict()
    n2i_dic = {l:k for k,l in i2n_dic.items()}

    i2n_v = np.vectorize(lambda i:i2n_dic[int(i)])
    # %%
    master_ds = clust_ts.to_xarray().to_array(dim='lab_name',name = 'srr_pt')
    # %%
    for k in list(mds.keys()):
        mds = mds.rename({k:k+'_stat'})
    # %%
    mds = mds.to_array(dim='stat_dim',name='stat_vals')
    mds = mds.assign_coords({'lab_name':xr.apply_ufunc(i2n_v,mds['lab'])})
    # mds = mds.swap_dims({'lab_name':'lab'})
    mds = mds.swap_dims({'lab':'lab_name'})
    # %%
    merged_ds = xr.merge([mds,master_ds])

    # %%
    merged_ds.to_netcdf(pjoin(co.tmp_data_path,'clus_medeoid_stats.nc'))
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%

