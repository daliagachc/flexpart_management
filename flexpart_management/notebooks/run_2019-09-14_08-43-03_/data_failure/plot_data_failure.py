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
from useful_scit.imps import (pd,np,xr,za,mpl,plt,sns, pjoin,
                               os,glob,dt,sys,ucp,log, splot)

# %%
import data_failure as df

# %%

# %%
f.add_subplot

# %%
f = plt.Figure(figsize=(10,10))
for i,(p,v) in enumerate(df.pars.items()):
    ax = f.add_subplot(1,len(df.pars),i+1)
    y = range(0,len(v))
    _l = ax.plot(v,y)
    ax.set_ylabel('index'); ax.set_xlabel(p)
f.tight_layout()
f

# %%
