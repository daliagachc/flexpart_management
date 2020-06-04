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
    ds1, var2keep = get_ds_and_vars_to_keep()
    # %%

    centroid_18_df = lfc.get_centroid_df(ds1, 'lab_nc18')
    centroid_18_df.to_csv(pjoin(co.tmp_data_path, 'centroid_18_v3.csv'))
    centroid_6_df = lfc.get_centroid_df(ds1, 'lab_nc06')
    centroid_6_df.to_csv(pjoin(co.tmp_data_path, 'centroid_6_v3.csv'))


    # %%
    df18 = get_pol_df(ds1, N18, var2keep, threshold=.85)
    # %%
    df18.to_pickle(pjoin(co.tmp_data_path, 'pol18.pickle'))
    # %%
    df6 = get_pol_df(ds1, N6, var2keep, threshold=.95)
    df6.to_pickle(pjoin(co.tmp_data_path, 'pol6.pickle'))
    # %%

    kml: simplekml.kml.Kml = simplekml.Kml()
    for i, (l, r) in enumerate(df6.iterrows()):
        make_pol(kml, r, ucp.cb[i])
    kml.save(pjoin(co.tmp_data_path, 'pol6.kml'))

    kml: simplekml.kml.Kml = simplekml.Kml()
    for i, (l, r) in enumerate(df18.iterrows()):
        make_pol(kml, r, ucp.cb[i])
    kml.save(pjoin(co.tmp_data_path, 'pol18.kml'))

    # %%
    s = splot(6, 3, subplot_kw={'projection': crt.crs.PlateCarree()},
              figsize=(20, 20), dpi=200)
    i = 0
    for l, r in df6.iterrows():
        ax = s.axf[i]
        xm, ym, xM, yM = r['pol'].bounds
        xm = min(co.CHC_LON, xm)
        xM = max(co.CHC_LON, xM)
        ym = min(co.CHC_LAT, ym)
        yM = max(co.CHC_LAT, yM)
        ax = fa.get_ax_bolivia(lola_extent=[xm, xM, ym, yM], ax=ax)
        ax.plot(r['x'], r['y'])
        ax.scatter(co.CHC_LON, co.CHC_LAT)
        ax.set_title(l)
        i += 1
    s.f.show()


# %%

# %%

if __name__ == '__main__':
    main()
