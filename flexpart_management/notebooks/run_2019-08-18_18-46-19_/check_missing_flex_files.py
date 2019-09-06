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
from useful_scit.imps import *


# %%
from useful_scit.imps import *
import flexpart_management.modules.FlexLogPol as FLP
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa

plt.style.use('ggplot')

from IPython.display import set_matplotlib_formats
set_matplotlib_formats('png')

# %%
path = '/Volumes/mbProD/Downloads/flx_log_coor/run_2019-08-18_18-46-19_'
# flp = FLP.FlexLogPol(path,concat=True)
# self = FLP.FlexLogPol(path,concat=False)

self = FLP.FlexLogPol(
    path,
#     concat=True,
    concat=False,
    get_clusters=False,
    open_merged=True,
    clusters_avail=False
)

# %%
ds = self.merged_ds

# %%
ds

# %%
_c = fa.get_dims_complement(ds,[co.RL])
ds_sum = ds.sum(_c)

_ds = ds_sum[co.CONC]

_ds = _ds.resample(**{co.RL:'1H'}).mean()

_n = _ds.isnull().to_dataframe()[co.CONC]

_vc = _n.value_counts()/_n.count() * 100

import pprint
_p = pprint.pformat(_vc,compact=True)

ax = _vc.plot.bar()
ax.set_title('[%] missing dates\n' + _p)
ax.grid(True)
# ax.figure

# %%

# %%
_pd = _ds.to_pandas()
ax = _pd.plot(
#     kind='',
    figsize=(10,5),
    linewidth=0,
    marker='.'
)

# %%
ax = sns.distplot(_pd.dropna(),hist_kws=dict(cumulative=True),kde=False,norm_hist=True)

# %%
pd1 = _pd[_pd<5e4]

# %%
ind = pd1.index

# %%
pd2 = pd1.resample('D').count()
ax = pd2.plot(marker='o',linewidth=0)
txt = ax.set_title('days with most FLEXPART fails')

# %%
pd3 = pd2[pd2>0]

# %%
pd3.sort_values(ascending=False)

# %%
l = np.linspace(0,10,11)

# %%
l

# %%
l[None:None:None]

# %%
sns.choose_colorbrewer_palette('q')

# %%
sns.color_palette("Set2",3,as_cmap=True)

# %%
cmap = plt.cm.get_cmap('Set1',3)

# %%
# %connect_info

# %%
from IPython import get_ipython
ipython = get_ipython()

# %%
ipython.magic('load_ext autoreload')

# %%
