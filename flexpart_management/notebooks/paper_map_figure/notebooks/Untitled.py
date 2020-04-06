# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: ''
#     name: ''
# ---
# %%
from useful_scit.imps import *

from notebooks.map_figure import map_figure
from wrf_flexpart_figures import constants as co
import cartopy.crs as ccrs
from cartopy.io.srtm import SRTM3Source
from wrf_flexpart_figures import util


# %%


def main():
    # %%

    # %%
    util.login_nasa()
    # %%

    source = SRTM3Source

    plt.figure()
    import cartopy.mpl.geoaxes
    ax: cartopy.mpl.geoaxes.GeoAxes = plt.axes(projection=ccrs.PlateCarree())
    ax.add_raster(source(max_nx=100, max_ny=100))
    range = 10
    ax.set_extent([
        co.CHC_LON - range, co.CHC_LON + range,
        co.CHC_LAT - range, co.CHC_LAT + range,
    ]
    )
    ax.gridlines(draw_labels=True)
    # ax.set_extent([14, 15, -10, 10])
    plt.show()
    plt.clf()

    # %%
    """
    This example illustrates the automatic download of STRM data, and adding of
    shading to create a so-called "Shaded Relief SRTM".

    Originally contributed by Thomas Lecocq (http://geophysique.be).

    """
    from cartopy.io import srtm

    from cartopy.io import PostprocessedRasterSource, LocatedImage

    def shade(located_elevations):
        """
        Given an array of elevations in a LocatedImage, add a relief (shadows) to
        give a realistic 3d appearance.

        """
        new_img = srtm.add_shading(located_elevations.image,
                                   azimuth=135, altitude=15)
        return LocatedImage(new_img, located_elevations.extent)

    def plot(Source, name):
        plt.figure()
        ax = plt.axes(projection=ccrs.PlateCarree())

        # Define a raster source which uses the SRTM data and applies the
        # shade function when the data is retrieved.
        shaded_srtm = PostprocessedRasterSource(Source(), shade)

        # Add the shaded SRTM source to our map with a grayscale colormap.
        ax.add_raster(shaded_srtm, cmap='Greys')

        # This data is high resolution, so pick a small area which has some
        # interesting orography.
        ax.set_extent([12, 13, 47, 48])

        plt.title(name + " Shaded Relief Map")

        gl = ax.gridlines(draw_labels=True)
        gl.xlabels_top = False
        gl.ylabels_left = False

    # %%
    map_figure()

    # %%

    # %%

    # %%

    # %%

# %%

# %%
# %%

# %%
