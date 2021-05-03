# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.7.0-rc1
#   kernelspec:
#     display_name: Python [conda env:b36]
#     language: python
#     name: conda-env-b36-py
# ---

# %%
import flexpart_management.notebooks.release_ds_v3.release_ds_v3_lfc as lfc
from flexpart_management.notebooks.release_ds_v3.release_ds_v3_lfc import *


# %%


def main():
    # %%
    ds = get_dcc().load()
    # %%
    b1 = ds[co.R_CENTER] > .10
    b2 = ds[co.R_CENTER] < .25
    t1 = ds[co.TH_CENTER] > 5 * np.pi/6
    t2 = ds[co.TH_CENTER] < 7.5 * np.pi/6
# %%

    # %%
    _rt = {co.R_CENTER:(b1 & b2),co.TH_CENTER: (t1 & t2)}
    dlp0 = ds[{**_rt, co.ZM:[0]}]
    dlp1 = ds[{**_rt, co.ZM:[0,1]}]
    dlp2 = ds[{**_rt, co.ZM:[0,1,2]}]
    dlpt = ds[{**_rt}]
    # %%
    dls = [dlp0,dlp1,dlp2,dlpt]
    dss = ['lp0','lp1','lp2','lpt']
    # s = splot(figsize=(20,4))
    df = pd.DataFrame([])
    for dl,dds in zip(dls,dss):
        ser = dl.sum(NRL).to_dataframe()[CO]
        df[dds] = ser
        # ser[CO].to_dataframe().plot(ax=s.ax)
    # plt.show()
    # df = df / df.mean()
    # %%
    df_ts = import_time_series()
    df_ts[co.RL] = df_ts.index
    df_ts = df_ts.set_index(co.RL)
    # %%
    df_ts = df_ts.resample('H').mean()
    # %%
    csv = xr.open_dataset(pjoin(co.tmp_data_path,'cluster_series_v3.nc'))
    # %%
    s7 = csv['conc_lab_nc18'].loc[{N18:'07_SR',NORM:0,ZCOL:'BL'}].to_dataframe()[CL18]
    t7 = csv['conc_lab_nc18'].loc[{N18:'07_SR',NORM:0,ZCOL:'ALL'}].to_dataframe()[CL18]
    # %%
    s07=ds[CO][{co.ZM:[0]}].where(ds[N18]=='07_SR').sum(NRL).to_dataframe()
    s12=ds[CO][{co.ZM:[0]}].where(ds[N18]=='12_SR').sum(NRL).to_dataframe()
    s11=ds[CO][{co.ZM:[0]}].where(ds[N18]=='11_SR').sum(NRL).to_dataframe()
    s04=ds[CO][{co.ZM:[0]}].where(ds[N18]=='04_SR').sum(NRL).to_dataframe()
    s02=ds[CO][{co.ZM:[0]}].where(ds[N18]=='02_SR').sum(NRL).to_dataframe()
    s10=ds[CO][{co.ZM:[0]}].where(ds[N18]=='10_SR').sum(NRL).to_dataframe()



    # %%
    surf = ds[CO][{co.ZM:[0]}].loc[{co.R_CENTER:slice(0,.30)}].sum(NRL).to_dataframe()
# %%

    df['s7'] = s7
    df['t7'] = t7
    df['s07'] = s07
    df['BC'] = df_ts['BC']
    df[c91] = df_ts[c91]
    df['surf'] = surf
    df['s12'] = s12
    df['s11'] = s11
    df['s04'] = s04
    df['s02'] = s02
    df['s10'] = s10
# %%

    df_ts = import_time_series()
    df_ts
    # %%
    # df = ser.to_dataframe().reset_index()
    # df['LT']  = df[co.RL] - pd.Timedelta('4H')
    # from bokeh.plotting import figure, output_file, show
    # import bokeh
    # from bokeh.models import ColumnDataSource
    # from bokeh.palettes import Dark2_5 as palette
    # output_file('/tmp/my_first_graph.html')
    # p = figure(x_axis_type='datetime',plot_width=1000, plot_height=500)
    # source = ColumnDataSource(df)
    #
    # p.line(x='LT', y=CO, source=source, )
    # p.line(x='Time_LT', y=c91, source=df_ts, color = palette[1])
    # show(p)

    # %%
    # bcc = df_ts[['RH_station']].resample('H').mean().dropna()
    bcc = df_ts[['BC']].resample('H').mean().dropna()
    bc = bcc['BC']
    # %%
    import sklearn.preprocessing as pre
    bcT = pre.QuantileTransformer(
        output_distribution='normal',n_quantiles=100)\
        .fit_transform(bcc.values)
    bcL = pre.QuantileTransformer(n_quantiles=100) \
        .fit_transform(bcc.values)
    # %%
    bcc['bcT'] = bcT
    bcc['bc2'] = bcT+2
    bcc.index.name=co.RL

    # %%
    # s = splot(3,squeeze=False)
    # ax0,ax1,ax2 = s.axf[0],s.axf[1],s.axf[2]
    # x1 = 3
    # x2 = 5000
    # bins = np.geomspace(x1,x2,10)
    # bins = [0,*bins[1:-1],np.max([bc.max()+1,bins[-1]])]
    # ax0.hist(bc, bins=bins)
    # ax0.set_xlim(x1,x2)
    # ax0.set_xscale('log')
    # ax0.set_title('log')
    # ax1.hist(bc,bins=100)
    # ax1.set_title('normal')
    #
    # ax2.hist(bcT)
    # ax2.set_title('bc quantile')
    # s.f.tight_layout()
    # plt.show()

    # %%
    dsc = xr.open_dataset(
        pjoin(co.tmp_data_path,'cluster_series_v3.nc'))
    # %%
    ser = dsc['conc_lab_nc18'].loc[{'z_column':'BL','normalized':0}]
    # %%
    import sklearn.linear_model as lm
    reg = lm.ElasticNet(
        positive=True,)
    # %%
    su = ds[{co.ZM:[0]}].sum([co.RL,co.ZM])
    # %%
    su[co.CONC].plot.hist()
    plt.show()


    # %%
    sun = ds[{co.ZM:0}]/su
    # sun = ds/ds.sum(co.RL)
    # %%
    dsun = sun.to_dataframe()[co.CONC]
    dsun = dsun[~dsun.isnull()]
# %%
    # %%
    du = dsun.unstack().T
    # %%
    # bcc['rat'] = (bcc['C4_C5_compounds']/bcc['C9_C13_compounds'])[bcc['C9_C13_compounds']>0]
    # buc = bcc[['RH_station']]['2017-12-06':'2018-05-31'].dropna().copy()
    buc = bcc[['BC']]['2017-12-06':'2018-05-31'].dropna().copy()
    duc = du.loc[buc.index].copy()

    reg = lm.ElasticNet(positive=True,alpha=.17,fit_intercept=False)
    reg.fit(duc,buc)
    we = pd.DataFrame(reg.coef_, index=duc.T.index,columns=['w'])
    we.to_xarray()['w'].plot()
    ax = plt.gca()
    ax.set_yscale('log')
    plt.show()
# %%

    # %%
    import cartopy
    dd = .8 
    lo_c = -68.5
    la_c = -16
    lom = lo_c-dd
    loM = lo_c+dd
    lam = la_c-dd
    laM = la_c+dd
    ww='$P_w$ [%]'
    goo = xr.merge([su,we.to_xarray()])*100
    goo = goo.rename({'w':ww})
    ax = fa.get_ax_lapaz(
        fig_args={'figsize':(5,4),'dpi':200},
        chc_lp_legend=True,
        lalo_extent=[lom,loM,lam,laM],
        lola_ticks=[[-69.0,-68.5,-68.0],[-16.5,-16.0,-15.5]],
        y_left_lab=True,
        map_line_alpha=1,
        borders=False,
        plot_cities=False,
        lake_face_color=cartopy.feature.COLORS['water'],
        grid_color='white'
    )
    
    fa.logpolar_plot(goo[ww], ax=ax,name=ww)
    ax.plot(co.lola_la_paz_pol[:, 0], co.lola_la_paz_pol[:, 1],c='g')
#     ax.get_legend().remove()


    base_uri = 'https://map1c.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi'

    layer_name ='VIIRS_Black_Marble'

    # Create a Cartopy crs for plain and rotated lat-lon projections.
    plain_crs = ccrs.PlateCarree()


#     fig = plt.figure(dpi=300)
    
#     la,lo = -16.4897, -68.1193

    dd = 1
    # Plot WMTS data in a specific region, over a plain lat-lon map.
#     ax = fig.add_subplot(1, 2, 1, projection=plain_crs)
#     ax.set_extent([lo-dd, lo+dd, la-dd, la+dd], crs=ccrs.PlateCarree())
#     ax.coastlines(resolution='50m', color='yellow')
#     ax.gridlines(color='lightgrey', linestyle='-')
    # Add WMTS imaging.
    ax.add_wmts(base_uri, layer_name=layer_name, wmts_kwargs={'time': '2016-01-01'})

    plt.show()

    ax.figure.savefig('bams_lapaz_bc.pdf')

# %%
if __name__ == '__main__':
    main()

# %%

# %%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def plot_city_lights():
    # Define resource for the NASA night-time illumination data.
    base_uri = 'https://map1c.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi'

    layer_name ='VIIRS_Black_Marble'

    # Create a Cartopy crs for plain and rotated lat-lon projections.
    plain_crs = ccrs.PlateCarree()


    fig = plt.figure(dpi=300)
    
    la,lo = -16.4897, -68.1193

    dd = 1
    # Plot WMTS data in a specific region, over a plain lat-lon map.
    ax = fig.add_subplot(1, 2, 1, projection=plain_crs)
    ax.set_extent([lo-dd, lo+dd, la-dd, la+dd], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='50m', color='yellow')
    ax.gridlines(color='lightgrey', linestyle='-')
    # Add WMTS imaging.
    ax.add_wmts(base_uri, layer_name=layer_name, wmts_kwargs={'time': '2012-01-01'})

#     layer_name ='VIIRS_Black_Marble'
    
    
    ax = fig.add_subplot(1, 2, 2, projection=plain_crs)
    ax.set_extent([lo-dd, lo+dd, la-dd, la+dd], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='50m', color='yellow')
    ax.gridlines(color='lightgrey', linestyle='-')
    # Add WMTS imaging.
    ax.add_wmts(base_uri, layer_name=layer_name, wmts_kwargs={'time': '2016-01-01'})

    plt.show()


if __name__ == '__main__':
    plot_city_lights()

# %%
