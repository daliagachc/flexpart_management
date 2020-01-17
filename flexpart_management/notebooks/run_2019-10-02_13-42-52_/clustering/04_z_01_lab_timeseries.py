# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
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

# %% [markdown]
# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# %%
# %% [markdown]
# imports
# %%

from useful_scit.imps import *
# noinspection PyUnresolvedReferences
import matplotlib.colors
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
# noinspection PyUnresolvedReferences
import flexpart_management.modules.flx_array as fa
# %%
import flexpart_management.modules.clustering_funs as cfuns
from flexpart_management.modules.clustering_funs import (
    add_total_per_row ,
    add_time_per_row ,
    )

# import flexpart_management.modules.clustering_funs as cfuns
def main():
    # plt.rcParams[ 'figure.facecolor' ] = 'white'
    co.LAB = 'lab'

    # plt.style.use('seaborn-whitegrid')
    # plt.rcParams["legend.frameon"] = True
    # plt.rcParams["legend.fancybox"] = True

    # %%
    # def main() :

    log.ger.setLevel( log.log.DEBUG )

    # %%
    # noinspection PyUnusedLocal,PyShadowingNames
    def open_if_taito() :
                     # noinspection SpellCheckingInspection
                     path = \
                     '/homeappl/home/aliagadi/wrk/DONOTREMOVE' \
                     '/flexpart_management_data/runs/' \
                     'run_2019-10-02_13-42-52_/' \
                     'log_pol/run_2019-10-02_13-42-52_'
                     # flp = FLP.FlexLogPol(path,concat=True)
                     # flp_instance = FLP.FlexLogPol(path,concat=False)
                     selfFLP = FlexLogPol.FlexLogPol(
                     path ,
                     # concat=True,
                     concat=False ,
                     get_clusters=False ,
                     # open_merged=False,
                     open_merged=True ,
                     # merge_ds=False ,
                     # merge_ds=True ,
                     clusters_avail=False ,

                     # postprocess set to false since we are opening the re interpolated
                     # version
                     postprocess=False ,

                     use_new_merge_fun=True ,

                     # set to false bc already done in the saved version
                     filter_r_min_max=False ,
                     )
                     selfFLP.get_list_datasets_saved()
                     # noinspection PyUnresolvedReferences
                     ds = selfFLP.open_ds_version( 'ds_clustered_18.nc' )
                     return selfFLP , ds


    # %%
    # selfFLP,ds = open_if_taito()
    path = '/Users/diego/flexpart_management/flexpart_management/tmp_data' \
       '/ds_clustered_18.nc'
    ds = xr.open_dataset( path )
    # %%
    # %%
    # %%
    conc_lab = 'CONC_smooth_t_300_z_25_r_100_th_50'
    new_lab_p = 'conc_smooth_p'
    new_lab_p_t = 'conc_smooth_p_t'
    add_total_per_row( ds , conc_lab , new_lab_p )
    add_time_per_row( ds , conc_lab , new_lab_p_t )
    # print( da_tot )

    # %%
    # ds[new_lab_p].sum([co.RL,co.ZM],keep_attrs=True).plot()
    # plt.show()
    # ds[new_lab_p_t].sum(fa.get_dims_complement(ds,co.RL),keep_attrs=True).plot()
    # plt.show()
    # %%
    prop_df = pd.read_csv(co.prop_df_path)
    prop_df
    # %%
    conc_tot_ts = 'CONC_tot_ts'
    dim_complement_rl = fa.get_dims_complement(ds['CONC'], co.RL)
    da_tot_ts = ds['CONC'].sum(dim_complement_rl) / 100
    # %%
    ranges = ('SR','SM','MR','LR')
    range_names = ('short range','short-medium range',
                  'medium range', 'long range')
    ri = 0
    for ri in range(len(ranges)):
        plot_multi_time_series(
            da_tot_ts, dim_complement_rl, ds, prop_df, ranges, range_names, ri,
            save=True
        )

    # %%
    # %%



    # %%

    # %%

    # %%

# %%

def plot_multi_time_series(da_tot_ts, dim_complement_rl, ds, prop_df, ranges,
                           range_names, ri, save=False):
    prop_df_ = prop_df[prop_df['range'] == ranges[ri]]
    col = ucp.cc[ri]
    len_df = len(prop_df_)
    f, axs = plt.subplots(len_df, sharex=True, sharey=True,
                          figsize=(4, .8 * len_df+.5))
    axf = axs.flatten()
    for ii, (l, r) in enumerate(prop_df_.iterrows()):
        i = r['cluster_i']
        da_lab = ds['CONC'].where(ds['lab'] == i).sum(
            dim_complement_rl) / da_tot_ts

        # cfuns.plot_lab_time_series(da_lab=da_lab)
        df_lab = da_lab.reset_coords(drop=True).to_dataframe()
        ax: plt.Axes = axf[ii]
        df_lab['CONC'].plot(ax=ax, c=col)
        # ax.grid(linestyle=':')
        # ax.set_xlabel(None)
        ax.annotate(r['short_name'],(1,1),xycoords='axes fraction',
                    verticalalignment='top',xytext=(-2,-2),
                    horizontalalignment='right',
                    textcoords='offset points'
                    )
        if ii is 0:
            ax.set_title(range_names[ri])

    ax.set_ylabel('SRR [%]')

    f.tight_layout()
    # f.suptitle(range_names[ri])
    #
    ax.annotate('SSR [%]',(0.03,.5),rotation=90,xycoords='figure fraction',
                horizontalalignment = 'left',
                verticalalignment='center'
                )
    ax.set_ylabel(None)
    # f.tight_layout()
    #
    # ax.annotate('release time',(0.5,.01),rotation=0,
    #             xycoords='figure fraction',
    #             horizontalalignment = 'center'
    #             )
    #
    # ax.annotate(range_names[ri],(0.5,1),rotation=0,
    #             xycoords='figure fraction',
    #             horizontalalignment = 'center',
    #             verticalalignment='top'
    #             )
    # f.subplots_adjust(left=.1)


    f:plt.Figure
    # f.suptitle()
    plt.show()
    if save:
        path = '/Users/diego/flexpart_management/flexpart_management/victoria_trento/figures'
        name = ranges[ri]+'time_series'+'.pdf'
        f.savefig(os.path.join(path,name))

# plot_multi_time_series(da_tot_ts, dim_complement_rl, ds, prop_df, ranges,range_names, 3)
