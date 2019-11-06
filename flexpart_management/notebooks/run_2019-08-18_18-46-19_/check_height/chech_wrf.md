```python
from useful_scit.imps import (pd,np,xr,za,mpl,plt,sns, pjoin,
                              os,glob,dt,sys,ucp,log, splot)
import cartopy.crs as crs
```


```python
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
```


```python
path = '/proj/atm/saltena/runs/run_2019_05_15/wrf/'
```


```python
files = glob.glob(path+'wrfout*d04*2017-12-31*')
files.sort()
```


```python
TIME = 'Time'
PBLH = 'PBLH'
XTIME = 'XTIME'
LTIME = 'LOCAL TIME'
```


```python
dso = ds = xr.open_mfdataset(files,concat_dim=TIME,combine='nested')
for ll in [co.XLAT,co.XLONG]:
    ds[ll] = ds[ll].mean(co.TIME)
ds[co.XLAT] = ds[co.XLAT].mean(co.WE).load()
ds[co.XLONG] = ds[co.XLONG].mean(co.SN).load()
```


```python
ds[LTIME]=(ds[XTIME].to_pandas()-pd.Timedelta(hours=4)).to_xarray()
```


```python
ds = ds.swap_dims({co.WE:co.XLONG,co.SN:co.XLAT,co.TIME:LTIME})
```


```python
ax = fa.get_ax_lapaz()
ds[PBLH][{LTIME:-1}].plot(ax=ax,transform=crs.PlateCarree())
fa.add_chc_lpb(ax)
ax.set_xlim(co.CHC_LON-1,co.CHC_LON+1)
ax.set_ylim(co.CHC_LAT-1,co.CHC_LAT+1)
```




    (-17.350427, -15.350427)




![png](chech_wrf_files/chech_wrf_8_1.png)



```python
__ds = ds[PBLH]#[{co.TIME:-1}]
```


```python
_,ax = splot(figsize=(10,5))
_ds = __ds.sel({co.XLAT:co.CHC_LAT},method='nearest')
_ds = _ds.plot.line(ax=ax,hue=LTIME,add_legend=False,alpha=.5)
ax.axvline(co.CHC_LON,color='k')
```




    <matplotlib.lines.Line2D at 0x7f36dff41320>




![png](chech_wrf_files/chech_wrf_10_1.png)



```python
_,ax = splot(figsize=(10,5))
_ds = __ds.sel({co.XLAT:co.CHC_LAT},method='nearest')
_ds = _ds.plot(ax=ax,levels=10,cmap=plt.get_cmap('Reds'))
ax.axvline(co.CHC_LON,color='k')
ax.grid(True,linestyle='--',color='k')
ax.set_axisbelow(False)
```


![png](chech_wrf_files/chech_wrf_11_0.png)



```python
_ds = __ds.sel({co.XLAT:co.CHC_LAT,co.XLONG:co.CHC_LON},method='nearest')
```


```python
_ds.plot()
```




    [<matplotlib.lines.Line2D at 0x7f8ffa12ecf8>]




![png](chech_wrf_files/chech_wrf_13_1.png)



```python
_ds.min().load()
```




    <xarray.DataArray 'PBLH' ()>
    array(44.62256, dtype=float32)
    Coordinates:
        XLAT     float32 -16.35415
        XLONG    float32 -68.136345




```python
ll=list(ds.variables)
ll.sort()
```


```python
_ds = ds['TKE_PBL'].sel({co.XLAT:co.CHC_LAT,co.XLONG:co.CHC_LON},method='nearest')
```


```python
_ds.plot(x=LTIME,cmap=plt.get_cmap('Reds'))
```




    <matplotlib.collections.QuadMesh at 0x7f8ff9e01f28>




![png](chech_wrf_files/chech_wrf_17_1.png)



```python
_ds = ds['W'].sel({co.XLAT:co.CHC_LAT,co.XLONG:co.CHC_LON},method='nearest')
_ds.plot(x=LTIME,cmap=plt.get_cmap('RdBu_r'))
```




    <matplotlib.collections.QuadMesh at 0x7f8ff8f1b208>




![png](chech_wrf_files/chech_wrf_18_1.png)



```python
file_objs = dso._file_obj.file_objs
```


```python
fds = []
for f in file_objs:
    fds.append(f.ds)
```


```python
z = wrf.getvar(fds,'wa')
z
```




    <xarray.DataArray 'wa' (bottom_top: 49, south_north: 150, west_east: 153)>
    array([[[-0.018474, -0.018575, ...,  0.051077,  0.051583],
            [-0.016205, -0.013031, ...,  0.034716,  0.058396],
            ...,
            [ 0.05208 ,  0.026403, ...,  0.017713,  0.031059],
            [ 0.059268,  0.041391, ...,  0.017977,  0.017071]],
    
           [[-0.066681, -0.066028, ...,  0.047494,  0.066744],
            [-0.059876, -0.052877, ...,  0.027261,  0.068518],
            ...,
            [ 0.047792,  0.047965, ...,  0.051564,  0.113028],
            [ 0.058062,  0.057922, ...,  0.064514,  0.07741 ]],
    
           ...,
    
           [[ 0.026223,  0.024132, ...,  0.057854,  0.058898],
            [ 0.036509,  0.037556, ...,  0.060485,  0.053659],
            ...,
            [ 0.012881,  0.015542, ..., -0.017599, -0.01466 ],
            [ 0.015666,  0.015542, ..., -0.017273, -0.014995]],
    
           [[ 0.012212,  0.010027, ...,  0.020951,  0.021668],
            [ 0.016199,  0.015829, ...,  0.019539,  0.019085],
            ...,
            [ 0.003278,  0.003943, ..., -0.002695, -0.001663],
            [ 0.004767,  0.004766, ..., -0.00199 , -0.001247]]], dtype=float32)
    Coordinates:
        XLONG    (south_north, west_east) float32 -68.95856 -68.94759 ... -67.29216
        XLAT     (south_north, west_east) float32 -17.15197 -17.15197 ... -15.58474
        XTIME    float32 41760.0
        Time     datetime64[ns] 2017-12-31
    Dimensions without coordinates: bottom_top, south_north, west_east
    Attributes:
        FieldType:    104
        MemoryOrder:  XYZ
        description:  destaggered w-wind component
        units:        m s-1
        stagger:      
        coordinates:  XLONG XLAT XTIME
        projection:   Mercator(stand_lon=-66.30000305175781, moad_cen_lat=-17.000...




```python
_dds = wrf.vinterp(fds[0],z,'ght_msl',[0,1,2,3,4,5,6])
```


```python
_dds.plot.pcolormesh(col='interp_level',col_wrap=2,size=6)
```




    <xarray.plot.facetgrid.FacetGrid at 0x7f8ff5f150b8>




![png](chech_wrf_files/chech_wrf_23_1.png)



```python
base_fun = xr.DataArray.plot.pcolormesh
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-207-2c3e3bfa8f60> in <module>
    ----> 1 base_fun = xr.DataArray.plot.pcolormesh
    

    AttributeError: 'property' object has no attribute 'pcolormesh'



```python
_dds.plot.pcolormesh
```




    <bound method pcolormesh of <xarray.plot.plot._PlotMethods object at 0x7f8ff5c21390>>




```python
base_pcolormesh = xr.plot.pcolormesh
```


```python
_dds.sum('interp_level').plot.pcolormesh()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-22-a9562c5b5f66> in <module>
    ----> 1 _dds.sum('interp_level').plot.pcolormesh()
    

    NameError: name '_dds' is not defined



```python

```
