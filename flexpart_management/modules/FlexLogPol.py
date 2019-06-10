# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
from sklearn.preprocessing import normalize
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages

COLORS = [*sns.color_palette('Set1', n_colors=9, desat=.5), sns.color_palette('Dark2', n_colors=6, desat=.8)[-1]]


class FlexLogPol:
    source_path:str = None
    d1 = 'd01'
    d2 = 'd02'
    doms = []
    list_d1 = []
    list_d2 = []
    pat_d1 = ''
    pat_d2 = ''
    dask_ds_01 = None
    dask_ds_02 = None
    dasks_dic = None
    combined_path = 'combined'
    merged_ds = None
    merged_path = None
    cluster_flags = []

    def __init__(self,
                 source_path:str,
                 concat = False,
                 save_concat = True,
                 get_clusters = False,
                 ):
        self.save_concat = save_concat
        self.concat = concat
        self.doms = [self.d1,self.d2]
        self.source_path = os.path.join(source_path,'')
        self.combined_path = os.path.join(self.source_path,
                                          self.combined_path)
        self.merged_path = os.path.join(
            self.combined_path,
            'merged_ds.nc'
        )
        self.set_concat_paths()

        if self.concat:
            self.concat_ds()
            if save_concat:
                self.save_concat_to_disk()
        else:
            try:
                self.open_concat_files()
            except:
                print('cant open')
        self.get_merged_ds()
        if get_clusters:
            self.get_clusters_r()
        if get_clusters is not True:
            self.merged_ds = xr.open_dataset(self.merged_path)

        self.set_cluster_flags()

        self.add_conc_vars()

        #

    def add_conc_vars(self):
        CPer = co.CPer
        tot = self.merged_ds[co.CONC].sum(dim=[co.R_CENTER, co.TH_CENTER])
        self.merged_ds[CPer] = self.merged_ds[co.CONC] / tot * 100
        CC = co.CC
        CCPer = co.CCPer
        self.merged_ds[CC] = self.merged_ds[co.CONC] / self.merged_ds[co.GA]
        tot = self.merged_ds[CC].sum(dim=[co.R_CENTER, co.TH_CENTER])
        self.merged_ds[CCPer] = self.merged_ds[CC] / tot * 100

    def set_cluster_flags(self):
        fls = self.merged_ds[co.ClusFlag].to_series().dropna().unique()
        fls.sort()
        self.cluster_flags = fls

    def get_clusters_r(self, coarsen_time=4, min_clus=2, max_clus=15):
        mer = self.merged_ds
        ar = mer[co.CONC]
        ar.load()
        ar = ar.coarsen(**{co.RL: coarsen_time}).sum()
        ar.name = co.CONC
        ar1 = ar.dropna(dim=co.RL)
        df = ar1.reset_coords()[[co.CONC]].to_dataframe().unstack(co.RL)
        dfn = df.copy()
        dfn[co.CONC] = normalize(df[co.CONC])
        rnc = rpackages.importr('NbClust')
        trim_df = dfn[dfn[co.CONC].sum(axis=1) > 0]
        trim_vals = trim_df[co.CONC].values
        r, c = trim_vals.shape
        m = robjects.r.matrix(
            robjects.FloatVector(trim_vals.T.flatten()),
            nrow=r
        )
        res = rnc.NbClust(data=m, distance="euclidean",
                          method='kmeans',
                          **{'min.nc': min_clus, 'max.nc': max_clus},
                          index="all")
        flags = np.array(res[3]).copy()
        trim_df[co.ClusFlag] = flags
        mer[co.ClusFlag] = trim_df[co.ClusFlag].to_xarray()
        fa.compressed_netcdf_save(mer,self.merged_path)



    def get_merged_ds(self):
        i = slice(0, None)
        l2M = 24
        l2m = 10
        l1M = None
        l1m = 13
        d1 = self.dasks_dic[self.d1][{co.RL: i}][{co.R_CENTER: slice(l1m, l1M)}]
        d2 = self.dasks_dic[self.d2][{co.RL: i}][{co.R_CENTER: slice(l2m, l2M)}]
        mer = xr.merge([d1, d2])
        self.merged_ds = mer

    def open_concat_files(self):
        dasks_dic = {}
        for d in self.doms:
            dasks_dic[d] = xr.open_mfdataset(
                self.concat_paths[d],
                concat_dim=co.RL,
                chunks={co.RL: 48}
            )
        self.dasks_dic = dasks_dic

    def save_concat_to_disk(self):
        os.makedirs(self.combined_path, exist_ok=True)
        for d in self.doms:
            fa.compressed_netcdf_save(
                self.dasks_dic[d], self.concat_paths[d]
            )

    def concat_ds(self):
        self.list_d1 = glob.glob(self.source_path + self.d1 + '*')
        self.list_d1.sort()
        self.list_d2 = glob.glob(self.source_path + self.d2 + '*')
        self.list_d2.sort()
        self.get_dask_ds()

    def set_concat_paths(self):
        concat_paths = {}
        for d in self.doms:
            concat_paths[d] = os.path.join(self.combined_path, d + '.nc')
        self.concat_paths = concat_paths

    def get_dask_ds(self):
        self.dask_ds_01 = xr.open_mfdataset(self.list_d1, concat_dim=co.RL)
        self.dask_ds_02 = xr.open_mfdataset(self.list_d2, concat_dim=co.RL)
        dasks = [self.dask_ds_01, self.dask_ds_02]
        dask_dic = {}
        for d, ds in zip(self.doms, dasks):
            dask_dic[d] = ds
        self.dasks_dic = dask_dic

    def plot_rel_per_day(self,dom):
        dat = 'date'
        ds = self.dasks_dic[dom]
        ds[dat]=ds[co.RL].dt.round('D')
        fd = ds[[dat]]
        fd.swap_dims({co.RL:dat}).reset_coords(co.RL).groupby(dat).count()[co.RL].plot()

    def plot_clusters_inlfuence(self,ylab=False):
        len_clus = len(self.cluster_flags)
        colors = COLORS
        fig,axs = plt.subplots(3,4,sharex=True,sharey=True,figsize=(15,10))
        axf = axs.flatten()
        for i in range(len_clus):
            ax = axf[i]
            self.plot_cluster_influence_i(colors, i, ax,
                                          ylab=ylab)
        for ax in axf:
            ax.grid(True)
        fig.autofmt_xdate()
        return fig

    def plot_cluster_influence_i(self,
                                 colors, i,
                                 ax=None,
                                 ylab=False
                                 ):
        if ax==None:
            fig, ax = plt.subplots()

        color = colors[i]
        clus = self.cluster_flags[i]
        boo = self.merged_ds[co.ClusFlag] == clus
        #     fig,ax = plt.subplots()
        self.merged_ds.where(boo)[co.CPer].sum(dim=[co.R_CENTER, co.TH_CENTER]).plot(color=color, ax=ax)
        ax.set_xlabel('release time (utc)')
        if ylab is not False:
            ax.set_ylabel(ylab)
        ax.set_title('cluster {}'.format(clus))
        ax.grid(True,'both')
        return ax


