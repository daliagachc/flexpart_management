# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
from sklearn.preprocessing import normalize
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from pprint import pprint
from sklearn.cluster import KMeans
import warnings
from scipy.ndimage import gaussian_filter
import matplotlib

ZN = 6

Z2 = 30002

Z1 = 1000

COLORS = [*sns.color_palette('Set1', n_colors=9, desat=.5),
          sns.color_palette('Dark2', n_colors=6, desat=.8)[-1],
          *sns.color_palette('Dark2', n_colors=6, desat=.8)[:-1]
          ]

CON_COLS = [co.CONC, co.CPer, co.CC, co.CCPer]


class FlexLogPol:
    source_path: str = None
    d1 = 'd01'
    d2 = 'd02'
    h1 = 'h01'
    h2 = 'h02'
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
    coarsen_par = None
    colors = COLORS
    head_rel_path = 'heads'
    head_dic_ds = {}
    h1_ds = None
    h2_ds = None

    l2M = 24
    l2m = 10
    l1M = None
    l1m = 13
    merged_head_ds = None

    def __init__(self,
                 source_path: str,
                 concat=False,
                 save_concat=True,
                 get_clusters=False,
                 open_merged=False,
                 clusters_avail=False,
                 coarsen_par=4
                 ):

        # SET CONSTANT ATTRIBUTES
        self.coarsen_par = coarsen_par
        self.save_concat = save_concat
        self.concat = concat
        self.doms = [self.d1, self.d2]
        self.source_path = os.path.join(source_path, '')
        self.combined_path = os.path.join(self.source_path,
                                          self.combined_path)
        self.merged_path = os.path.join(
            self.combined_path,
            'merged_ds.nc'
        )
        self.set_concat_paths()

        ###

        if self.concat:
            self.concat_ds()
            if save_concat:
                self.save_concat_to_disk()
        else:
            try:
                self.open_concat_files()
            except:
                print('cant open')

        # def ret(self):pass
        if open_merged:
            self.merged_ds = xr.open_dataset(self.merged_path)
        else:
            self.get_merged_ds()

        if get_clusters:
            self.get_clusters_r(coarsen_time=self.coarsen_par)

        if clusters_avail:
            self.set_cluster_flags()

        self.set_z_vols()
        self.add_conc_vars()

        self.add_topo_to_merge_ds()

        # i = 1
        # self.plot_cluster_grid(i)

        #

    def add_topo_to_merge_ds(self):
        '''
        adds topography to the input ds from the merged head ds.
        :return:
        '''
        print('starting')
        log.ger.debug('starting')
        self.get_all_head_ds()
        log.ger.debug('heads got')
        self.merge_log_pol_heads()
        log.ger.debug('merge pol heads got')
        try:
            topo_ = self.merged_head_ds[co.TOPO].mean(co.ZMID)
            log.ger.debug('manage to add mean zmid')
        except:
            topo_ = self.merged_head_ds[co.TOPO]
        mds_: xr.Dataset = self.merged_ds
        mds_[co.TOPO] = topo_
        mds_[co.TOPO].values = topo_.values
        self.merged_ds = mds_.assign_coords(**{co.TOPO: mds_[co.TOPO]})

    def get_all_head_ds(self):
        head_path = os.path.join(self.source_path, self.head_rel_path)
        self.get_head_ds(self.d1, head_path, self.h1)
        self.get_head_ds(self.d2, head_path, self.h2)
        self.h1_ds = self.head_dic_ds[self.h1]
        self.h2_ds = self.head_dic_ds[self.h2]

    def get_head_ds(self, d1, head_path, lh1):
        h1 = glob.glob(
            os.path.join(head_path, 'header*' + d1 + "*.nc")
        )[0]
        h1 = xr.open_dataset(h1)
        h1 = get_log_polar_coords_topo(h1)
        self.head_dic_ds[lh1] = h1

    def plot_cluster_grid(self,
                          i,
                          par_to_plot=co.COL
                          ):
        fs = np.array([11, 13]) * .7
        fig_ops = dict(figsize=fs)
        fig: plt.Figure = plt.figure(**fig_ops)
        rows = 4
        cols = 2
        perM = .9
        rmap = rows - 2
        cplot = 1
        ax = fig.add_axes([0, .7, .4, .4], projection=co.PROJ, )
        self.plot_cluster_map(
            i=i,
            log_plot_dic=dict(
                perM=perM
            ),
            map_dic=dict(
                ax=ax,
            ),

            par_to_plot=par_to_plot
        )
        fa.add_chc_lpb(ax)

        self.plot_lapaz_rect(ax)

        ax = fig.add_axes([.5, .7, .4, .4], projection=co.PROJ, )
        self.plot_cluster_map(
            i=i,
            log_plot_dic=dict(
                perM=perM,
                colorbar=True,
            ),
            map_dic=dict(
                ax=ax,
                lalo_extent=co.LALO_LAPAZ
            ),

            par_to_plot=par_to_plot
        )
        fa.add_chc_lpb(ax)

        ax = fig.add_subplot(rows, cplot, (rows * cplot) - 2)
        self.plot_clust_height(ax, i, perM, par_to_plot=par_to_plot)

        ax = fig.add_subplot(rows, cplot, (rows * cplot) - 1)
        self.plot_absolute_height(ax=ax, i=i, perM=perM)

        ax = fig.add_subplot(rows, cplot, (rows * cplot) - 0)
        self.plot_cluster_influence_i(i=i,
                                      ax=ax,
                                      par_to_plot=par_to_plot,
                                      )
        fig.subplots_adjust(wspace=.4, hspace=.6)

        return fig

    def plot_clust_height(self, ax: plt.Axes, i,
                          perM,
                          drop_zero=True,
                          par_to_plot=co.COL):
        clus = self.cluster_flags[i]
        boo = self.merged_ds[co.ClusFlag] == clus
        ar = self.merged_ds[par_to_plot].where(boo)
        com = fa.get_dims_complement(ar, [co.R_CENTER, co.ZM])
        ar = ar.sum(dim=com)
        if par_to_plot is co.CPer:
            ar = ar / self.merged_ds[par_to_plot].sum() * 100
        if drop_zero:
            ar = ar.where(ar > 0)
        q = ar.quantile(perM)
        lab = "km from CHC"
        ar[lab] = ar[co.R_CENTER] * 100
        ar = ar.swap_dims({co.R_CENTER: lab})
        try:
            ar.name = co.PLOT_LABS[par_to_plot]
        except:
            pass
        ar.plot(
            cmap=fa.get_custom_cmap(self.colors[i]),
            vmin=0,
            vmax=q,
            ax=ax,
            x=lab,
        )
        ax.set_yscale('log')
        ax.set_ylim(100, 20000)
        ax.set_xscale('log')
        ax.set_xlim(.05 * 100, 30 * 100)
        ax.grid(True, 'major', axis='y')
        ax.grid(True, 'both', axis='x')
        ax.set_ylabel(co.PLOT_LABS[co.ZM])

    def plot_lapaz_rect(self, ax):
        fa.plot_lapaz_rect(ax)

    def add_conc_vars(self):
        '''
        adds extra CON variables derived from original co.CONC
        :return:
        '''
        CPer = co.CPer
        dim_complement = fa.get_dims_complement(self.merged_ds, co.RL)
        tot = self.merged_ds[co.CONC].sum(dim=dim_complement)
        self.merged_ds[CPer] = self.merged_ds[co.CONC] / tot * 100
        CC = co.CC
        CCPer = co.CCPer
        if co.VOL in list(self.merged_ds.coords):
            self.merged_ds[CC] = self.merged_ds[co.CONC] / self.merged_ds[
                co.VOL]
            pprint('using vol for conc')
        else:
            pprint('using area for conc')
            self.merged_ds[CC] = self.merged_ds[co.CONC] / self.merged_ds[co.GA]
        tot = self.merged_ds[CC].sum(dim=dim_complement)
        self.merged_ds[CCPer] = self.merged_ds[CC] / tot * 100

    def set_cluster_flags(self):
        fls = self.merged_ds[co.ClusFlag].to_series().dropna().unique()
        fls.sort()
        self.cluster_flags = fls

    def get_clusters_r(self,
                       coarsen_time=4,
                       min_clus=2,
                       max_clus=15,
                       save_flags=True,
                       stop_before_clust=False
                       ):

        df = self.get_vector_df_for_clustering(coarsen_time)
        dfn = df.copy()
        dfn[co.CONC] = normalize(df[co.CONC])

        trim_df: pd.DataFrame = dfn[dfn[co.CONC].sum(axis=1) > 0]

        if stop_before_clust:
            return trim_df, df

        flags, res = self.r_cluster_wrap(trim_df, min_clus, max_clus)
        trim_df[co.ClusFlag] = flags
        self.merged_ds[co.ClusFlag] = trim_df[co.ClusFlag].to_xarray()
        if save_flags:
            fa.compressed_netcdf_save(self.merged_ds, self.merged_path)
        return trim_df

    def get_vector_df_for_clustering(self, coarsen_time, ar=False):
        if ar is False:
            ar: xr.Dataset = self.merged_ds[co.CONC].copy()
            ar.load()
        ar = ar.coarsen(**{co.RL: coarsen_time}).sum()
        ar.name = co.CONC
        ar1 = ar.dropna(dim=co.RL)
        df = ar1.reset_coords()[[co.CONC]].to_dataframe().unstack(co.RL)
        return df

    def r_cluster_wrap(self, trim_df, min_clus, max_clus):
        trim_vals = trim_df[co.CONC].values
        r, c = trim_vals.shape
        m = robjects.r.matrix(
            robjects.FloatVector(trim_vals.T.flatten()),
            nrow=r)
        pprint('starting to cluster')
        rnc = rpackages.importr('NbClust')
        res = rnc.NbClust(data=m, distance="euclidean",
                          method='kmeans',
                          **{'min.nc': min_clus, 'max.nc': max_clus},
                          index="all")
        pprint('done clustering')
        flags = np.array(res[3]).copy()
        return flags, res

    def python_cluster(self,
                       n_cluster=8,
                       df=False,
                       return_df=False,
                       random_state=1234
                       ):
        if df is False:
            df = self.get_vector_df_for_clustering(self.coarsen_par)
        nor = np.linalg.norm(df, axis=1)
        thre = np.quantile(nor, .5) * .01
        new_df = df[nor > thre].copy()
        new_df[co.CONC] = normalize(new_df[co.CONC])

        kmeansO = KMeans(
            n_clusters=n_cluster,
            random_state=random_state,
            max_iter=500,
            n_init=20
        )

        kmeans = kmeansO.fit(new_df[co.CONC])
        df[co.ClusFlag] = kmeans.predict(df[co.CONC])
        if return_df:
            return df
        self.merged_ds[co.ClusFlag] = df[co.ClusFlag].to_xarray()
        self.set_cluster_flags()

    def get_merged_ds(self):
        i = slice(0, None)
        l2M = self.l2M
        l2m = self.l2m
        l1M = self.l1M
        l1m = self.l1m
        d1 = self.dasks_dic[self.d1][{co.RL: i}][{co.R_CENTER: slice(l1m, l1M)}]
        d2 = self.dasks_dic[self.d2][{co.RL: i}][{co.R_CENTER: slice(l2m, l2M)}]
        mer = xr.merge([d1, d2])
        self.merged_ds = mer
        fa.compressed_netcdf_save(self.merged_ds, self.merged_path)

    def open_concat_files(self):
        dasks_dic = {}
        for d in self.doms:
            dasks_dic[d] = xr.open_mfdataset(
                self.concat_paths[d],
                concat_dim=co.RL,
                chunks={co.RL: 48},
                combine='by_coords'
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

    def plot_rel_per_day(self, dom):
        dat = 'date'
        ds = self.dasks_dic[dom]
        ds[dat] = ds[co.RL].dt.round('D')
        fd = ds[[dat]]
        fd.swap_dims({co.RL: dat}).reset_coords(co.RL).groupby(dat).count()[
            co.RL].plot()

    def plot_clusters_inlfuence(self, ylab=False, cols=2):
        len_clus = len(self.cluster_flags)
        colors = self.colors
        # cols = 2
        rows = int(np.ceil((len_clus / cols)))
        # noinspection PyTypeChecker
        fig, axs = plt.subplots(rows, cols,
                                sharex=True,
                                sharey=True,
                                figsize=(15, 10))
        axf = axs.flatten()
        for i in range(len_clus):
            ax = axf[i]
            self.plot_cluster_influence_i(colors=colors, i=i, ax=ax,
                                          ylab=ylab)
        for ax in axf:
            ax.grid(True)
        fig.autofmt_xdate()
        return ax

    def plot_cluster_influence_i(self,
                                 colors=None,
                                 i=0,
                                 ax=None,
                                 ylab=False,
                                 par_to_plot=co.CPer,
                                 ):
        if colors == None:
            colors = self.colors

        if ax == None:
            fig, ax = plt.subplots()

        color = colors[i]
        clus = self.cluster_flags[i]
        boo = self.merged_ds[co.ClusFlag] == clus
        #     fig,ax = plt.subplots()

        c_per_ = self.merged_ds.where(boo)[par_to_plot]
        comp_dims = fa.get_dims_complement(c_per_, co.RL)
        c_per_.sum(dim=comp_dims).plot(color=color, ax=ax)
        ax.set_xlabel('arrival time (utc)')
        if ylab is not False:
            ax.set_ylabel(ylab)
        else:
            ax.set_ylabel(co.PLOT_LABS[par_to_plot])
        ax.set_title('cluster {}'.format(clus))
        ax.grid(True, 'both')
        return ax

    def set_z_vols(self):
        '''
        adds z parameters to the ds.
            - also icludes volume
        :return:
        '''
        self.merged_ds = fa.add_zbot(self.merged_ds)
        self.merged_ds = fa.add_zmid(self.merged_ds)
        self.merged_ds = fa.add_zlength_m(self.merged_ds)
        self.merged_ds = fa.add_volume(self.merged_ds)
        # sets the dim to be co.ZM rather than origianl co.ZT
        self.merged_ds = self.merged_ds.swap_dims({co.ZT: co.ZM})

        self.merged_ds: xr.Dataset

    def reset_z_levels(self):

        zlin = self.get_zlin()
        try:
            self.merged_ds = self.merged_ds.swap_dims({co.ZM: co.ZT})
        except:
            pass
        new_ds = []
        for z in range(len(zlin) - 1):
            res = self.merged_ds.sel(**{co.ZT: slice(zlin[z], zlin[z + 1] - 1)})
            maxZ = res[co.ZT].max()
            res = res.sum(co.ZT)
            res[co.ZT] = maxZ
            res = res.assign_coords(**{co.ZT: res[co.ZT]})
            res = res.expand_dims(co.ZT)

            new_ds.append(res)
        new_ds = xr.concat(new_ds, dim=co.ZT)
        new_ds.load()
        self.merged_ds = new_ds
        self.set_z_vols()
        self.add_conc_vars()

    def get_zlin(self):
        z1 = Z1
        z2 = Z2
        zn = ZN
        zlog = np.linspace(np.log(z1), np.log(z2), zn)
        zlin = [0, *np.e ** zlog]
        return zlin

    def plot_conc_over_time(self):
        comp = fa.get_dims_complement(self.merged_ds, co.RL)
        res = self.merged_ds[co.CONC].sum(dim=comp)
        res.plot()

    def setCOL(self):
        COL = co.COL
        self.merged_ds[COL] = self.merged_ds[co.CONC] / np.sqrt(
            self.merged_ds[co.GA])

    def plot_cluster_map(self,
                         i,
                         log_plot_dic={},
                         map_dic={},
                         par_to_plot=co.COL,
                         ):
        clus = self.cluster_flags[i]
        boo = self.merged_ds[co.ClusFlag] == clus

        ax = fa.get_ax_bolivia(**map_dic)
        #     fig,ax = plt.subplots()
        warnings.simplefilter('ignore')

        ar = self.merged_ds.where(boo)[par_to_plot]
        com = fa.get_dims_complement(ar, [co.R_CENTER, co.TH_CENTER])
        ar = ar.sum(dim=com)
        if par_to_plot is co.CPer:
            ar = ar / self.merged_ds[par_to_plot].sum() * 100
        cmap = fa.get_custom_cmap(self.colors[i])
        def_dic = dict(
            ax=ax,
            name=par_to_plot,
            perM=.95,
            quantile=True,
            colorbar=False,
            patch_args={'cmap': cmap}
        )

        com_dic = {**def_dic, **log_plot_dic}
        fa.logpolar_plot(ar,
                         **com_dic
                         )

    def merge_log_pol_heads(self):
        l2M = self.l2M
        l2m = self.l2m
        l1M = self.l1M
        l1m = self.l1m
        d1 = self.h1_ds[{co.R_CENTER: slice(l1m, l1M)}]
        d2 = self.h2_ds[{co.R_CENTER: slice(l2m, l2M)}]
        mer = xr.merge([d1, d2])
        self.merged_head_ds = mer.copy()

    def plot_absolute_height(self,
                             i,
                             ax=None,
                             perM=.95,
                             drop_zero=True,
                             par_to_plit=co.COL
                             ):
        mer = self.merged_ds.copy()
        # i = 6
        clus = self.cluster_flags[i]

        H = co.H
        fla = co.FLAGS
        HC = 'H*CONC'

        ver_area = 'VER_AREA'
        log_center = np.log(mer[co.R_CENTER])
        dis = log_center - \
              log_center.shift({co.R_CENTER: 1})
        dis = dis.median()
        l1 = log_center - dis / 2
        l2 = log_center + dis / 2
        l1 = np.e ** l1
        l2 = np.e ** l2
        r_dis = (l2 - l1) * 100000
        zlen = 500
        ar = np.arange(zlen / 2, 20000, zlen)

        mer = mer[[co.CONC, fla, co.TOPO]]

        # return merged_ds

        mer = mer.where(mer[fla] == clus, 0)

        mer['c/v'] = mer[co.CONC] / mer[co.VOL]

        mer = mer.interp(**{co.ZM: ar})

        mer[co.VOL] = mer[co.GA] * zlen
        mer[co.CONC] = mer['c/v'] * mer[co.VOL]

        mer[H] = mer[co.TOPO] + mer[co.ZM]

        mer[HC] = mer[H] * mer[co.CONC]

        var = [co.CONC, HC]
        com = fa.get_dims_complement(mer, [co.R_CENTER, co.ZM])
        ms = mer[var].sum(com)

        ms[ver_area] = ms[co.ZLM] * r_dis

        # ms:xr.DataArray = ms/ms[ver_area]

        ms[co.CONC] = ms[co.CONC].where(ms[co.CONC] > 0, 0)

        # ms = ms*zlen*r_dis

        ms[H] = ms[HC] / ms[co.CONC]

        def find_nearest(value):
            #     ar = self.get_zlin()
            array = np.asarray(ar)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        ms[H] = xr.apply_ufunc(find_nearest, ms[H], vectorize=True)

        hs = ms.to_dataframe().groupby([H, co.R_CENTER]).sum()[
            co.CONC].to_xarray()

        lab = "km from CHC"
        hs[lab] = hs[co.R_CENTER] * 100
        hs = hs.swap_dims({co.R_CENTER: lab})

        hs1 = hs.interp(**{H: ar})
        hs1 = hs1.combine_first(hs)

        if drop_zero:
            hs1 = hs1.where(hs1 > 0)

        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 5))

        hs1 = hs1 / self.merged_ds[co.CONC].sum() * 100
        hs1.name = co.CPer
        q = hs1.quantile(perM)

        hs1.name = co.PLOT_LABS[co.CPer]

        hs1.plot(
            cmap=fa.get_custom_cmap(self.colors[i]),
            vmin=0,
            vmax=q,
            ax=ax,
            x=lab,
        )
        ax.set_ylim(100, 20000)
        ax.set_xscale('log')
        ax.set_xlim(.05 * 100, 30 * 100)
        ax.grid(True, 'major', axis='y')
        ax.grid(True, 'both', axis='x')
        ax.set_ylabel(co.PLOT_LABS[co.H])

    def plot_hout_influence(self, i,
                            log='False',
                            pM=None
                            ):
        # %%
        lt = 'Local Time'
        ds = self.merged_ds.copy()

        ds[lt] = np.mod(ds[co.RL].dt.hour - 3.5, 24)
        ds = ds.assign_coords(**{lt: ds[lt]})
        dsLP = ds.where(self.merged_ds[co.FLAGS] == i)
        com = fa.get_dims_complement(dsLP, co.RL)
        conLP = dsLP[co.CONC].sum(com)
        conTot = ds[co.CONC].sum(com)
        conLP = conLP / conTot * 100
        cl = 'clog'
        conLP = conLP.where(conLP > 0)
        conLP = np.log(conLP)
        conLP.name = cl

        df = conLP.to_dataframe()
        gp = df.groupby(lt)
        desc = gp.describe()[cl]

        # %%
        labs = ['25%', '50%', '75%', 'mean']

        desc = desc[labs]

        desc = np.e ** desc
        if pM is None:
            yM = None
        else:
            yM = desc.quantile(pM).max()

        # %%
        fig, ax = plt.subplots()
        c = self.colors[i]
        ax.plot(desc.index, desc[labs[1]], color=c, label=labs[1])
        ax.plot(desc.index, desc[labs[3]], color='k', label=labs[3])
        ax.fill_between(desc.index, desc[labs[0]], desc[labs[2]], color=c,
                        alpha=.2, label=labs[0] + '-' + labs[2])
        ax.legend(loc='upper left')
        ax.set_xlabel(lt)
        ax.set_ylabel(co.PLOT_LABS[co.CPer])
        ax.grid(True)
        tickrange = np.arange(0, 25, 3)
        ax.set_xticks(tickrange)
        ax.set_title('cluster {}'.format(i))
        if log:
            ax.set_yscale('log')
        ax.set_ylim(None, yM)
        return ax

    def filter_hours_with_few_mea(
            self,
            threshold=2e5,
            interpolate = True
    ):
        diag_dic = {}
        sum_coords = [co.ZM, co.R_CENTER, co.TH_CENTER]
        sum_ds = self.merged_ds[co.CONC].sum(sum_coords)
        bool_thre = sum_ds[sum_ds > threshold]

        filtered_merged_ds: xr.Dataset = self.merged_ds.where(bool_thre)
        diag_dic['rel 0st filt'] = self.merged_ds.dims[co.RL]
        diag_dic['rel 1st filt'] = filtered_merged_ds.dims[co.RL]

        filtered_merged_ds1:xr.Dataset = filtered_merged_ds.resample(
            **{co.RL: '1H'}
        ).mean()

        diag_dic['rel 2st filt'] = filtered_merged_ds1.dims[co.RL]
        # print(1)

        if interpolate:

            filtered_merged_ds1:xr.Dataset = filtered_merged_ds1.interpolate_na(
                dim=co.RL,
            )

        # return filtered_merged_ds1,diag_dic

        return filtered_merged_ds1


# ------------------------------------------------------------------------------------------

def smooth_merged_ds(
        ds
):
    '''
    Returns
    -------
    '''
    for col in CON_COLS:
        ds[col] = smooth_col(ds[col])
    return ds


def smooth_col(da, t=3, z=.5, r=1, th=1):
    # da = ds[col]
    dag = da.isel(**{co.R_CENTER: slice(1, None)})
    vals = dag.values
    print(vals.shape)
    n_vals = gaussian_filter(
        vals,
        sigma=[t, z, r, th],
        mode=['nearest', 'nearest', 'nearest', 'wrap']
    )
    dag.values = n_vals
    return dag


def get_log_polar_coords_topo(
        head_ds,
        coords_to_keep=[co.WE, co.SN],
        rounding_vals=[co.ROUND_R_LOG, co.ROUND_TH_RAD],
        keep_list=[],
        keep_vars=[co.TOPO]
):
    keep_coords = coords_to_keep
    head_ds = fa.add_lat_lot(head_ds)
    head_ds = head_ds[keep_vars]
    complement_coords = fa.get_dims_complement(head_ds, keep_coords)
    head_ds = head_ds.mean(dim=complement_coords)

    val = rounding_vals
    lp_ds = xr.Dataset()
    for v in keep_vars:
        lp_ds[v] = fa.data_array_to_logpolar(
            head_ds[v],
            *val,
            dim2keep=keep_list,
            fun='mean'
        )

    return lp_ds


def zlog_round():
    return (np.log(Z2) - np.log(Z1)) / ZN
