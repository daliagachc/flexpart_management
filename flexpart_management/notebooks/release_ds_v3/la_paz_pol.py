# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
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
    ax =fa.get_ax_lapaz(lalo_extent=[-68.5,-67.5,-17,-16,])
    lp_series = dlp0.sum([co.RL, co.ZM])
    fa.logpolar_plot(lp_series, ax=ax)
    ax.plot(co.lola_la_paz_pol[:,0],co.lola_la_paz_pol[:,1])
    plt.show()
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
    s7 = csv['conc_lab_nc18'].loc[{N18:'07_SR',NORM:0,ZCOL:'SURF'}].to_dataframe()[CL18]
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
    sns.heatmap(df.corr(), cmap='Reds',annot=True)
    plt.show()

    # %%
    from bokeh.plotting import figure, output_file, show
    import bokeh
    from bokeh.models import ColumnDataSource
    # noinspection PyUnresolvedReferences
    from bokeh.palettes import Category20 as palette
    _df = (df/df.mean()).reset_index()
    output_file('/tmp/my_first_graph.html')
    p = figure(x_axis_type='datetime',plot_width=1000, plot_height=500)
    _s = ['s07', 's7', 't7', 'lp0', 'lp1', 'lp2', 'lpt','BC',c91,'surf',
          's12','s11','s04','s02','s10'
          ]
    _l = ['7-level0 ','7-level012','7-levelall','lp-level0','lp-level1','lp-level012','lp-levelall',
          'BC',c91,'surf',
          's12', 's11', 's04', 's02', 's10'
          ]
    source = ColumnDataSource(_df)
    for c,y,l in zip(palette[20],_s,_l):
        # print(palette[c])
        p.line(x=co.RL, y=y, source=source, color = c,legend_label=l,line_width=2)
        # p.line(x=co.RL, y='lp0', source=source, color = palette[1])
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    show(p)

    # %%

    df_ts = import_time_series()
    df_ts
    # %%
    df = ser[CO].to_dataframe().reset_index()
    df['LT']  = df[co.RL] - pd.Timedelta('4H')
    from bokeh.plotting import figure, output_file, show
    import bokeh
    from bokeh.models import ColumnDataSource
    from bokeh.palettes import Dark2_5 as palette
    output_file('/tmp/my_first_graph.html')
    p = figure(x_axis_type='datetime',plot_width=1000, plot_height=500)
    source = ColumnDataSource(df)

    p.line(x='LT', y=CO, source=source, )
    p.line(x='Time_LT', y=c91, source=df_ts, color = palette[1])
    show(p)

    # %%
    # %%
    # %%
    # %%

