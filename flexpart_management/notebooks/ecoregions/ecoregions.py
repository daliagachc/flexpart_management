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
import flexpart_management.notebooks.ecoregions.ecoregions_lfc as lfc
from flexpart_management.notebooks.ecoregions.ecoregions_lfc import *
import geopandas


# %%
def main():
    # %%

    ecoregions_trimmed = lfc.get_ecoregions_gdf()

    # %%

    df18 = pd.read_pickle(pjoin(co.tmp_data_path, 'pol18.pickle'))

    gdf18 = geopandas.GeoDataFrame(df18, geometry=df18['pol'])
    gdf18 = add_centroids_and_range(gdf18)
    gdf18 = lfc.add_hatch(gdf18)
    gdf18

    # %%

    iho = get_iho_gdf()
    meow = get_meow_gdf()

    all_meow = get_all_meow(meow)
    all_eco = get_all_eco(ecoregions_trimmed)
    pacific_ocean_pol = get_pacific_ocean_pol(iho, all_meow)
    lake_pol = get_lake_pol(all_eco)
    all_18_pol = get_all_18_pol(gdf18)

    mer_gdf = get_mer_gdf(meow, all_eco)
    mer_gdf['geometry'] = mer_gdf['geometry'] - lake_pol
    ter_gdf = get_ecoregion_gdf(ecoregions_trimmed)
    ext_gdf = get_extra_gdf(lake_pol, pacific_ocean_pol)

    combined_gdf = get_combined_gdf(ext_gdf, mer_gdf, ter_gdf)

    # %%
    la_lo_ext_big = 15
    la_lo_ext_small = 2.2
    extent = lfc.get_extent(la_lo_ext_big, la_lo_ext_big)
    rec = get_rec_pol(extent)

    cropped_combined_gdf = crop_combined_gdf(combined_gdf, rec)

    cropped_combined_gdf = add_parameter_to_combined_gdf(
        all_18_pol,
        cropped_combined_gdf
    )
    # %%

    s = lfc.plot_double_ecoregions_map(
        extent, cropped_combined_gdf, la_lo_ext_small)
    s.f.tight_layout()
    # s.f.subplots_adjust(left=.5)
    s.f.savefig(pjoin(co.paper_fig_path,
                      'ecoregions_map.pdf'))
    s.f.show()

    # %%
    s = lfc.plot_table_ecoregions(
        gdf18, cropped_combined_gdf,
        figsize=(7.25,5.6),
        min_per=5
    )
    s.f.tight_layout()
    # s.f.subplots_adjust(left=.5)
    s.f.show()
    s.f.savefig(pjoin(co.paper_fig_path, 'table_ecoregions.pdf'))

    # %%
    topoline = lfc.get_topoline(zline=3900)

    # %%

    # %%

    fl = lfc.FigLayout(cropped_combined_gdf,
                       topoline=topoline,
                       gdf18=gdf18)
    fl.f.savefig(pjoin(co.paper_fig_path, 'combined_cl18_eco_map.pdf'))
    # fl.f.tight_layout()
    plt.show()

    # %%
    s = splot(figsize=(7.25, 1.5))
    ax = s.ax
    import pandas.plotting as plotting
    plot_label_ecoregion(ax, cropped_combined_gdf)
    plt.show()

    # %%

    s = splot()
    ax = s.ax
    plot_pols(ax, gdf18)
    plt.show()

    # %%

    pass





