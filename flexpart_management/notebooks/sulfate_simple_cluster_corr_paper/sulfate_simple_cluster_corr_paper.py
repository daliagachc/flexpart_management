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
import flexpart_management.notebooks.sulfate_simple_cluster_corr_paper. \
    sulfate_simple_cluster_corr_paper_lfc as lfc
from flexpart_management.notebooks.sulfate_simple_cluster_corr_paper. \
    sulfate_simple_cluster_corr_paper_lfc import *


# %%
def main():
    # %%
    sul = 'Sulfate'
    lab_name = 'lab_name'
    # %%
    acsm = lfc.get_acsm_data()
    # %%
    lfc.plot_distributions(acsm, sul)

    # %%
    ds = fa.open_temp_ds('ds_clustered_18_agl.nc')
    # ds['lab_name'] = ds['lab_name'][{co.RL: 0}]
    ds
    # %%
    _dic, cols, dj18 = lfc.get_corrs(acsm, ds, lab_name, sul)
    _dic6, cols6, dj6 = lfc.get_corrs(acsm, ds, 'lab_nc06', sul)

    lfc.plot_corrs(_dic, cols, sul)
    lfc.plot_corrs(_dic6, cols6, sul)

    # %%
    # s = splot(2,1,dpi=300,figsize=(7.25,4))
    lfc.plot_fig_comparison(_dic, cols, dj18, sul)

    # %%
    df18, df6, ticks, white_lines = lfc.get_dfs(_dic, _dic6, sul)

    # %%

    ds['lab_nc06'] = ds['lab_nc06'][{co.RL: [0]}].sum(co.RL)
    ds['lab_name'] = ds['lab_name'][{co.RL: [0]}].sum(co.RL)
    # %%

    dcc, dsn = lfc.get_dcc(ds)
    # %%
    d9 = dsn.where(dsn['lab_name'] == '09_MR').sum([co.RL, co.ZM])
    d9c = d9['CONC'].load()
    d10 = dsn.where(dsn['lab_name'] == '10_SR').sum([co.RL, co.ZM])
    d10c = d10['CONC'].load()

    d8M = dsn.where(dsn['lab_name'] == '08_SM').sum([co.RL, co.ZM])
    d8mc = d8M['CONC'].load()

    d7 = dsn.where(dsn['lab_name'] == '07_SR').sum([co.RL, co.ZM])
    d7c = d7['CONC'].load()

    d8 = dsn.where(dsn['lab_nc06'] == '08_PW').sum([co.RL, co.ZM])
    d8c = d8['CONC'].load()
    # %%
    f, gs, axa,axc, axd = lfc.plot_fig_corr_s04(_dic, cols, dcc, df18,
                                            df6, dj18, dj6, sul,
                                            ticks,
                                            white_lines, dsn)

    axb = lfc.plot_map2(d10c, d7c, d8c, d8mc, d9c, f, gs)

    axa.annotate(f'a', [-0.2, 1.05], xycoords='axes fraction',weight='bold')
    axb.annotate(f'b', [-0.05, 1.05], xycoords='axes fraction',weight='bold')
    axc.annotate(f'c', [0.0, 1.05], xycoords='axes fraction',weight='bold')
    axd.annotate(f'd', [0.0, 1.05], xycoords='axes fraction',weight='bold')

    f.subplots_adjust(hspace=.5)

    f.show()

    f.savefig(pjoin(co.paper_fig_path, 'pearson_corr_so4.pdf'))

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
# %%
# %%
# %%
# %%
# %%
