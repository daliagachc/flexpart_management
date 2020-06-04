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
from flexpart_management.notebooks.paper_silhouette.paper_silhouette_lfc import *
# %%
path = '/Users/diego/flexpart_management/flexpart_management/tmp_data/silhouette_scores.pickle'
df = pd.read_pickle(path)
# %%
ss = 'ss'
wss = 'wss'
# plt.Axes.barh()
ser:pd.Series = df[ss]
width = 3.54
height = width/1.6
f, ax = plt.subplots(figsize=(width,height), dpi=300)
ax:plt.Axes
ser.plot(ax=ax, linewidth=.5, marker='.', color='k',
         linestyle=':', markersize=5
         )
ax.set_xlim(1,25)
ax.set_ylim(0.15,0.30)
ax.set_xticks([6,12,18,24])
sns.despine(ax=ax)
ax.set_ylabel('Silhouette average score')
ax.set_xlabel('number of clusters')
# ax.axvline(x=18,ymax=.2)
ax.vlines(
    x=18,ymin=0,ymax=ser[18],
    color=ucp.cc[0],
    linewidth=1.5, linestyles='-'
)

ax.vlines(
    x=6,ymin=0,ymax=ser[6],
    color=ucp.cc[0],
    linewidth=1.5, linestyles='-'
)

ax.scatter(x=18,y=ser[18], color=ucp.cc[0],zorder=20,
           s=7
           )

ax.scatter(x=6,y=ser[6], color=ucp.cc[0],zorder=20,
           s=7
           )


f.tight_layout()
f.savefig(pjoin(co.paper_fig_path,'sil_score_3_54.pdf'))
plt.show()
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%


