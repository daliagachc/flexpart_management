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
import flexpart_management.notebooks.log_pol_revisited. \
    log_pol_revisited_lfc as lfc

from flexpart_management.notebooks.log_pol_revisited. \
    log_pol_revisited_lfc import *


# %%
def main():
    # %%

    # path = '2017-12-17'
    lfc._data_dir = '/homeappl/home/aliagadi/wrk/DONOTREMOVE' \
                    '/flexpart_management_data/runs/run_2019-10-02_13-42-52_'

    out_dir = 'log_pol_log_pol'

    out_dir = pjoin(lfc._data_dir, out_dir)

    os.makedirs(out_dir, exist_ok=True)

    # dir = pjoin(lfc._data_dir, path)

    dir = sys.argv[1]

    # %%
    dir_ = dir[:-4]
    p1 = dir_ + '1.nc'
    p2 = dir_ + '2.nc'
    # %%

    basename = os.path.basename(dir[:-7])

    log.ger.warning(f'basename is: {basename}')
    # %%

    out_path1 = pjoin(out_dir, basename + '_log_pol.nc')
    # out_path2 = pjoin(out_dir,basename+'_d02.nc')
    # %%
    ds2 = xr.open_dataset(p2)
    ds1 = xr.open_dataset(p1)

    da2 = lfc.get_log_pol(ds2)
    da1 = lfc.get_log_pol(ds1)

    aa = lfc.get_merged_da_log_pol2(ds1[co.CONC], ds2[co.CONC])

    aa = aa.set_coords(['G_AREA', 'AGE'])

    fa.compressed_netcdf_save(aa, out_path1)
    log.ger.warning('done s')
    # %%


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
