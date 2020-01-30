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
# noinspection PyStatementEffect
from vertical_plots_from_wrf_lfc import open_slice_and_save

ucp
from wrf_management.modules.util import get_df_list
import wrf
from flexpart_management.modules import constants as co
log.ger.setLevel(log.log.DEBUG)
import sys
# %%
def main():
    # %%
    date_low_limit = '2017-12-16'
    if len(sys.argv) >= 2:
        date_low_limit = sys.argv[1]
    wrf_path = '/proj/atm/saltena/runs/run_2019_05_15/wrf'

    ex_name = 'wrfout_d04_2017-12-30_16:00:00'
    df_list:pd.DataFrame = get_df_list(path=wrf_path,pref='wrfout_d04')

    out_path_dir = '/homeappl/home/aliagadi/saltena_2018/flexpart_management/' \
                   'flexpart_management/tmp_data/chc_wrf_slice/'

    # %%
    df_list = df_list.reset_index().set_index('date')
    df_list['day']=pd.to_datetime(df_list.index.date)
    df_list['out_path'] = df_list['day'].dt.strftime(
        '%Y_%m_%d.nc').apply(lambda d: pjoin(out_path_dir,d))
    # %%
    f1 = df_list['p'].iloc[0]
    # %%
    ds = xr.open_dataset(f1)
    # %%
    x,y = wrf.ll_to_xy(ds._file_obj.ds,co.CHC_LAT,co.CHC_LON).values
    # %%
    # wrf.getvar(ds._file_obj.ds,'eth',timeidx=wrf.ALL_TIMES)
    df_list = df_list[df_list.index>date_low_limit]
    # %%
    # wrf.getvar(ds._file_obj.ds,'wa',timeidx=wrf.ALL_TIMES)
    # %%
    df_g = df_list.groupby('out_path')
    # %%
    # %%
    for out_path,df in df_g:
        log.ger.debug(f'startint with {out_path}')
        file_list = df.iloc[:]['p']
        open_slice_and_save(file_list, out_path, x, y)
    # %%
    # nds = xr.open_dataset(out_path)
    # eth = wrf.getvar(nds._file_obj.ds, 'eth', timeidx=wrf.ALL_TIMES)
    # wa  = wrf.getvar(nds._file_obj.ds, 'wa', timeidx=wrf.ALL_TIMES)
    # ua  = wrf.getvar(nds._file_obj.ds, 'ua', timeidx=wrf.ALL_TIMES)
    # va  = wrf.getvar(nds._file_obj.ds, 'va', timeidx=wrf.ALL_TIMES)
    # # %%
    #
    # nds = xr.open_dataset(out_path)
    # z  = wrf.getvar(nds._file_obj.ds, 'z', timeidx=wrf.ALL_TIMES)
    # print(z.max(),z.min())


    # %%
    # %%


# %%
if __name__ == '__main__':
    main()
    pass





