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
    ds_ = ds.copy()
    lalons = [
        co.LAT_00, co.LAT_11, co.LAT_01, co.LAT_10,
        co.LON_00, co.LON_11, co.LON_01, co.LON_10,
    ]
    var2keep = [
        *lalons,
        'rm', 'rM'
    ]

    lam = (ds_[co.LAT_00] + ds_[co.LAT_01])/2
    laM = (ds_[co.LAT_10] + ds_[co.LAT_11])/2
    lom = (ds_[co.LON_00] + ds_[co.LON_01])/2
    loM = (ds_[co.LON_10] + ds_[co.LON_11])/2

    rm = ((lam-co.CHC_LAT)**2+(lom - co.CHC_LON)**2)**(1/2)
    rM = ((laM-co.CHC_LAT)**2+(loM - co.CHC_LON)**2)**(1/2)
    ds_['rm'] = rm
    ds_['rM'] = rM
    ds_ = ds_.set_coords(['rm','rM'])
    # for var in var2keep:
    #     ds_[var] = ds_[var][{co.ZM:0}]

    # %%
    ds1 = ds_.sum(co.RL)
    # %%
    df18 = get_pol_df(ds1, N18, var2keep,threshold=.85)
    # %%
    df6 = get_pol_df(ds1, N6, var2keep,threshold=.95)
    # %%

    kml:simplekml.kml.Kml =  simplekml.Kml()
    for i,(l,r) in enumerate(df6.iterrows()):
        make_pol(kml,r,ucp.cb[i])
    kml.save(pjoin(co.tmp_data_path,'pol6.kml'))

    kml:simplekml.kml.Kml =  simplekml.Kml()
    for i,(l,r) in enumerate(df18.iterrows()):
        make_pol(kml,r,ucp.cb[i])
    kml.save(pjoin(co.tmp_data_path,'pol18.kml'))



    # %%
    s  = splot(6,3,subplot_kw={'projection':crt.crs.PlateCarree()},
               figsize=(20,20),dpi=200)
    i = 0
    for l,r in df6.iterrows():
        ax=s.axf[i]
        xm,ym,xM,yM = r['pol'].bounds
        xm = min(co.CHC_LON,xm)
        xM = max(co.CHC_LON,xM)
        ym = min(co.CHC_LAT,ym)
        yM = max(co.CHC_LAT,yM)
        ax = fa.get_ax_bolivia(lola_extent=[xm,xM,ym,yM],ax=ax)
        ax.plot(r['x'],r['y'])
        ax.scatter(co.CHC_LON,co.CHC_LAT)
        ax.set_title(l)
        i += 1
    s.f.show()





if __name__ == '__main__':
    main()
