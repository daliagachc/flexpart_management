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
import flexpart_management.notebooks.ecoregions.ecoregions_hatched_lfc as lfc
from flexpart_management.notebooks.ecoregions.ecoregions_hatched_lfc import *
import geopandas


# %%
def main():
    # %%

    ecoregions_trimmed = lfc.get_ecoregions_gdf()
    # %%
    ecoregions_trimmed = ecoregions_trimmed.dissolve('BIOME_NAME').reset_index()

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
    ter_gdf = get_ecoregion_gdf_biome(ecoregions_trimmed)
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
    pars = cropped_combined_gdf[['concur_area','parent']].groupby('parent').sum().sort_values('concur_area',ascending=False)
    pars['hatch'] = ''
    p_dic = pars['hatch'].to_dict()
    p_dic['Tropical & Subtropical Dry Broadleaf Forests']='....'
    p_dic['Flooded Grasslands & Savannas']='\\\\\\\\'
    # %%

    # from itertools import cycle
    # from matplotlib.colors import colorConverter
    # from colorharmonies import Color, complementaryColor
    # s = splot(dpi=300)
    # _lc = len(cropped_combined_gdf)
    # # for i in range(len(cropped_combined_gdf)):
    # for i in range(_lc):
    #         pol = cropped_combined_gdf.iloc[[i]]
    #         j = p_dic[pol['parent'].item()]
    #         print(j)
    #         _co = pol['color'].item()
    #         _c = colorConverter.to_rgb(_co)
    #         # _c = (np.array(_c) * 255).astype(int)
    #         # _c = complementaryColor(Color(_c,'',''))
    #         # _c = np.array(_c)/255.
    #         _c = np.array(_c).mean()
    #         _i = .5
    #         if _c > .5:
    #             _c = _c - _i
    #         else:
    #             _c = _c + _i
    #
    #         pol.plot(
    #             ax=s.ax,
    #             hatch=j*1,
    #             # hatch.color='b',
    #             edgecolor=colorConverter.to_rgba(
    #                 [_c,_c,_c],alpha=.2),
    #             color=_co,
    #             linewidth=0
    #         )
    # s.f.show()

    # %%


    s = lfc.plot_double_ecoregions_map(
        extent, cropped_combined_gdf, la_lo_ext_small)
    s.f.tight_layout()
    # s.f.subplots_adjust(left=.5)
    s.f.savefig(pjoin(co.paper_fig_path,
                      'ecoregions_map.pdf'))
    s.f.savefig(pjoin(co.paper_fig_path,
                      'ecoregions_map.svg'))
    s.f.show()

    # %%
    s = lfc.plot_table_ecoregions(
        gdf18, cropped_combined_gdf,
        figsize=(7.25,3),
        min_per=1,
        tw=40
    )
    s.f.tight_layout()
    # s.f.subplots_adjust(left=.5)
    s.f.show()
    s.f.savefig(pjoin(co.paper_fig_path, 'table_ecoregions_ll.pdf'))

    # %%
    topoline = lfc.get_topoline(zline=3900)

    # %%

    # %%

    fl = lfc.FigLayout(cropped_combined_gdf,
                       topoline=topoline,
                       gdf18=gdf18)
    fl.f.savefig(pjoin(co.paper_fig_path, 'combined_cl18_eco_map_source.pdf'))
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





