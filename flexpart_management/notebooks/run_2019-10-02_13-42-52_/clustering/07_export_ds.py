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
from itertools import cycle

from useful_scit.imps import *
# noinspection PyUnresolvedReferences
import matplotlib.colors
import flexpart_management.modules.FlexLogPol as FlexLogPol
import flexpart_management.modules.constants as co
# noinspection PyUnresolvedReferences
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.clustering_funs as cfuns
from flexpart_management.modules.clustering_funs import (
    add_total_per_row ,
    add_time_per_row ,
    )
# %%

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

def get_time_series(variable , ds, n_clusters=18, lab_variable=co.LAB):
    ds_lab_dic = {}
    for ci in range(n_clusters):
        ds_lab = ds[[variable]].where(ds[lab_variable] == ci).copy()
        ds_lab_dic[ci] = ds_lab.copy()
    # %%
    ll = []
    for i in range(n_clusters):
        dsum = ds_lab_dic[i].sum([co.R_CENTER, co.TH_CENTER, co.ZM])
        dsum = dsum.expand_dims(**{'lab': [i]})
        ll.append(dsum)
    #
    # %%
    mega_ds = xr.concat(ll, dim='lab')
    # %%
    df_ = mega_ds.to_dataframe()
    return df_
# %%
def main():

    # %%
    # selfFLP,ds = open_if_taito()
    path = '/Users/diego/flexpart_management/flexpart_management/tmp_data' \
       '/ds_clustered_18.nc'
    ds = xr.open_mfdataset( path ,concat_dim=co.RL,combine='nested')
    # %%
    conc_lab = 'CONC_smooth_t_300_z_25_r_100_th_50'
    new_lab_p = 'conc_smooth_p'
    new_lab_p_t = 'conc_smooth_p_t'
    conc = co.CONC
    # %%

    add_total_per_row( ds , conc_lab , new_lab_p )
    add_time_per_row( ds , conc_lab , new_lab_p_t )
    # print( da_tot )

    # %%

    # %%

    # %%
    df_ = get_time_series(conc,ds)
    # %%
    dfu = df_.unstack('lab')
    dfu_sum = dfu.sum(axis=1)
    (dfu.T/dfu_sum*100).T


    # %%
    df1 = df_.unstack(0)

    # %%
    df1_tot = df1.sum(axis=1)
    dfn = (df1.T/df1_tot).T * 100
    # %%
    df_prop = pd.read_csv(co.prop_df_path)
    dfn_cols = dfn['CONC'].columns
    short_name = df_prop.set_index(
        'cluster_i').loc[dfn_cols, 'short_name']
    dfn_c = dfn['CONC']
    dfn_c.columns = short_name
    order_sn = df_prop.sort_values(co.R_CENTER)['short_name'].values
    dfn_c = dfn_c[order_sn]

    # %%
    path_out = os.path.join(co.tmp_data_path,'conc_ts_cluster.csv')
    dfn_c.to_csv(path_out)
    # %%




    # %%

    # noinspection PyUnresolvedReferences
    from bokeh.palettes import Category20_18
    from bokeh.models import Legend
    from bokeh.plotting import figure, output_file, show
    from bokeh.sampledata.stocks import AAPL, IBM, MSFT, GOOG

    p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
    p.title.text = 'Click on legend entries to hide the corresponding lines'

    # for data, name, color in zip([AAPL, IBM, MSFT, GOOG],
    #                              ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):
    legends = []
    for i,sn in enumerate(dfn_c.columns):
        # df = pd.DataFrame(data)
        # df['date'] = pd.to_datetime(df['date'])
        res = p.line(dfn.index,dfn_c[sn],
                     # legend_label=str(i),
               line_width=2, alpha=0.8,
               color = Category20_18[i]
               )
        legends.append((sn,[res]))

    leg1 = Legend(items=legends[:6],click_policy='hide')
    leg2 = Legend(items=legends[6:12],click_policy='hide')
    leg3 = Legend(items=legends[12:18],click_policy='hide')

    # p.legend.location = "right"
    p.add_layout(leg3, 'left')
    p.add_layout(leg2, 'left')
    p.add_layout(leg1,'left')

    # p.legend.click_policy = "hide"

    output_file("/tmp/interactive_legend.html",
                title="interactive_legend.py example",
                mode='inline')

    show(p)
    

    # %%
    df1.to_excel(f'/Users/diego/flexpart_management/flexpart_management/presentations/{new_lab_p}.xls')

    # %%
    N_CLUSTERS = 18
    ds_lab_dic_t = { }
    for ci in range( N_CLUSTERS ) :
        ds_lab = ds[ [ new_lab_p_t ] ].where( ds[ co.LAB ] == ci ).copy()
        ds_lab_dic_t[ ci ] = ds_lab.copy()

    # %%
    i=0
    ll_t = []
    for i in range(N_CLUSTERS):
        dsum = ds_lab_dic_t[i].sum([co.R_CENTER,co.TH_CENTER,co.ZM])
        dsum = dsum.expand_dims(**{'lab':[i]})
        ll_t.append(dsum)

    #

    # %%
    mega_ds = xr.concat(ll_t,dim='lab')

    # %%
    df_ = mega_ds.to_dataframe()

    # %%
    df1 = df_.unstack(0)

    # %%
    df1.to_excel(f'/Users/diego/flexpart_management/flexpart_management/presentations/{new_lab_p_t}.xls')

    # %%

    # %%


