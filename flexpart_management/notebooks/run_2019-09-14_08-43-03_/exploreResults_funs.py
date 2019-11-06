# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
from cartopy import crs
from useful_scit.imps import (pd,np,xr,za,mpl,plt,sns, pjoin, os,glob,
                              dt,sys,ucp,log, splot, crt)

from flexpart_management.modules import constants as co, flx_array as fa


def plot_multiple_foot_prints(nds_in, pad_chc=.2, height_lims=(4e3, 8.5e3)):
    _da = nds_in[co.CONC].squeeze()
    # %%
    # %%
    _da1 = _da.sum([co.TIME, co.VLONG]).loc[{co.ZM: slice(0, 4e3)}]
    f, ax = splot()
    _da1.plot.pcolormesh(ax=ax, cmap=plt.get_cmap('Reds'));
    ax.grid(True, color='k', linestyle='--')
    ax.set_title('');
    ax.set_axisbelow(False)
    ax.set_xlim((co.CHC_LAT - pad_chc, co.CHC_LAT + pad_chc))

    # %%
    _da1 = _da.sum([co.TIME, co.ZM])
    f, ax = splot(subplot_kw={'projection': crs.PlateCarree()})
    _da1.plot.pcolormesh(ax=ax, cmap=plt.get_cmap('Reds'), levels=10);
    ax.set_title('');
    ax.set_xlim((co.CHC_LON - pad_chc, co.CHC_LON + pad_chc))
    ax.set_ylim((co.CHC_LAT - pad_chc, co.CHC_LAT + pad_chc))
    # ax.set_yticks([co.CHC_LAT], crs=crs.PlateCarree())
    gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                      linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    fa.add_chc_lpb(ax)
    ucp.scale_bar(ax, (.1, .1), 10)

#     return

    # %%
    # _da1 = _da.sum([co.TIME,co.ZM])
    _da1 = _da[co.TOPO]
    f, ax = splot(subplot_kw={'projection': crs.PlateCarree()})
    _da1.plot.pcolormesh(ax=ax, cmap=plt.get_cmap('Reds'), robust=True,
                         vmin=4e3, vmax=5250, levels=7);
    ax.set_title('');
    ax.set_xlim((co.CHC_LON - pad_chc, co.CHC_LON + pad_chc))
    ax.set_ylim((co.CHC_LAT - pad_chc, co.CHC_LAT + pad_chc))
    # ax.set_yticks([co.CHC_LAT], crs=crs.PlateCarree())
    gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                      linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    fa.add_chc_lpb(ax)
    ucp.scale_bar(ax, (.1, .1), 10)

#     return
    log.ger.debug('starting last plot')
    # %%
    f,ax = splot()
    _da.sum(fa.get_dims_complement(_da, co.TIME)).plot(ax=ax)
    # %%
#     i7 = (5000 - _da[co.TOPO])
#     f,ax = splot()
#     i7.plot.hist(ax=ax);
#     i7.name = 'i7'
    # %%
    ZSL = 'ZSL'
    # %%
    zr = np.arange(0, 1e4, 1e2)
    zr = xr.DataArray(zr, coords=[(ZSL, zr)])
    # %%
    zr[ZSL] = zr[ZSL].assign_attrs(units='masl')
    # %%
    _zr = (zr - _da[co.TOPO])
    # %%
    _int = _da.interp(
        **{co.ZM: _zr, co.VLAT: _zr[co.VLAT], co.VLONG: _zr[co.VLONG]})
    # %%
    _int.sum().load().item()
    # %%
    _da.sum().load().item()
    # %%
    _int2 = _int.where(_zr > 0)
    # %%
    _is = _int2.sum([co.VLONG, co.TIME])
    _is = _is.where(_is > 0)
    f,ax = splot(figsize=(15, 1.5))
    res = _is.plot(cmap=plt.get_cmap('Reds'),ax=ax)
#     ax = plt.gca()
    ax.set_xlim((co.CHC_LAT - pad_chc, co.CHC_LAT + pad_chc))
    ax.set_ylim(height_lims)
    ax.tick_params(axis='x', rotation=90)
    ax.grid(color='k', alpha=.5)
    ax.set_axisbelow(False)