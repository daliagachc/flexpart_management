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
import flexpart_management.notebooks.six_clusters_centroids. \
    six_clusters_centroids_lfc as lfc
from flexpart_management.notebooks.six_clusters_centroids. \
    six_clusters_centroids_lfc import *


# %%

def main():
    # %%
    ls = 'lab_nc06'
    con = 'CONC_smooth_t_300_z_25_r_100_th_50'
    con = co.CONC
    # %%
    da = lfc.get_da(con, ls)
    # %%


    # %%

    df = lfc.get_df(da, ls)
    # %%
    _cols = df.columns
    _ord = ['rrs','dis','agl','asl','ratio']
    df1 = df[_ord]


    df1.to_excel(pjoin(co.tmp_data_path,'nc06_props.xls'))
    df.to_excel(pjoin(co.tmp_data_path,'nc06_props_all.xls'))
    # %%
    f = lfc.plot_nc6_vert_props(df)
    f.savefig(pjoin(co.paper_fig_path,'cluster_medeoids_nc6_7_25.pdf'))
    # %%


    # %%
    lfc.get_th_dic(da,ls,['07_PW'])

    # %%
    # %%
    # %%
    # %%
    # %%
    # %%
    # %%





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
