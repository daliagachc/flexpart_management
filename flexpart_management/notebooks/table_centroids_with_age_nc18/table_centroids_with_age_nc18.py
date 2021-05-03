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
import flexpart_management.notebooks. \
    table_centroids_with_age_nc18.table_centroids_with_age_nc18_lfc as lfc
from flexpart_management.notebooks. \
    table_centroids_with_age_nc18.table_centroids_with_age_nc18_lfc import *


# %%
def main():
    # %%
    ds = xr.open_mfdataset(pjoin(co.tmp_data_path,
                                 'cluster_series_v3.nc'),
                           concat_dim=co.RL, combine='nested')
    # %%
    dfa = lfc.get_plot_df(ds)
    round_dic = lfc.round_dic()

    tp = lfc.TablePlot(dfa, cwidth=7.25/9, rheight=.3,
                       title_size=8,round_dic=round_dic,
                       text_size=8)
    tp.plot_label()
    tp.plot_cols()
    tp.splot.axf[0].set_ylim(-.5, tp.nr + .5)
    df1 = lfc.fix_index(dfa, tp)
    lfc.fix_main_pw(df1, tp)
    lfc.add_blines(tp)

    tp.despine()
    tp.splot.f.tight_layout()
    tp.splot.f.subplots_adjust(wspace=.1)
    tp.splot.f.show()
    tp.splot.f.savefig(pjoin(co.paper_fig_path,'combined_cluster_data_mod.pdf'))

    # %%
    dfa = lfc.get_plot_df_6(ds)
    round_dic = lfc.round_dic()

    dfa = dfa.rename({SRR:SRR6},axis=1)

    tp = lfc.TablePlot(dfa, cwidth=7.25/7, rheight=.45,
                       title_size=8,round_dic=round_dic,
                       text_size=8)
    tp.plot_label()
    tp.plot_cols()
    tp.splot.axf[0].set_ylim(-.5, tp.nr + .5)
    df1 = lfc.fix_index6(dfa, tp)
    # lfc.fix_main_pw(df1, tp)
    lfc.add_blines6(tp)

    tp.despine()
    tp.splot.f.tight_layout()
    tp.splot.f.subplots_adjust(wspace=.1)
    tp.splot.f.show()
    tp.splot.f.savefig(pjoin(co.paper_fig_path,'combined_cluster_data_nc6_mod_11_2_cm_.pdf'))
    tp.splot.f.show()

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
# %%
