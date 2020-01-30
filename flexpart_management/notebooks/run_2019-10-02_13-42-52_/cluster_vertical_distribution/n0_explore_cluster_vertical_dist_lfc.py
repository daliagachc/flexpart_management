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
from scipy.signal import savgol_filter
from useful_scit.imps import *
from flexpart_management.modules import\
    flx_array as fa, constants as co

LIST_PLOT = [0, 1, 3, 7, 14, 29]

z_lim = 1500
boundary_lab = 'boundary_lab'
# %%

def plot_bl_ft(ds_comb):
    df_comb = ds_comb.to_dataframe()
    df_comb.plot.area()
    ax = plt.gca()
    ax.set_ylabel('SRR')
    ax.figure.tight_layout()
    plt.show()


# %%


def process_ds_zg(ds_zg, cum_sum_start=0):
    da_conc = ds_zg[co.CONC]
    comp_dim = fa.get_dims_complement(da_conc, co.RL)
    # %%
    da_tot = da_conc.sum(comp_dim)
    comp_z = fa.get_dims_complement(da_conc, [co.RL, co.ZM])
    da_zi = da_conc[{co.ZM: slice(0, None)}].sum(comp_z) / da_tot * 100
    slice_da = da_zi[{co.ZM: slice(cum_sum_start, None)}]
    da_zi_cumsum = slice_da.cumsum(co.ZM)
    da_norm = da_zi_cumsum / da_zi_cumsum.mean(co.RL)
    return comp_dim, da_conc, da_norm, da_zi_cumsum


def plot_cum_sum(da_zi):

    da_plot = da_zi[{co.ZM: LIST_PLOT}]
    cozt: xr.DataArray = da_plot[co.ZT]
    attrs = {'long_name': 'Ztop', 'units': 'mag'}
    da_plot[co.ZT] = cozt.assign_attrs(attrs)
    dz_ = r'$\int_{z=0}^{z=z_{top}}{\mathrm{SRR}_{\mathrm{pc}}(t,z)} \,dz$'
    attrs = {'long_name': dz_, 'units': '%'}
    da_plot = da_plot.assign_attrs(attrs)
    da_plot.plot.line(x=co.RL, figsize=(20, 10), alpha=.6, hue=co.ZT)
    plt.gca().set_ylabel(dz_)
    plt.show()


def plot_norm_cum_sum(da_norm):
    da_plot = da_norm[{co.ZM: LIST_PLOT}]
    da_plot.load()
    # %%
    da_plot.plot.line(
        x=co.RL,
        figsize=(20, 10),
        alpha=.5,
        hue=co.ZT
    )
    dz_ = r'\int_{z=0}^{z=z_{top}}{\mathrm{SRR}_{\mathrm{pc}}(t,z)} \,dz'
    dzn = r'$\frac{' + dz_ + r'}{\int^t{' + dz_ + r'}\,dt}$'
    plt.gca().set_ylabel(dzn)
    plt.show()


def plot_z0_timeseries(da_z0):
    da_z0.plot(figsize=(40, 5));
    plt.show()


def plot_sg_filter(da_z0, ds_z0):
    da_z0.plot(figsize=(40, 5))
    ds_z0['sf'].plot()
    plt.show()


def savgol_filtering(da_z0):
    ds_z0 = da_z0.to_dataset()
    ds_z0['sf'] = da_z0.copy()
    ds_z0['sf'].data = savgol_filter(da_z0, 49, 1)
    detr = 'detr'
    ds_z0[detr] = ds_z0[co.CONC] - ds_z0['sf']
    ds_z0['detr_median'] = ds_z0[detr] + ds_z0['sf'].median()
    # ds_z0['detr'].plot();plt.show()
    df0 = ds_z0.reset_coords(drop=True).to_dataframe()
    df0['loc_time'] = df0.index - pd.Timedelta(hours=4)
    df0['hour'] = df0['loc_time'].dt.hour
    return df0, ds_z0


def plot_diurnal_variation_z0_level(df0):
    f,ax=plt.subplots(dpi=150)
    sns.boxplot('hour', 'detr_median', data=df0, color=[.95, .95, .95],ax=ax)
    plt.show()


def notation_for_diurnal_plot():
    import matplotlib.image as mpimg
    img = mpimg.imread(
        '/Users/diego/flexpart_management/flexpart_management/pics/IMG_20200127_175726089.jpg')
    f,ax = plt.subplots(figsize=(15,15))
    ax.imshow(img)
    plt.show()


def plot_histogram_vertical_masl(da_conc,ds):
    zt_dim_comp = fa.get_dims_complement(da_conc, co.ZM)
    da_z = da_conc.sum(zt_dim_comp)
    da_z = da_z/da_z.sum()*100
    # %%
    dfz = da_z.reset_coords(drop=True).to_dataframe().reset_index()

    dz_conc = ds[co.CONC].sum(fa.get_dims_complement(ds[co.CONC], co.ZM))
    dz_conc = dz_conc/dz_conc.sum()*100
    df_conc = dz_conc.reset_coords(drop=True).to_dataframe().reset_index()

    # plt.show()
    f, ax = plt.subplots(figsize=(4, 5),dpi=150)
    df_conc.plot(x=co.CONC, y=co.ZM, ax=ax,
                 label='z asl', marker='o')
    dfz.plot(x=co.CONC, y=co.ZM, ax=ax, label='z agl',marker='o')
    ax.grid()
    ax.set_xlim(0,13)
    plt.tight_layout()
    plt.show()