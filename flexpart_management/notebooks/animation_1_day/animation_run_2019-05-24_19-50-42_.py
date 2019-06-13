# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.1.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

# %%
from useful_scit.imps import *
import flexpart_management.modules.FLEXOUT as FX
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

# %%
path = '/Volumes/mbProD/Downloads/flex_out/run_2019-06-02_20-42-05_/2017-12-10'

# %%
fd1 = FX.FLEXOUT('d01',path,'/tmp/')

# %%
rel = 14 
dh = 24
lh = 96

# %%
ds = fd1.flexout_ds[{co.RL:rel}]
# ds.load();

# %%
ds1 = ds[{co.TIME:slice(rel-2,rel+lh+3)}]

# %%
lt = len(ds1[co.TIME])

# %%
rl = [] 
for i in range(lt):
    res = fa.data_array_to_logpolar(
        ds1[co.CONC][i,0,:],
        r_round_log=co.ROUND_R_LOG,
        th_round_rad=co.ROUND_TH_RAD,
        dim2keep=[co.ZM,co.TIME]

    )
    print(i)
    rl.append(res)

# %%
dsL1 = xr.concat(rl[:],co.TIME)

# %%
fd2 = FX.FLEXOUT('d02',path,'/tmp/')

# %%
rel = 14 
dh = 24
lh = 96

# %%
ds = fd2.flexout_ds[{co.RL:rel}]
# ds.load();

# %%
ds1 = ds[{co.TIME:slice(rel-2,rel+lh+3)}]

# %%
lt = len(ds1[co.TIME])

# %%
rl = [] 
for i in range(lt):
    res = fa.data_array_to_logpolar(
        ds1[co.CONC][i,0,:],
        r_round_log=co.ROUND_R_LOG,
        th_round_rad=co.ROUND_TH_RAD,
        dim2keep=[co.ZM,co.TIME]

    )
    print(i)
    rl.append(res)

# %%
dsL2 = xr.concat(rl[:],co.TIME)

# %%
dsL2.sum(fa.get_dims_complement(dsL1,co.TIME)).plot()


# %%

def get_merged_ds(ds1,ds2):

    l2M = 24
    l2m = 10
    l1M = None
    l1m = 13
    d1 = ds1[{co.R_CENTER: slice(l1m, l1M)}]
    d2 = ds2[{co.R_CENTER: slice(l2m, l2M)}]
    mer = xr.merge([d1, d2])
    return mer



# %%
dl = get_merged_ds(dsL1,dsL2)

# %%
dp

# %%
i=2
mm = dl[co.CONC].sum(co.TH_CENTER).quantile(.985).values
def plot_for_offset(i):
    r = 2
    fig = plt.figure(figsize=(7,7))
    llm = dl[co.CONC].where(dl[co.CONC]>0).sum(co.ZM).quantile(.99)
    ax1 = fig.add_subplot(2,2,1,projection=co.PROJ)
    fa.get_ax_bolivia(ax=ax1)
    dp = dl[{co.TIME:i}].sum(co.ZM)
    fa.logpolar_plot(dp,ax=ax1,perM=llm,quantile=False,colorbar=False)
    fa.plot_lapaz_rect(ax=ax1)
    fa.add_chc_lpb(ax1)
    ax2 = fig.add_subplot(2,2,2,projection=co.PROJ)
    fa.get_ax_lapaz(ax=ax2)
    dp = dl[{co.TIME:i}].sum(co.ZM)
    fa.logpolar_plot(dp,ax=ax2,perM=llm,quantile=False,colorbar=True)
    fa.add_chc_lpb(ax2)
    ax = fig.add_subplot(r,1,r)
    fa.plot_clust_height(dl[{co.TIME:i}][co.CONC],ax=ax,perM=mm,quantile=False,par_to_plot=co.CONC)
    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)

    return image




# %%
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import imageio
kwargs_write = {'fps':1.0, 'quantizer':'nq'}
imageio.mimsave('./powers.gif', [plot_for_offset(i) for i in range(98,3,-1)], fps=2.5)

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%
