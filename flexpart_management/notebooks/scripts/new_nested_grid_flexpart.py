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
from useful_scit.imps import (pd,np,xr,za,mpl,plt,sns, pjoin, os,
                              glob,dt,sys,ucp,log, splot, crt,axsplot)

# %%
ucp.set_dpi(200)

# %%
x1 =0.0000000
y1 =0.0000000
xn1=468      
yn1=340              
dx1=9500.0   
dy1=9500.0   

x2=1946500.0  
y2=1588670.0  
xn2=153        
yn2=150                
dx2=1055.5556  
dy2=1055.5556 

_n = 3
ax2=np.round(1946500.0  + (xn2/2)*dx2 - _n*(xn2/2)*dx2)
ay2=np.round(1588670.0  + (yn2/2)*dy2 - _n*(yn2/2)*dy2)
axn2=xn2*_n     
ayn2=yn2*_n                
adx2=1055.5556  
ady2=1055.5556 

_ca = ucp.cc[0]
_cb = ucp.cc[1]

# %%
ax2,ay2,axn2,ayn2

# %%
ax = axsplot()

rect = mpl.patches.Rectangle((x1,y1),xn1*dx1,yn1*dy1)
pc = mpl.collections.PatchCollection([rect],edgecolor = _ca,facecolor='none')
ax.add_collection(pc)

rect = mpl.patches.Rectangle((x2,y2),xn2*dx2,yn2*dy2)
pc = mpl.collections.PatchCollection([rect],edgecolor = _ca,facecolor='none')
ax.add_collection(pc)

rect = mpl.patches.Rectangle((ax2,ay2),axn2*adx2,ayn2*ady2)
pc = mpl.collections.PatchCollection([rect],edgecolor = _cb,facecolor='none')
ax.add_collection(pc)

ax.set_xlim(-10*dx1,(xn1+10)*dx1)
ax.set_ylim(-10*dy1,(yn1+10)*dy1)

# %%
