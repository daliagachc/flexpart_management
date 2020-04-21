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
    mega_ds = xr.open_dataset(pjoin(co.tmp_data_path,'cluster_series_v3.nc'))
    # %%
    # %%
    labs = co.DIC_186.sort_values(['sr', '18_NC'])['18_NC']
    s = splot(3, 6, sharex=True, sharey=False, figsize=(16, 8))
    for lab, ax in zip(labs, s.axf):
        tot = mega_ds[CL18].loc[{N18: lab, ZCOL: ALL, NORM: False}]
        sur = mega_ds[CL18].loc[{N18: lab, ZCOL: SURF, NORM: False}]
        rat = sur / tot
        ax.hist(rat.values, bins=np.arange(0, 1.01, .1), weights=tot.values)
        ax.set_title(lab)
    s.f.tight_layout()
    s.f.subplots_adjust(top=.9)
    s.f.suptitle(f'SRRsurf/SRRtot (weighted by SRRtot)', y=.97)

    s.f.show()

    # %%
    labs = co.DIC_186.sort_values(['sr', '18_NC'])['18_NC']
    s = splot(3, 6, sharex=True, sharey=False, figsize=(16, 8))
    for lab, ax in zip(labs, s.axf):
        tot = mega_ds[CL18].loc[{N18: lab, ZCOL: ALL, NORM: 0}]
        age = mega_ds[AG18].loc[{N18: lab, ZCOL: ALL}]
        rat = age
        bins = np.geomspace(1, 100, 10)
        ax.hist(rat.values, bins=bins, weights=tot.values)
        ax.set_title(lab)
        ax.set_xlim(1, 100)
        ax.set_xscale('log')
        # ax.set_xticks([0,12,24,36,48,60,72,84,96])
    s.f.tight_layout()
    s.f.subplots_adjust(top=.9)
    s.f.suptitle(f'AGE (weighted by SRRtot)', y=.97)

    s.f.show()
    # %%
    # %%
    labs = co.DIC_186.sort_values(['sr', '18_NC'])['18_NC']
    s = splot(3, 6, sharex=True, sharey=False, figsize=(16, 8))
    for lab, ax in zip(labs, s.axf):
        tot = mega_ds[CL18].loc[{N18: lab, ZCOL: ALL, NORM: False}]
        age = mega_ds[AG18].loc[{N18: lab, ZCOL: ALL}]
        rat = age
        bins = np.geomspace(1, 100, 10)
        ax.plot(age, c=ucp.cb[1])
        ax.set_title(lab)
        at = ax.twinx()
        at.plot(tot, c=ucp.cb[2])
        # ax.set_xlim(1,100)
        # ax.set_xscale('log')
        # ax.set_xticks([0,12,24,36,48,60,72,84,96])

    s.f.tight_layout()
    s.f.subplots_adjust(top=.9)
    s.f.suptitle(f'AGE (weighted by SRRtot)', y=.97)

    s.f.show()

    # %%
    labs = co.DIC_186.sort_values(['sr', '18_NC'])['18_NC']
    s = splot(3, 6, sharex=True, sharey=True, figsize=(16, 8))
    for lab, ax in zip(labs, s.axf):
        tot = mega_ds[CL18].loc[{N18: lab, ZCOL: ALL, NORM: True}]
        # sur = mega_ds[CL18].loc[{N18: lab, ZCOL: SURF, NORM: False}]
        # rat = sur / tot
        arange = [0, *np.geomspace(.01, 1.01, 10)]
        ax.hist(tot.values, bins=arange)
        ax.set_xlim([.006, 1])
        ax.set_xscale('log')
        ax.set_title(lab)
    s.f.tight_layout()
    s.f.subplots_adjust(top=.9)
    s.f.suptitle(f'normalized SRR', y=.97)

    s.f.show()

    # %%
    plt_diag(all_age, all_dis, all_ds, all_zsl, ang_clock_all)

    # %%
    _s = (ds[CO] * ds[co.ZM]).sum([co.RL, co.TH_CENTER, co.ZM]) / ds[CO].sum(
        [co.RL, co.TH_CENTER, co.ZM])
    _s.plot()
    plt.show()
    # %%

    df: pd.DataFrame = all_age_18.to_dataframe()
    df.dropna().reset_index(level=N18).hist(by=N18, sharex=True, sharey=True,
                                            figsize=(10, 10))
    plt.tight_layout()
    plt.show()

    # %%
    # %%
    all_ds[CALL].plot(hue=ZCOL)
    plt.show()
    # %%

    # %%
    # %%
    # %%

    # %%
    # %%
    big_ds.loc[{NORM: False}][CALL].plot(row=ZCOL, figsize=(20, 5), )
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
# %%
# %%
# %%
# %%
# %%
