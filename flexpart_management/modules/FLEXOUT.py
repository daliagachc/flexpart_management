# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
'''class created to control the output from flexpart'''
from useful_scit.imps import *
import typing
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
import pandas as pd

DEBUG = True


def dp(*args):
    if DEBUG:
        print(*args)


class FLEXOUT:
    dom: str = None
    folder_path: str = None
    head_file_path: str = None
    out_file_list: typing.List[str] = None
    head_ds: xr.Dataset = None
    out_ds_list: typing.List[xr.Dataset] = None
    head_pat: str = 'header_'
    out_file_pat: str = 'flxout_'
    out_path_pat: str = None
    out_dask_ds: xr.Dataset = None
    flexout_ds: xr.Dataset = None
    flexout_hour_ds_list: typing.List[xr.Dataset] = None
    flexout_hour_ds: xr.Dataset = None
    hours = 96
    folder_path_out: str = None
    run_name: str = None

    def __init__(self, dom: str,
                 folder_path: str,
                 folder_path_out: str = None,
                 run_name: str = None,
                 ):
        self.dom = dom
        self.folder_path = os.path.join(folder_path, '')
        self.folder_path_out = os.path.join(folder_path_out, '')
        self.run_name = run_name

        self.set_head_path()
        self.set_out_file_path_list()

        self.head_ds = xr.open_dataset(self.head_file_path)
        self.out_dask_ds = xr.open_mfdataset(self.out_file_list, concat_dim=co.TIME)
        self.out_dask_ds = fa.convert_ds_time_format(self.out_dask_ds)
        self.get_and_tune_flexout_ds()

        self.get_flx_hour_ds_list()

        self.flexout_hour_ds = xr.concat(self.flexout_hour_ds_list, dim=co.RL)

    def get_flx_hour_ds_list(self):
        releases = self.flexout_ds[co.RL]
        self.flexout_hour_ds_list = []
        for r in releases:
            nds = self.flexout_ds.sel(**{co.RL: r})
            nds = fa.trim_swap_dim_coord(nds, self.hours)
            self.flexout_hour_ds_list.append(nds)

    def get_and_tune_flexout_ds(self):
        self.flexout_ds = fa.join_head(self.out_dask_ds, self.head_ds)
        # self.flexout_ds = fa.add_release_time_dim(self.flexout_ds, self.head_ds)
        self.flexout_ds = fa.assign_vars_to_cords(self.flexout_ds)
        self.flexout_ds = fa.add_lat_lot(self.flexout_ds)
        self.flexout_ds = fa.add_zmid(self.flexout_ds)
        self.flexout_ds = fa.add_zbot(self.flexout_ds)
        self.flexout_ds = fa.add_zlength_m(self.flexout_ds)
        self.flexout_ds = fa.add_alt_m(self.flexout_ds)
        self.flexout_ds = fa.add_volume(self.flexout_ds)

    def set_head_path(self):
        head_file = self.folder_path + '*' + self.head_pat + '*' + self.dom + '*'
        dp(head_file)
        head_file = glob.glob(head_file)[0]
        self.head_file_path = head_file
        dp(self.head_file_path)

    def set_out_file_path_list(self):
        out_path = self.folder_path + '*' + self.out_file_pat + '*' + self.dom + '*'
        self.out_path_pat = out_path
        dp(out_path)
        out_path = glob.glob(out_path)
        out_path.sort()
        self.out_file_list = out_path
        dp(self.out_file_list[:1])
        self.check_files_are_not_corrupted()

    def check_files_are_not_corrupted(self):
        new_out_list = []
        for f in self.out_file_list:
            try:
                nf = xr.open_dataset(f)
                new_out_list.append(f)
            except:
                print('cant open', f)
        self.out_file_list = new_out_list

    def get_log_polar_coords(self,
                             release: pd.Timestamp,
                             coords_to_keep=[co.WE, co.SN],
                             rounding_vals=[co.ROUND_R_LOG, co.ROUND_TH_RAD]
                             ):

        keep_list = [co.RL]
        keep_vars = [co.CONC]
        keep_coords = coords_to_keep

        sum_ds = self.flexout_hour_ds
        sum_ds = sum_ds[keep_vars].sel(**{co.RL: release})
        complement_coords = fa.get_dims_complement(sum_ds, keep_coords)
        sum_ds = sum_ds.sum(dim=complement_coords)

        val = rounding_vals
        lp_ds = xr.Dataset()
        for v in keep_vars:
            lp_ds[v] = fa.data_array_to_logpolar(
                sum_ds[v],
                *val,
                dim2keep=keep_list)

        return lp_ds

    def export_log_polar_coords(self):
        out_path = os.path.join(self.folder_path_out,self.run_name)
        os.makedirs(out_path,exist_ok=True)
        releases = self.flexout_hour_ds[co.RL]
        rel_df = releases.to_dataframe()
        rn = 'release_name'
        rp = 'release_path'
        rel_df[rn]= rel_df[co.RL].dt.strftime(self.dom+'_%Y-%m-%d_%H-%M-%S.nc')
        rel_df[rp]= rel_df[rn].apply(
            lambda n: os.path.join(out_path,n))
        for k,r in rel_df.iterrows():
            try:
                lp_ds = self.get_log_polar_coords(r[co.RL])
                fa.compressed_netcdf_save(lp_ds,r[rp])
            except:
                print('error in',k)

        return rel_df


