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

from flexpart_management.notebooks.multicluster_main_pathways.multicluster_main_pathways_lfc import *
import \
    flexpart_management.notebooks.multicluster_main_pathways.multicluster_main_pathways_lfc as lfc

from flexpart_management.notebooks.multicluster_main_pathways.multicluster_main_pathways_lfc import \
    n2c, n2m


# %%

def main():
    # %%

    ds = pd.read_hdf(pjoin(co.tmp_data_path, 'multicluster_df.nc'))
    ds

    # %%
    pdf = pd.read_csv(pjoin(co.tmp_data_path, 'prop_df_.csv'))
    ni = pdf.set_index('cluster_i')['short_name']
    ni
    # %%
    nds = pd.merge(ds, ni, left_index=True, right_index=True)
    nds = nds.sort_values(6).set_index('short_name')
    ser_6 = nds[6]

    # %%

    cms = xr.open_dataset(pjoin(co.tmp_data_path, 'clus_medeoid_stats.nc'))
    cms
    # %%
    css = xr.open_dataset(pjoin(co.tmp_data_path, 'cluster_stat_ts.nc'))
    css
    # %%
    allds = fa.open_temp_ds_clustered_18()
    conc_name = 'CONC_smooth_t_300_z_25_r_100_th_50'
    dac = allds[conc_name]
    dac_sum = dac.sum(co.RL).load()
    # %%

    path_colors = co.pathway_colors
    npdf = pdf.set_index('short_name')
    npdf['clus_6'] = ser_6
    npdf['c6_colors'] = npdf['clus_6'].apply(lambda c: path_colors[c])

    npdf['range_color'] = npdf['range'].apply(lambda r: n2c(r))
    npdf['range_marker'] = npdf['range'].apply(lambda r: n2m(r))

    # %%
    table_path = pjoin(co.tmp_data_path, 'combined_cluster_data.xlsx')
    npdf.to_excel(table_path)
    # ! open {table_path}
    # f, ax = plt.subplots()
    # ax:plt.Axes



    # fa.logpolar_plot()

    # %%
    #
    # lfc.create_combined_plot(
    #     conc_name, dac_sum, npdf, path_colors,
    #     f_width=7.25,min_fs=6, out_name='horizontal_clus_desc_7_25_bad.pdf'
    #                          )
    # %%

    lfc.create_combined_plot_simple(
        conc_name, dac_sum, npdf, path_colors,
        f_width=7.25,min_fs=6, out_name='simple_horizontal_clus_desc_7_25.pdf',
        add_patch = False, background_alpha = .8
    )
    plt.show()

if __name__ == '__main__':
    main()

