# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
# %%

import flexpart_management.modules.flx_array as fa
import flexpart_management.modules.constants as co
from useful_scit.imps import *

# %%
dsn = xr.open_mfdataset(pjoin(co.tmp_data_path, 'new_log_pol_ds_agl.nc'),
                        combine='nested', concat_dim=co.RL)
# %%
d1 = dsn.sum([co.R_CENTER,co.TH_CENTER]).reset_coords()['CONC']
d2 = d1.to_dataframe()
# %%
d3:pd.DataFrame= d2.reset_index().set_index([co.RL,co.ZM]).unstack()
# %%
d4= d3['CONC'].corr()
# %%
cm = plt.get_cmap('RdBu_r',8)
sns.heatmap(d4,cmap=cm,vmin=-1,vmax=1)
plt.tight_layout()
plt.show()
# %%

import numpy as np


def squiggle_xy(a, b, c, d, i=np.arange(0.0, 2*np.pi, 0.05)):
    return np.sin(i*a)*np.cos(i*b), np.sin(i*c)*np.cos(i*d)


fig11 = plt.figure(figsize=(16, 16), constrained_layout=False)
outer_grid = fig11.add_gridspec(2, 3,
                                # wspace=0, hspace=0,
                                height_ratios = [1,2]
                                )

for a in range(2):
    for b in range(3):
        # gridspec inside gridspec
        inner_grid = outer_grid[a, b].subgridspec(3, 3,
                                                  # wspace=0, hspace=0
                                                  )
        axs = inner_grid.subplots(sharex=True,sharey=True)  # Create all subplots for the inner grid.
        for (c, d), ax in np.ndenumerate(axs):
            ax.plot(*squiggle_xy(a + 1, b + 1, c + 1, d + 1))
            # ax.set(xticks=[], yticks=[])

# show only the outside spines
for ax in fig11.get_axes():
    # ax.spines['top'].set_visible(ax.is_first_row())
    # ax.spines['bottom'].set_visible(ax.is_last_row())
    # ax.spines['left'].set_visible(ax.is_first_col())
    # ax.spines['right'].set_visible(ax.is_last_col())
    pass

fig11.tight_layout()

plt.show()