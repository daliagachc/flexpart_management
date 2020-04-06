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
    nc186 = pd.read_csv(pjoin(co.tmp_data_path, 'nc_18_nc_06.csv'))
    _df = nc186.rename({'18_NC': 'lab_name'}, axis=1).set_index('lab_name')
    nc = '06_NC'
    _da = _df.to_xarray()[nc]
    _ds = ds.assign_coords({nc: _da})

    # %%
    _ds1 = _ds.groupby(nc).sum()
    ct = 'conc_tot'
    # %%
    _da: xr.DataArray = _ds1[ct]
    _da = _da.transpose(co.RL, nc)
    # _da = _da.rolling(**{co.RL:24*30},min_periods=1,center=True).
    dat = _da.data
    import scipy.ndimage as si
    sig = 24 * 10
    dat1 = si.gaussian_filter(dat, (sig, 0), truncate=1 * sig, mode='nearest')
    gau = xr.zeros_like(_da) + dat1
    con_gau = 'con_gau'
    _ds1[con_gau] = gau
    labs = _ds1[nc].values
    len_labs = len(labs)
    # %%

    f, axs = plt.subplots(len_labs, 1, figsize=(7.25, .8 * len_labs), dpi=300,
                          sharey=False,
                          sharex=False
                          )
    axf = axs.flatten()
    abc = ['a','b','c','d','e','f']
    for ax, lab,a in zip(axf, labs,abc):
        _d = _ds1.loc[{nc: lab}].to_dataframe()
        ax: plt.Axes
        col = co.pw_col_dict[lab]
        _d[con_gau].plot(ax=ax, color=col, alpha=.4, linewidth=1.5)
        _d[ct].plot(ax=ax, linewidth=.5, color=col)
        # _d['conc_sfc'].plot(ax=ax)
        sns.despine(ax=ax)
        ax.set_ylim([-1, 100])
        ax.set_yticks([0, 50, 100])
        ax.set_yticklabels([0, 50, 100])
        # ax.axhline(50,color='w')
        ax.text(.99, 1.1, lab,
                horizontalalignment='right',
                verticalalignment='top',
                transform=ax.transAxes,
                color=co.pw_col_dict[lab],
                size=8
                # weight='bold'
                )

        ax.text(0.01, 1.05, a,
                horizontalalignment='left',
                verticalalignment='top',
                transform=ax.transAxes,
                # color=co.pw_col_dict[lab],
                weight='bold',
                )
        ax.set_xlabel(None)
    des_ops = dict(trim=True,offset={'bottom':5,'left':5})
    for ax in axs[:-1]:
        sns.despine(ax=ax,bottom=True,**des_ops)
        ax.set_xticks([])
        ax.set_xticks([],minor=True)
        # ax.xaxis.set_ticks_position('none')
        # ax.set_yticklabels(['', 50, 100])
        pass


    sns.despine(ax=axs[-1], **des_ops)

    f: plt.Figure
    full_ax:plt.Axes = f.add_subplot(1,1,1)
    full_ax.patch.set_alpha(0)
    sns.despine(ax=full_ax,left=True,bottom=True)
    full_ax.set_yticks([0])
    full_ax.set_yticklabels(['       '])
    full_ax.tick_params(colors=[0,0,0,0])
    full_ax.set_xticks([])
    full_ax.set_ylabel('SRR [%]')

    plt.tight_layout()
    f.subplots_adjust(left=.1,right=.98,top=.97,bottom=.1,hspace=.3)
    f.show()
    f.savefig(pjoin(co.paper_fig_path,'pw_timeseries_7_25.pdf'))

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
