# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
import numpy
import pandas
from flexpart_management.notebooks.sulfate_volcano_chc.n02_regressors.n02_regressors_lfc import *
from matplotlib import pyplot


def get_source_fit(
        clus_cols,
        var_name,
        ts_merged_in,
        fit_par=None,
        log=False,
        log_thr_min=.01,
        log_thr_max=10,
        orig_interval='1H',
        plot = True
):
    default_dic = dict(
        # l1_ratio=[1], n_alphas=100
    )

    if fit_par is not None:
        fit_par = {**default_dic, **fit_par}
    else:
        fit_par = default_dic

    # sulf_log = 'lg(SO4)'
    ts_merged = ts_merged_in.resample(orig_interval).median()
    # ts_merged[sulf_log] = np.log(ts_merged[var_name])
    ts_var = ts_merged[var_name]


    ts_var_pos = ts_merged[ts_merged[var_name] >= 0]

    _y = ts_var_pos[var_name]
    '''results vector'''

    _X = get_clus_norm(clus_cols, ts_var_pos)
    '''input cluster matrix normalized to the mean'''

    import sklearn.linear_model as lm
    reg = lm.ElasticNet(
        positive=True,
        **fit_par

    )
    '''regression object'''

    reg.fit(_X, _y)

    coef_ds = pd.Series(reg.coef_, index=clus_cols)
    '''coeficient results from the regression'''



    __y = pd.Series(reg.predict(_X), index=_X.index)
    _y_mod = __y.resample(orig_interval).mean()
    '''prediction from the model'''

    residuals: pd.Series = _y - _y_mod
    '''residuals from model vs meas'''


    if plot:
        plot_diag_hist(log_thr_max, log_thr_min, ts_var)
        plot_diag_ts(log_thr_max, log_thr_min, ts_var)
        plot_coefs(coef_ds)

        plot_res_dists(_y, residuals)

        plot_model_vs_meas(
            _y_mod.resample(orig_interval).mean(),
            _y.resample(orig_interval).mean()
        )

    return reg, _X, _y


def plot_res_dists(_y, residuals):
    f, ax = plt.subplots()
    ax: plt.Axes
    sns.distplot(
        residuals.dropna(),
        ax=ax,
        norm_hist=True,
        label='residuals',
    )
    sns.distplot(
        _y.dropna(),
        ax=ax,
        norm_hist=True,
        label='measurements'
    )
    ax.legend()
    plt.show()


def plot_model_vs_meas(_x, _y):
    f, ax = plt.subplots()
    ax: plt.Axes
    _x.plot(ax=ax, label='mod')
    _y.plot(ax=ax, label='input')
    ax.legend()
    plt.show()


def plot_coefs(coef_ds):
    if None is None:
        f, ax = plt.subplots()
        ax: plt.Axes

    coef_ds.plot.bar(ax=ax, zorder=1)
    ax.grid(axis="y", color='w', linewidth=1)
    ax.set_title('coeficients')
    plt.show()


def plot_diag_ts(log_thr_max, log_thr_min, var_ser, ax=None):
    if ax is None:
        f, ax = plt.subplots(figsize=(10, 4))
        ax: plt.Axes
    var_ser.plot(label='original', ax=ax,
                 color=[ucp.cc[0]]
                 )

    # plt.show()

    axt = ax.twinx()
    var_ser.plot(ax=axt, label='original log',
                 color=[ucp.cc[1]]
                 )
    axt.set_yscale('log')
    axt.set_ylim(log_thr_min, log_thr_max)
    axt.legend(loc=1)
    ax.legend(loc=2)
    plt.show()


def plot_diag_hist(log_thr_max, log_thr_min, var_ser):
    f, ax = plt.subplots()
    ax: plt.Axes
    bins = np.geomspace(log_thr_min, log_thr_max, 15)
    # sulf_ = sulf_
    var_ser_norm = var_ser
    sns.distplot(
        a=var_ser,
        bins=bins,
        ax=ax,
        hist=True,
        kde=False,
        norm_hist=False,
        color=ucp.cc[0]

    )
    ax.tick_params(labelcolor=ucp.cc[0], axis='y')
    ax.set_ylabel('histogram')

    axt = ax.twinx()
    var_ser_nc = var_ser
    sns.distplot(
        a=var_ser,
        hist_kws=dict(cumulative=True),
        hist=True,
        kde=False,
        norm_hist=True,
        ax=axt,
        bins=bins,
        color=ucp.cc[1]
    )
    axt.tick_params(labelcolor=ucp.cc[1], axis='y')
    axt.set_ylabel('cum sum')
    ax.set_xscale('log')
    # plt.hist()
    plt.show()
