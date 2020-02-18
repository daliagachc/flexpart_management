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
import numpy
from matplotlib import pyplot
from useful_scit.imps import *
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa


co, fa, plt;


# %%


def log_his_series(ser, ax=None, fmin=None,
                   plot=True,
                   **kwargs):
    qM = ser.quantile(.99)
    qm = ser.quantile(.01)
    smin = ser.min()
    smax = ser.max()
    qmm = qM * np.power(10, -3.2)
    if qm <= 0:
        qm = qmm
    if fmin is not None:
        qm = fmin

    bins = np.geomspace(qm, qM, 40)
    bins = [smin, *bins[1:-1], smax]
    if ax is None:
        f, ax = plt.subplots()
    ax: plt.Axes
    ser.plot.hist(bins=bins, alpha=.5, ax=ax, **kwargs)
    ax.set_xscale('log')
    ax.set_xlim(qm, qM)
    ax.set_title(ser.name)
    if plot:
        ax.figure.show()


def plot_mult_hist(ax, c_, ts, xmax=1e6):
    log_his_series(ts[c_], ax=ax, label='all', plot=False)
    jan_bool = ts['time_utc'].dt.month == 1
    log_his_series(ts[jan_bool][c_], ax=ax, color='red',
                   fmin=3000, label='jan', plot=False)
    day_bool = \
        (ts['time_utc'].dt.hour > 12) \
        & (ts['time_utc'].dt.hour < 11)
    log_his_series(ts[~day_bool][c_], ax=ax, color='black',
                   fmin=3000, label='night', plot=False)
    log_his_series(ts[(~day_bool) & (jan_bool)][c_], ax=ax, color='green',
                   fmin=3000, label='night_jan', plot=False)
    if ax is not None:
        ax.set_xlim(2000, xmax)
        ax.legend()
        ax.figure.show()


# %%
def plot_row(cc, ts, bmin=1e5, bmax=1e7):
    f, axs = plt.subplots(4, 1, sharey=False, sharex=True)
    lab = 'all', 'night', 'jan', 'jan night'
    bins = np.geomspace(bmin, bmax, 25)
    bins = [0, *bins[1:-1], 1e10]
    colors = [ucp.cc[i] for i in range(4)]
    axf = axs.flat
    axf[0].set_title(cc)
    for l, ax, c in zip(lab, axf, colors):
        ts[ts[l]][cc].plot.hist(
            ax=ax, bins=bins, colors=[c], label=l
        )
        ax.set_xscale('log')
        ax.set_xlim(bmin, bmax)
        ax.legend()
    plt.show()


def interactive_plot(c4, c46, c6, c9, ts):
    from bokeh.layouts import gridplot
    from bokeh.plotting import figure, show, output_file
    from bokeh.models import Range1d, LinearAxis, LogAxis
    x = np.linspace(0, 4 * np.pi, 100)
    y = np.sin(x)
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
    p1 = figure(title="Legend Example", tools=TOOLS,
                plot_width=1200, plot_height=400,
                y_axis_type="log", x_axis_type='datetime'
                )
    p2 = figure(title="Legend Example", tools=TOOLS,
                plot_width=1200, plot_height=400,
                y_axis_type="linear", x_axis_type='datetime',
                x_range=p1.x_range
                )
    # Setting the second y axis range name and range
    p1.extra_y_ranges = {"foo": Range1d(*ts[c9].quantile([.01, .99]))}
    # Adding the second axis to the plot.
    p1.add_layout(LogAxis(y_range_name="foo"), 'right')
    p1.line('time_utc', c4, legend_label=c4, source=ts, color='black')
    p1.line('time_utc', c6, legend_label=c6, source=ts, color='blue')
    p1.line('time_utc', c9, legend_label=c9, source=ts, color='red',
            y_range_name="foo"
            )
    p2.line('time_utc', c46, legend_label=c4, source=ts, color='black'

            )
    # p1.circle(x, 2 * y, legend_label="2*sin(x)", color="orange")
    # p1.circle(x, 3 * y, legend_label="3*sin(x)", color="green")
    #
    # p1.legend.title = 'Example Title'
    #
    # p2 = figure(title="Another Legend Example", tools=TOOLS)
    #
    # p2.circle(x, y, legend_label="sin(x)")
    # p2.line(x, y, legend_label="sin(x)")
    #
    # p2.line(x, 2 * y, legend_label="2*sin(x)", line_dash=(4, 4),
    #         line_color="orange", line_width=2)
    #
    # p2.square(x, 3 * y, legend_label="3*sin(x)", fill_color=None,
    #           line_color="green")
    # p2.line(x, 3 * y, legend_label="3*sin(x)", line_color="green")
    output_file("legend.html", title="legend.py example")
    show(gridplot([p1, p2], ncols=1, ))
    # plot_width=400,
    # plot_height=400))  # open a browser
    # show(p1)


def interactive_plot_bok(*, df, col, time_col, fig_kw=None):
    if fig_kw is None:
        fig_kw = {}
    from bokeh.layouts import gridplot
    from bokeh.plotting import figure, show, output_file
    from bokeh.models import Range1d, LinearAxis, LogAxis
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
    fops = {**dict(tools=TOOLS,
                plot_width=1200, plot_height=400,
                y_axis_type="log", x_axis_type='datetime'),
            **fig_kw
            }
    p1 = figure(title="Legend Example", **fops)
    # Setting the second y axis range name and range
    # Adding the second axis to the plot.
    p1.line('time_utc', col, legend_label=col, source=df, color='black')
    # p2.square(x, 3 * y, legend_label="3*sin(x)", fill_color=None,
    #           line_color="green")
    # p2.line(x, 3 * y, legend_label="3*sin(x)", line_color="green")
    output_file("legend.html", title="legend.py example")
    # show(gridplot([p1, p2], ncols=1, ))
    # plot_width=400,
    # plot_height=400))  # open a browser
    show(p1)
# %%

def plot_corr_wrf_mea(wrf_col, mea_col, wrf_ds, ts, mult=1000):
    wrf_qv = wrf_ds[wrf_col].reset_coords(drop=True).to_dataframe()
    wrfR = wrf_qv.resample('30T').mean()
    tsR = ts.set_index('time_utc')[mea_col].resample('30T').mean()
    mwrfts = pd.merge(wrfR, tsR, left_index=True, right_index=True)
    mwrfts[wrf_col] = mwrfts[wrf_col] * mult
    _boo = mwrfts.isnull().any(1)
    mwrfts = mwrfts[~_boo]
    # %%
    # %%
    mwrfts.plot.scatter(x=wrf_col, y=mea_col, marker='.', alpha=.1)
    plt.show()
    # %%
    f, ax = plt.subplots()
    sns.kdeplot(data=mwrfts[wrf_col], data2=mwrfts[mea_col],
                cmap='Reds', cbar=True, shade=True, ax=ax
                )
    mwrfts.plot.scatter(x=wrf_col, y=mea_col, marker=',', color='k',
                        alpha=.1, ax=ax
                        )
    f, ax = plt.subplots()
    sns.kdeplot(data=mwrfts[wrf_col], data2=mwrfts[mea_col],
                cmap='Reds', cbar=True, shade=True, ax=ax
                )
    plt.show()
    return mwrfts
