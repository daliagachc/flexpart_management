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
from useful_scit.imps import *
import flexpart_management.modules.constants as co
ucp
# %%

def main():
    # %%
    log.ger.setLevel(log.log.DEBUG)
    files_path = pjoin(co.tmp_data_path,'chc_wrf_slice/*')
    files = glob.glob(files_path)
    files.sort()
    # %%
    files_short = files[:]
    # ds = xr.open_mfdataset(files_short,concat_dim='Time',combine='nested')
    # %%
    # %%
    var_list = ['wa','z','p','slp']
    ts_out_list = []
    for f in files_short[:]:
        log.ger.debug('f: %s',f)
        ds_out = get_ts_single_cell([f], var_list)
        ts_out_list.append(ds_out)
    # %%
    new_list = [ts_out.drop(['XTIME','datetime']) for ts_out in ts_out_list]
    ts_out = xr.concat(new_list,dim='Time')
    # %%
    df = ts_out.reset_coords(drop=True).to_dataframe()
    data_path = '/Users/diego/flexpart_management/flexpart_management/' \
                'requests/george/data'
    # df.to_csv(pjoin(
    #     data_path,
    #     'time_series_column_for_selected_values_at_chc_wrf.csv'
    # ))

    # %%
    for v in list(ts_out.variables):
        ts_out[v].attrs.pop('projection','nan')
        ts_out[v].attrs.pop('coordinates', 'nan')
    # %%
    path_out = pjoin(data_path,
                     'time_series_column_for_selected_values_at_chc_wrf.nc')
    # ts_out.to_netcdf(path_out)
    za.compressed_netcdf_save(ts_out, path_out)


    # %%

    pass

# %%
def get_ts_single_cell(files_short, var_list):
    import netCDF4
    import wrf
    ds_list = [netCDF4.Dataset(f) for f in files_short]
    out_list = []
    slice = {co.SN: 1, co.WE: 1}
    # wrf_ds = ds[wrf_list][slice]
    for v in var_list:
        dsv = wrf.getvar(ds_list, v, timeidx=wrf.ALL_TIMES)
        dsv = dsv[slice]
        out_list.append(dsv)
    ds_out = xr.merge(out_list)
    [ds.close() for ds in ds_list]
    return ds_out



if __name__ == '__main__':
    main()