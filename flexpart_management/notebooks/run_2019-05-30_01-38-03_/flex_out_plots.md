

```python
%load_ext autoreload
%autoreload 2
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload



```python
import flexpart_management.modules.flx_array as fa
```


```python
ds = xr.open_dataset('/tmp/dd4.nc')
ds2 = xr.open_dataset('/tmp/dd02.nc')
```


```python
i = 0 
for i in range(len(ds[fa.RL])):
    di = ds[{fa.RL:i}]
    dii = di[fa.CONC].sum(dim=[fa.TIME,fa.ZM])
    ax = fa.get_ax_bolivia()
    diii = dii * di[fa.LL_DIS]
    diii.plot(ax=ax,cmap=fa.red_cmap(),vmax=800)
    fa.add_chc_lpb(ax)
```

    /Users/diego/flexpart_management/flexpart_management/modules/flx_array.py:303: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      fig = plt.figure(figsize=(15, 10))
    /Users/diego/flexpart_management/flexpart_management/modules/flx_array.py:303: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      fig = plt.figure(figsize=(15, 10))
    /Users/diego/flexpart_management/flexpart_management/modules/flx_array.py:303: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      fig = plt.figure(figsize=(15, 10))
    /Users/diego/flexpart_management/flexpart_management/modules/flx_array.py:303: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      fig = plt.figure(figsize=(15, 10))



![png](flex_out_plots_files/flex_out_plots_3_1.png)



![png](flex_out_plots_files/flex_out_plots_3_2.png)



![png](flex_out_plots_files/flex_out_plots_3_3.png)



![png](flex_out_plots_files/flex_out_plots_3_4.png)



![png](flex_out_plots_files/flex_out_plots_3_5.png)



![png](flex_out_plots_files/flex_out_plots_3_6.png)



![png](flex_out_plots_files/flex_out_plots_3_7.png)



![png](flex_out_plots_files/flex_out_plots_3_8.png)



![png](flex_out_plots_files/flex_out_plots_3_9.png)



![png](flex_out_plots_files/flex_out_plots_3_10.png)



![png](flex_out_plots_files/flex_out_plots_3_11.png)



![png](flex_out_plots_files/flex_out_plots_3_12.png)



![png](flex_out_plots_files/flex_out_plots_3_13.png)



![png](flex_out_plots_files/flex_out_plots_3_14.png)



![png](flex_out_plots_files/flex_out_plots_3_15.png)



![png](flex_out_plots_files/flex_out_plots_3_16.png)



![png](flex_out_plots_files/flex_out_plots_3_17.png)



![png](flex_out_plots_files/flex_out_plots_3_18.png)



![png](flex_out_plots_files/flex_out_plots_3_19.png)



![png](flex_out_plots_files/flex_out_plots_3_20.png)



![png](flex_out_plots_files/flex_out_plots_3_21.png)



![png](flex_out_plots_files/flex_out_plots_3_22.png)



![png](flex_out_plots_files/flex_out_plots_3_23.png)



![png](flex_out_plots_files/flex_out_plots_3_24.png)



```python
for i in range(len(ds[fa.RL])):
# for i in range(1):
    di = ds2[{fa.RL:i}]
    dii = di[fa.CONC].sum(dim=[fa.TIME,fa.ZM])
    ax = fa.get_ax_lapaz()
    diii = dii * di[fa.LL_DIS]
    diii.plot(ax=ax,cmap=fa.red_cmap(),vmax=5)
    fa.add_chc_lpb(ax)
```

    /Users/diego/flexpart_management/flexpart_management/modules/flx_array.py:327: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      fig = plt.figure(figsize=(15, 10))
    /Users/diego/flexpart_management/flexpart_management/modules/flx_array.py:327: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      fig = plt.figure(figsize=(15, 10))
    /Users/diego/flexpart_management/flexpart_management/modules/flx_array.py:327: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      fig = plt.figure(figsize=(15, 10))
    /Users/diego/flexpart_management/flexpart_management/modules/flx_array.py:327: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
      fig = plt.figure(figsize=(15, 10))



![png](flex_out_plots_files/flex_out_plots_4_1.png)



![png](flex_out_plots_files/flex_out_plots_4_2.png)



![png](flex_out_plots_files/flex_out_plots_4_3.png)



![png](flex_out_plots_files/flex_out_plots_4_4.png)



![png](flex_out_plots_files/flex_out_plots_4_5.png)



![png](flex_out_plots_files/flex_out_plots_4_6.png)



![png](flex_out_plots_files/flex_out_plots_4_7.png)



![png](flex_out_plots_files/flex_out_plots_4_8.png)



![png](flex_out_plots_files/flex_out_plots_4_9.png)



![png](flex_out_plots_files/flex_out_plots_4_10.png)



![png](flex_out_plots_files/flex_out_plots_4_11.png)



![png](flex_out_plots_files/flex_out_plots_4_12.png)



![png](flex_out_plots_files/flex_out_plots_4_13.png)



![png](flex_out_plots_files/flex_out_plots_4_14.png)



![png](flex_out_plots_files/flex_out_plots_4_15.png)



![png](flex_out_plots_files/flex_out_plots_4_16.png)



![png](flex_out_plots_files/flex_out_plots_4_17.png)



![png](flex_out_plots_files/flex_out_plots_4_18.png)



![png](flex_out_plots_files/flex_out_plots_4_19.png)



![png](flex_out_plots_files/flex_out_plots_4_20.png)



![png](flex_out_plots_files/flex_out_plots_4_21.png)



![png](flex_out_plots_files/flex_out_plots_4_22.png)



![png](flex_out_plots_files/flex_out_plots_4_23.png)



![png](flex_out_plots_files/flex_out_plots_4_24.png)



```python

```
