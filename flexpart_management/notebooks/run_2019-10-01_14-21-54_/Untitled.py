# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from useful_scit.imps import (pd,np,xr,za,mpl,plt,sns, pjoin, os,glob,dt,
                            sys,ucp,log, splot, crt,axsplot)
import flexpart_management.modules.constants as co
ucp.set_dpi(200)

# %%
path = '/homeappl/home/aliagadi/wrk/DONOTREMOVE/flexpart_management_data/'+\
'runs/run_2019-10-01_14-21-54_/2018-01-05/'

# %%
from useful_scit.imps import *
import typing
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.FLEXOUT as FO

# %%
fo = FO.FLEXOUT(dom='d02',folder_path=path,folder_path_out='./',run_name='name',process=False)

# %%
fo.process_log_coords()

# %%
fo.flexout_ds[co.TIME].plot()

# %%
fo.flexout_ds[{co.RL:slice(-4,None)}
             ].squeeze().sum([co.BT,co.SN,co.WE])[co.CONC].plot(hue=co.RL)


# %%
log.ger.setLevel(log.log.DEBUG)
lp_ds = fo.get_log_polar_coords(release=fo.flexout_ds[co.RL][-3].values,
                               coords_to_keep=[co.BT,co.SN,co.WE,'Time_h'],
                               keep_list = [co.RL,'Time_h',co.ZT])

# %%
_lp=lp_ds.squeeze()[co.CONC]
_lp = _lp.where(_lp<1e10,0)

# %%
_lp1=_lp.sum([co.ZTOP])

# %%
_lp1.loc[{'Time_h':slice(None,-1)}].plot(yscale='log',ylim=(.05,10),col='Time_h',robust=True,col_wrap=4,
                                       cmap=plt.get_cmap('Reds'))

# %%
_lp.sum([co.TH_CENTER,co.R_CENTER])

# %%
