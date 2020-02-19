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
from flexpart_management.notebooks.paper_time_series.paper_time_series_lfc \
    import *

import flexpart_management.notebooks.paper_time_series.paper_time_series_lfc \
as lfc



# %%
def main():
    # %%
    ds = xr.open_dataset(pjoin(co.tmp_data_path, 'srr_sfc_tot_clus.nc'))
    # %%
    ds['range'] = ds['lab_name'].str[-2:]
    ds = ds.set_coords('range')
    ds
    # %%
    pos_sr = [[.06, .73], [.01, .77], [.13, .65], [.1, .75], [.01, .8], [.04, .4],]
    pos_sm = [[.06, .83], [.005, .77], [.01, .65], [.04, .3],]
    pos_mr = [[.23, .8], [.06, .8], [.15, .53], [.15, .5], [.01, .7],]
    pos_lr = [[.04, .45], [.12, .5], [.03, .65],]
    y_ticks_sr = [0, 10, 20]
    y_ticks_sm = [0, 25, 50]
    y_ticks_mr = [0, 45, 90]
    y_ticks_lr = [0, 30, 60]

    lSR,lSM, lMR, lLR =(
        'short range (SR)','short-medium range (SM)',
        'medium range (MR)','long range (LR)')

    ops = dict(
        SR = dict(pos=pos_sr,y_ticks=y_ticks_sr,ln =lSR,col=ucp.cc[0]),
        SM = dict(pos=pos_sm,y_ticks=y_ticks_sm,ln =lSM,col=ucp.cc[1]),
        MR = dict(pos=pos_mr,y_ticks=y_ticks_mr,ln =lMR,col=ucp.cc[2]),
        LR = dict(pos=pos_lr,y_ticks=y_ticks_lr,ln =lLR,col=ucp.cc[3]),
    )
    # %%
    ranges = ['SR','SM']
    f = lfc.plot_combined_ts(ds, ops, ranges)
    f.savefig(pjoin(co.paper_fig_path,'ts_clus_sr_sm_7_25.pdf'))
    f.show()

    ranges = ['MR','LR']
    f = lfc.plot_combined_ts(ds, ops, ranges)
    f.savefig(pjoin(co.paper_fig_path,'ts_clus_mr_lr_7_25.pdf'))
    f.show()


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
