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
import cartopy
import numpy
from flexpart_management.modules import constants as co, flx_array as fa
from matplotlib import pyplot
from useful_scit.imps import *

# %%
def get_per_above5sl(da_srl):
    da_srl_tot = da_srl.sum()
    da_5000 = da_srl.where(da_srl[co.ZM] >= 5000).sum()
    da_a5sl = da_5000 / da_srl_tot * 100
    da_a5sl.load()
    return da_a5sl


def get_per_above_sfc(da_srl,level=1500):
    topo = da_srl[co.TOPO]
    hagl = da_srl[co.ZM] - topo
    _boo_hagl = np.logical_and(hagl >= 0, hagl <= level)
    da_tot = da_srl.sum()
    da_srf = da_srl.where(_boo_hagl).sum()
    per_ft = (da_tot - da_srf) / da_tot * 100
    per_ft.load()
    return per_ft


def plot_bol_cax(axbol, caxbol, da_srl, fig, name, r, t0, t1, tlen):
    patch = plot_bolivia(axbol, da_srl, name, r, t0, t1, tlen)
    fig.colorbar(patch, caxbol)


def plot_bolivia(ax, da_srl, name, r, t0, t1, tlen):
    da_th_r = da_srl.sum([co.ZM, co.RL])
    ax: plt.Axes = fa.get_ax_bolivia(ax=ax)
    patch = fa.logpolar_plot(da_th_r.to_dataset(), ax=ax, name=co.CONC,
                             return_patch=True, colorbar=False)
    ax.set_title(
        f'{name}:{r[name]}  |  {r[t0]}  -  {r[t1]}  |  {tlen}:{int(r[tlen])}')
    return patch


def plot_double_x_z(ax1, ax2, ax3, da_srl, h11, h12, h21, h22, r):
    h1 = h11
    h2 = h12
    mesh1 = plot_r_z(ax1, da_srl, h1, h2, r)
    h1 = h21
    h2 = h22
    mesh2 = plot_r_z(ax2, da_srl, h1, h2, r)
    vmax = np.max([mesh1.get_clim()[1], mesh2.get_clim()[1]])
    mesh1.set_clim(0, vmax)
    mesh2.set_clim(0, vmax)
    plt.colorbar(mesh1, cax=ax3)
    per_ft = get_per_above_sfc(da_srl)
    per_5sl = get_per_above5sl(da_srl)
    st = f'% > 1.5 km agl: {int(per_ft)}\n' \
         f'% > 5.0 km asl: {int(per_5sl)}'
    ax2.annotate(st, (0,-.2),
                 xycoords='axes fraction',
                 verticalalignment='top')




def plot_r_z(ax, da_srl, h1, h2, r):
    cmap = plt.get_cmap('Reds')
    th1 = r[h1] * np.pi / 6
    th2 = r[h2] * np.pi / 6
    if th1 <= th2:
        _fun = np.logical_and
    else:
        _fun = np.logical_or
    th_c = da_srl[co.TH_CENTER]
    _bool = _fun(th_c >= th1, th_c <= th2)
    da_srl_sth = da_srl[{co.TH_CENTER: _bool}]
    da_z_r_th = da_srl_sth.sum(co.RL)
    da_z_r_th = da_z_r_th.assign_coords(km=da_z_r_th[co.R_CENTER] * 100)
    da_z_r = da_z_r_th.sum(co.TH_CENTER)
    mesh = da_z_r.plot(x='km', y=co.ZM, add_colorbar=False, cmap=cmap, ax=ax)
    da_topo = da_z_r_th * da_z_r_th[co.TOPO]
    da_topo = da_topo.sum([co.ZM, co.TH_CENTER]) / da_z_r_th.sum(
        [co.ZM, co.TH_CENTER])
    da_topo.plot(color='k', ax=ax, x='km')

    ax.annotate(f'clock: {r[h1]} - {r[h2]}', [.01, .99],
                verticalalignment='top', xycoords='axes fraction')
    ax.set_ylabel('height [m a.s.l.]')
    ax.set_xlabel('distance from CHC [km]')
    ax.set_ylim(0, 15000)
    return mesh


def plot_plot(da, h11, h12, h21, h22, name, r, t0, t1, tlen):
    rt0 = xr.DataArray(r[t0])
    rt1 = xr.DataArray(r[t1])
    # %%
    da_srl = da.loc[{co.RL:slice(rt0,rt1)}]
    w_inch = 1.6
    h_inch = 1
    cols = 5
    rows = 12
    fig: plt.Figure = plt.figure(
        figsize=(w_inch * cols, h_inch * rows),
        dpi=150
                                 )
    g = fig.add_gridspec(5, 12)
    axbol = fig.add_subplot(g[:3, :-1], projection=crt.crs.PlateCarree())
    caxbol = fig.add_subplot(g[:3, -1])
    ax1 = fig.add_subplot(g[3, :-1])
    ax2 = fig.add_subplot(g[4, :-1])
    ax3 = fig.add_subplot(g[3:5, -1])
    # fig.show()
    # %%
    plot_double_x_z(ax1, ax2, ax3, da_srl, h11, h12, h21, h22, r)
    # fig.show()
    # %%
    # fig.show()
    # %%
    plot_bol_cax(axbol, caxbol, da_srl, fig, name, r, t0, t1, tlen)
    plt.show()
    return fig