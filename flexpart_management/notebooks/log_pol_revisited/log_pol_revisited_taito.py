# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# from dask.distributed import Client
# client = Client(n_workers=1, threads_per_worker=1, memory_limit='26GB')

import flexpart_management.notebooks.log_pol_revisited. \
    log_pol_revisited_lfc as lfc

from flexpart_management.notebooks.log_pol_revisited. \
    log_pol_revisited_lfc import *




# %%
def main():
    # %%

    # path = '2017-12-17'
    lfc._data_dir = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-10-02_13-42-52_'

    out_dir = 'log_pol_3'

    out_dir = pjoin(lfc._data_dir,out_dir)

    os.makedirs(out_dir,exist_ok=True)



    # dir = pjoin(lfc._data_dir, path)

    dir = sys.argv[1]

    basename = os.path.basename(dir)

    log.ger.warning(f'basename is: {basename}')

    out_path1 = pjoin(out_dir,basename+'_d01.nc')
    out_path2 = pjoin(out_dir,basename+'_d02.nc')



    h1 = xr.open_dataset(pjoin(dir,'header_d01.nc'))
    h2 = xr.open_dataset(pjoin(dir,'header_d02.nc'))
    files1 = glob.glob(pjoin(dir,'flxout_d01*.nc'))
    files2 = glob.glob(pjoin(dir,'flxout_d02*.nc'))
    files1.sort()
    files2.sort()
    # %%
    # %%
    # %%
    # do1(files1, h1, out_path1)
    # %%
    d2(files2, h2, out_path2)
    # %%


def d2(files2, h2, out_path2):
    log.ger.warning('start 2')
    da22 = lfc.get_da2(h2, files2)
    da22 = lfc.sum_over_time(da22)
    log.ger.warning('start s 2')
    fa.compressed_netcdf_save(da22.to_dataset(), out_path2)
    log.ger.warning('done s 2')


def do1(files1, h1, out_path1):
    log.ger.warning('start 1')
    da12 = lfc.get_da2(h1, files1)
    log.ger.warning('load 1')
    da12 = lfc.sum_over_time(da12)
    log.ger.warning('summed 1')
    log.ger.warning('start s 1')
    fa.compressed_netcdf_save(da12.to_dataset(), out_path1)
    log.ger.warning('done s 1')


if __name__ == '__main__':
    main()



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
# %%
