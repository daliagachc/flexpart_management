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
from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

plt;


# %%
def plot_range(
        axf, ds, ops, range_plot,
):
    _boo = ds['range'] == range_plot
    dsc = ds['conc_tot']
    dst = dsc.where(_boo).dropna('lab_name')
    df = dst.to_dataframe()['conc_tot'].unstack()
    df.index = pd.to_datetime(df.index)
    df.index.name = None
    ops_r = ops[range_plot]
    pos = ops_r['pos']
    y_ticks = ops_r['y_ticks']
    lab_list = np.array_split(df.columns, 2)
    cp = sns.color_palette('tab10', 10)
    jj = 0
    for i in range(2):
        for ii, c in enumerate(lab_list[i]):
            ax = axf[i]
            df[c].plot(
                ax=ax, linewidth=.4,
                c=cp[jj],
                # linestyle=sty[ii],
                label=c,
            )
            ax.set_yticks(y_ticks)
            ax.annotate(
                c, xy=pos[jj], c=cp[jj], xycoords='axes fraction',
                fontsize=6
            )
            ax.set_ylim(-.1 * y_ticks[-1], y_ticks[-1])
            # ax.legend()
            jj += 1
    ax = axf[0]
    ax.annotate(
        ops_r['ln'],
        xy=[1, 1],
        verticalalignment = 'bottom',
        horizontalalignment = 'right',
        xycoords = 'axes fraction',
        # c = ops_r['col']

    )

def plot_combined_ts(ds, ops, ranges):
    rows = 4
    h = 1
    f_h_raw = rows * h
    f_w = 7.25
    bot_in = .4
    f_h = f_h_raw + bot_in
    bot_pe = bot_in / f_h
    # noinspection PyTypeChecker
    f, axs = plt.subplots(rows, 1, figsize=(f_w, f_h), dpi=400, sharex=True,
                          sharey=False)
    axf = axs.flatten()
    ax: plt.Axes
    f: plt.Figure
    ax_i = [[0, 1], [2, 3]]
    for ai, r in zip(ax_i, ranges):
        plot_range(axf[ai], ds, ops, r)
    sns.despine(f, trim=True)
    for ax in axf[:-1]:
        sns.despine(ax=ax, bottom=True)
        ax.xaxis.set_ticks_position('none')
        pass
    full_ax:plt.Axes = f.add_subplot(1,1,1)
    full_ax.patch.set_alpha(0)
    sns.despine(ax=full_ax,left=True,bottom=True)
    full_ax.set_yticks([0])
    full_ax.set_yticklabels(['    '])
    full_ax.tick_params(colors=[0,0,0,0])
    full_ax.set_xticks([])
    full_ax.set_ylabel('SRR [%]')

    f.tight_layout()
    f.subplots_adjust(hspace=.2, top=.95, bottom=bot_pe,
                      left=.07)
    fa.add_fig_panels(axl=axf, par='')
    return f

