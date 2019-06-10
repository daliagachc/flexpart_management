# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

class FlxOutCheckAlt:
    path_pat = None
    dom = None
    flx_pat = 'flxout_'
    head_pat = 'header_'
    path_list = []
    flx_glob = None
    head_glob = None
    dask_ds = None
    head_ds = None
    sum_z_ds = None
    out_z_path = None
    def __init__(self,
                 path_pat,
                 dom,
                 out_z_path):
        self.path_pat = path_pat
        self.dom=dom
        self.out_z_path = out_z_path
        self.get_globs(dom)

        self.get_path_list()

        self.get_head_ds()

        self.get_dask_ds()
        self.sum_dask_ds_over_zt()

        # self.save_z_sum_ds(out_z_path)

    def save_z_sum_ds(self):
        self.sum_z_ds.to_netcdf(self.out_z_path)

    def sum_dask_ds_over_zt(self):
        # dim2sum = fa.get_dims_complement(self.dask_ds, co.ZT)
        print('start to sum')
        self.sum_z_ds = self.dask_ds[co.CONC].sum(
            dim=['releases', 'ageclass', 'south_north', 'west_east',]
        ).load()
        print('end load')
        self.sum_z_ds = self.sum_z_ds.sum('Time')


    def get_dask_ds(self):
        self.dask_ds = xr.open_mfdataset(self.path_list, concat_dim=co.TIME)
        self.dask_ds[co.ZT] = self.head_ds[co.ZT]
        self.dask_ds = self.dask_ds.swap_dims({co.BT: co.ZT})

    def get_head_ds(self):
        head_path = glob.glob(self.head_glob)[0]
        self.head_ds = xr.open_dataset(head_path)

    def get_path_list(self):
        self.path_list = glob.glob(self.flx_glob)
        self.path_list.sort()
        checked_list = []
        for p in self.path_list:
            try:
                ds = xr.open_dataset(p)
                ds.close()
                checked_list.append(p)
            except:
                print('cant open', p)
        self.path_list = checked_list

    def get_globs(self, dom):
        self.flx_glob = os.path.join(
            self.path_pat,
            self.flx_pat + dom + '*.nc'
        )
        self.head_glob = os.path.join(
            self.path_pat,
            self.head_pat + dom + '*.nc'
        )