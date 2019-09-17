```python
from useful_scit.imps import *
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co
mpl.rcParams['figure.dpi'] = 150
```

    reload



```python
# log.ger.setLevel(log.log.DEBUG)
log.ger.setLevel(log.log.INFO)
```


```python
def swap_xy2lon_lat(nds):
    _boo1 = (nds[co.XLONG].max(co.SOUTH_NORTH) - nds[co.XLONG].min(
        co.SOUTH_NORTH)).sum().item() == 0
    # %% {"jupyter": {"outputs_hidden": true}}
    _boo2 = (nds[co.XLAT].max(co.WEST_EAST) - nds[co.XLAT].min(
        co.WEST_EAST)).sum().item() == 0
    
    log.ger.debug('_boo1 is %s',_boo1)

    if _boo1 and _boo2:
        log.ger.debug('inside loop')
        xx = [co.XLAT, co.XLONG]
        ww = [co.WEST_EAST, co.SOUTH_NORTH]
        vv = [co.VLAT, co.VLONG]
        rr = [co.VLONG, co.VLAT]
        # %% {"jupyter": {"outputs_hidden": true}}
        for i in range(2):
            ff = nds[xx[i]].mean(ww[i])
            ff.name = vv[i]
            nds = nds.assign_coords(**{vv[i]: ff})
        for i in range(2):
            nds = nds.swap_dims({ww[i]: rr[i]})
    return nds


def get_combined_flx_ds(DD, dir_path,chop_list=-1):
    _ds_list = fa.get_flx_ds_list(DD, dir_path)
    _ds_list = _ds_list[:chop_list]
    # %% {"jupyter": {"outputs_hidden": true}}
    ds_list = fa.trim_flx_ds_list(_ds_list)
    # %% {"jupyter": {"outputs_hidden": true}}
    dsm = xr.open_mfdataset(ds_list, concat_dim=co.TIME, combine='nested')
    dsm = fa.convert_ds_time_format(dsm)
    dsm = fa.remove_ageclass(dsm)
    # %% {"jupyter": {"outputs_hidden": true}}
    hds = fa.import_head_ds(dir_path, DD)
    hds = hds.drop_dims([co.SPECIES, co.RECEPTORS, co.TIME, co.AGECLASS])
    # %% {"jupyter": {"outputs_hidden": true}}
    nds = xr.merge([hds, dsm])
    nds.attrs = hds.attrs.copy()
    nds = fa.add_zmid(nds)
    for v in (set(co.HEAD_VARS) & set(hds.variables)):
        nds = nds.assign_coords(**{v: nds[v]})
    _cr = co.RELEASENAME
    _df = nds[_cr].to_pandas().str.decode("utf-8")
    _df = pd.to_datetime(_df, format='chc%Y%m%d_%H')
    nds = nds.assign_coords(**{co.RELEASE_TIME: _df.to_xarray()})
    nds = nds.swap_dims({co.BT:co.ZM})


    return nds


def __main__():
    pass
```


```python
dir_path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/runs/run_2019-06-10_11-10-03_/2017-12-31'
```


```python
# concat_ds = fa.concat_file_ds_list(ds_list)
```


```python
DD = co.D2
nds = get_combined_flx_ds(DD, dir_path)
nds = swap_xy2lon_lat(nds)
# nds = nds[{co.RL:-1}]
```


```python
_da = nds[co.CONC][{co.RL:23}]
```


```python
_da1 = _da.sum([co.VLAT],keep_attrs=True).load()
```


```python
# _da2 = _da1.loc[{co.VLONG:slice(-68.5,-67),co.ZM:slice(0,1e4)}]
_da2 = _da1
```


```python
args = dict(
    x=co.DIS,
    y=co.ZM,
    norm=mpl.colors.LogNorm(),
    vmin=10,vmax=50000
)
```


```python
# fig,ax=plt.subplots(figsize=(10,5))
__da2 = _da2.copy()
__da2[co.DIS] = __da2[co.VLONG]*100
__da2[co.DIS] = __da2[co.DIS].assign_attrs(units='km')
__da2[co.DIS]=(__da2[co.DIS]/100-co.CHC_LON)*100
__da2[co.DIS]=__da2[co.DIS].assign_attrs(units='km')

__da2.plot(**{
    **args,
    'add_colorbar':True,
    'cmap': plt.get_cmap('Reds'),
    'norm':mpl.colors.Normalize(),
    'vmax':80,
    'col':co.TIME,
    'col_wrap':4,
    'ylim':(0,2e3),
    'xlim':(-5,5)
}

)
# ax.grid(True)
# ax.set_axisbelow(False)
# ax.xaxis.set_tick_params(rotation=90)
# ax.set_ylim(0,.2e4)
xl = 5
# ax.set_xlim(-xl,xl);
```


![png](check_heght_files/check_heght_10_0.png)



```python
_dss = _da2.sum(co.VLONG, keep_attrs = True)
_fg = _dss.plot(col=co.TIME,y=co.ZM,col_wrap=4,ylim=(0,4e3))

_v = _da2.sum([co.VLONG,co.TIME],keep_attrs = True)

q50=fa.weighted_quantile(.5,_v[co.ZM],sample_weight=_v.values)

_lt = len(_dss[co.TIME])
for i,ax in enumerate(_fg.axes.flatten()[:_lt]):
    _di = _dss.isel(**{co.TIME:i})
    _q50=fa.weighted_quantile(.5,_di[co.ZM],_di.values)
    _tot = _di.sum().item()
    ax.axhline(q50,color='k',linestyle='--',alpha=.5,label=f'global median = {np.round(q50)}')
    ax.axhline(_q50,color='r',linestyle='--',alpha=.5,label=f'global = {np.round(_q50)}')
    ax.axhline(_q50,color='r',linestyle='-',alpha=.5,label=f'tot = {np.round(_tot)}')
    ax.legend()



```

    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/modules/flx_array.py:840: RuntimeWarning: invalid value encountered in true_divide


    Error in callback <function flush_figures at 0x7fe87d99b840> (for post_execute):



    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/ipykernel/pylab/backend_inline.py in flush_figures()
        115         # ignore the tracking, just draw and close all figures
        116         try:
    --> 117             return show(True)
        118         except Exception as e:
        119             # safely show traceback if in IPython, else raise


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/ipykernel/pylab/backend_inline.py in show(close, block)
         37             display(
         38                 figure_manager.canvas.figure,
    ---> 39                 metadata=_fetch_figure_metadata(figure_manager.canvas.figure)
         40             )
         41     finally:


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/IPython/core/display.py in display(include, exclude, metadata, transient, display_id, *objs, **kwargs)
        304             publish_display_data(data=obj, metadata=metadata, **kwargs)
        305         else:
    --> 306             format_dict, md_dict = format(obj, include=include, exclude=exclude)
        307             if not format_dict:
        308                 # nothing to display (e.g. _ipython_display_ took over)


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/IPython/core/formatters.py in format(self, obj, include, exclude)
        178             md = None
        179             try:
    --> 180                 data = formatter(obj)
        181             except:
        182                 # FIXME: log the exception


    </homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/decorator.py:decorator-gen-9> in __call__(self, obj)


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/IPython/core/formatters.py in catch_format_error(method, self, *args, **kwargs)
        222     """show traceback on failed format call"""
        223     try:
    --> 224         r = method(self, *args, **kwargs)
        225     except NotImplementedError:
        226         # don't warn on NotImplementedErrors


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/IPython/core/formatters.py in __call__(self, obj)
        339                 pass
        340             else:
    --> 341                 return printer(obj)
        342             # Finally look for special method names
        343             method = get_real_method(obj, self.print_method)


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/IPython/core/pylabtools.py in <lambda>(fig)
        242 
        243     if 'png' in formats:
    --> 244         png_formatter.for_type(Figure, lambda fig: print_figure(fig, 'png', **kwargs))
        245     if 'retina' in formats or 'png2x' in formats:
        246         png_formatter.for_type(Figure, lambda fig: retina_figure(fig, **kwargs))


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/IPython/core/pylabtools.py in print_figure(fig, fmt, bbox_inches, **kwargs)
        126 
        127     bytes_io = BytesIO()
    --> 128     fig.canvas.print_figure(bytes_io, **kw)
        129     data = bytes_io.getvalue()
        130     if fmt == 'svg':


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/matplotlib/backend_bases.py in print_figure(self, filename, dpi, facecolor, edgecolor, orientation, format, bbox_inches, **kwargs)
       2058                     bbox_artists = kwargs.pop("bbox_extra_artists", None)
       2059                     bbox_inches = self.figure.get_tightbbox(renderer,
    -> 2060                             bbox_extra_artists=bbox_artists)
       2061                     pad = kwargs.pop("pad_inches", None)
       2062                     if pad is None:


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/matplotlib/figure.py in get_tightbbox(self, renderer, bbox_extra_artists)
       2365 
       2366         for a in artists:
    -> 2367             bbox = a.get_tightbbox(renderer)
       2368             if bbox is not None and (bbox.width != 0 or bbox.height != 0):
       2369                 bb.append(bbox)


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/matplotlib/legend.py in get_tightbbox(self, renderer)
       1020         `.BboxBase` : containing the bounding box in figure pixel co-ordinates.
       1021         """
    -> 1022         return self._legend_box.get_window_extent(renderer)
       1023 
       1024     def get_frame_on(self):


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/matplotlib/offsetbox.py in get_window_extent(self, renderer)
        242         '''
        243         w, h, xd, yd, offsets = self.get_extent_offsets(renderer)
    --> 244         px, py = self.get_offset(w, h, xd, yd, renderer)
        245         return mtransforms.Bbox.from_bounds(px - xd, py - yd, w, h)
        246 


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/matplotlib/offsetbox.py in get_offset(self, width, height, xdescent, ydescent, renderer)
        194         """
        195         return (self._offset(width, height, xdescent, ydescent, renderer)
    --> 196                 if callable(self._offset)
        197                 else self._offset)
        198 


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/matplotlib/legend.py in _findoffset(self, width, height, xdescent, ydescent, renderer)
        625 
        626         if self._loc == 0:  # "best".
    --> 627             x, y = self._find_best_position(width, height, renderer)
        628         elif self._loc in Legend.codes.values():  # Fixed location.
        629             bbox = Bbox.from_bounds(0, 0, width, height)


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/matplotlib/legend.py in _find_best_position(self, width, height, renderer, consider)
       1124         assert self.isaxes
       1125 
    -> 1126         verts, bboxes, lines, offsets = self._auto_legend_data()
       1127         if self._loc_used_default and verts.shape[0] > 200000:
       1128             # this size results in a 3+ second render time on a good machine


    ~/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/matplotlib/legend.py in _auto_legend_data(self)
        931 
        932         try:
    --> 933             vertices = np.concatenate([l.vertices for l in lines])
        934         except ValueError:
        935             vertices = np.array([])


    KeyboardInterrupt: 



```python
_da.sum(fa.get_dims_complement(_da,[co.TIME])).plot()
```




    [<matplotlib.lines.Line2D at 0x7fe7f53049e8>]




![png](check_heght_files/check_heght_12_1.png)



```python
nds[co.CONC].sum(fa.get_dims_complement(nds[co.CONC],[co.TIME])).plot()
```




    [<matplotlib.lines.Line2D at 0x7fe7f523a4a8>]




![png](check_heght_files/check_heght_13_1.png)



```python
_n = nds[{co.RL:-1}]

_n1 = _n.coarsen(**{co.TIME:11},boundary='trim').sum().sum(co.ZM)[co.CONC].load()

_n1.plot.pcolormesh(col=co.TIME,col_wrap=5)
```




    <xarray.plot.facetgrid.FacetGrid at 0x7fe7f4c40a20>




![png](check_heght_files/check_heght_14_1.png)



```python
args = {'norm':mpl.colors.LogNorm(vmin=10,vmax=500),'cmap':plt.get_cmap('Reds')}
```


```python
_n = nds[{co.RL:1}][co.CONC]
_n = _n.where(_n>0)
_n = _n.dropna(dim=co.TIME,how='all')
_n = _n[{co.TIME:slice(-24,None)}]

_n1 = _n.coarsen(**{co.TIME:2},boundary='trim').sum().sum(co.ZM).load()
_n1.plot.pcolormesh(col=co.TIME,col_wrap=5,**args)
_n1 = _n.coarsen(**{co.TIME:2},boundary='trim').sum().sum(co.VLAT).load()
_n1.plot.pcolormesh(col=co.TIME,col_wrap=5,yscale='log',ylim=(1e2,1e5),**args)
_n1 = _n.coarsen(**{co.TIME:2},boundary='trim').sum().sum(co.VLONG).load()
_n1.plot.pcolormesh(col=co.TIME,col_wrap=5,yscale='log',ylim=(1e2,1e5),**args)
```

    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/plot/plot.py:849: UserWarning: Attempted to set non-positive bottom ylim on a log-scaled axis.
    Invalid limit will be ignored.
      ax.set_ylim(y[0], y[-1])
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/plot/plot.py:849: UserWarning: Attempted to set non-positive bottom ylim on a log-scaled axis.
    Invalid limit will be ignored.
      ax.set_ylim(y[0], y[-1])





    <xarray.plot.facetgrid.FacetGrid at 0x7fe7ee5902e8>




![png](check_heght_files/check_heght_16_2.png)



![png](check_heght_files/check_heght_16_3.png)



![png](check_heght_files/check_heght_16_4.png)



```python

```


```python
_n = nds[{co.RL:-1}][co.CONC]
_n = _n.where(_n>0)
_n = _n.dropna(dim=co.TIME,how='all')
_n = _n[{co.TIME:slice(-24,None)}]


_n1 = _n.coarsen(**{co.TIME:2},boundary='trim').sum().sum(co.ZM).load()
_n1.plot.pcolormesh(col=co.TIME,col_wrap=5,**args)
_n1 = _n.coarsen(**{co.TIME:2},boundary='trim').sum().sum(co.VLAT).load()
_n1.plot.pcolormesh(col=co.TIME,col_wrap=5,yscale='log',ylim=(1e2,1e5),**args)
_n1 = _n.coarsen(**{co.TIME:2},boundary='trim').sum().sum(co.VLONG).load()
_n1.plot.pcolormesh(col=co.TIME,col_wrap=5,yscale='log',ylim=(1e2,1e5),**args)
```

    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/plot/plot.py:849: UserWarning: Attempted to set non-positive bottom ylim on a log-scaled axis.
    Invalid limit will be ignored.
      ax.set_ylim(y[0], y[-1])
    /homeappl/home/aliagadi/appl_taito/miniconda3/envs/b36backup/lib/python3.6/site-packages/xarray/plot/plot.py:849: UserWarning: Attempted to set non-positive bottom ylim on a log-scaled axis.
    Invalid limit will be ignored.
      ax.set_ylim(y[0], y[-1])





    <xarray.plot.facetgrid.FacetGrid at 0x7fe7e44b59b0>




![png](check_heght_files/check_heght_18_2.png)



![png](check_heght_files/check_heght_18_3.png)



![png](check_heght_files/check_heght_18_4.png)



```python
!pwd
```

    /homeappl/home/aliagadi/saltena_2018/flexpart_management/flexpart_management/notebooks/run_2019-08-18_18-46-19_/check_height



```python

```
