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
    ls = 'lab_name'
    con = 'CONC_smooth_t_300_z_25_r_100_th_50'
    con = co.CONC
    # %%
    da = lfc.get_da(con)
    # %%
    df = lfc.get_df(da, ls)
    # %%
    ord = lfc.get_nc18_order()
    df = df.loc[ord['18_NC']]
    df['pw'] = ord.set_index('18_NC')['06_NC']
    # %%

    df.to_excel(pjoin(co.tmp_data_path,'redo_nc18_df.xls'))
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
