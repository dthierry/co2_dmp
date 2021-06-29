import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import cartopy.io.shapereader as shpreader

import pandas as pd


def main():


    fig = plt.figure()


    projection = ccrs.LambertConformal()
    ax = fig.add_subplot(1, 1, 1, projection=projection, frameon=False)
    ax.patch.set_visible(False)

    # Limit the extent of the map to a small longitude/latitude range.
    ax.set_extent([-125, -66.5, 20, 50], crs=ccrs.Geodetic())
    # No coastlines.

    #####
    # Plant Barry Site
    ax.plot(-88.00, 31.00, marker='o', color='red', markersize=2,
            alpha=0.7, transform=ccrs.Geodetic())
    # Cranfield Site
    ax.plot(-91.207573, 31.5331, marker='o', color='red', markersize=2,
            alpha=0.7, transform=ccrs.Geodetic())
    # Illinois, Decatur
    ax.plot(-88.944288, 39.789432, marker='o', color='red', markersize=2,
            alpha=0.7, transform=ccrs.Geodetic())
    # Michigan Basin Site
    ax.plot(-84.552955, 44.980179, marker='o', color='red', markersize=2,
            alpha=0.7, transform=ccrs.Geodetic())

    # Bell Creek Site
    ax.plot(-105.093683, 45.112795, marker='o', color='red', markersize=2,
            alpha=0.7, transform=ccrs.Geodetic())

    # Kevin Dome Site
    ax.plot(-111.969740, 48.746531, marker='o', color='red', markersize=2,
            alpha=0.7, transform=ccrs.Geodetic())

    # Plant locations
    pLx = [-118.1256,
           -114.994167,
           -117.893056,
           -117.170369,
           -82.3208,
           -114.920686,
           -114.8783,
           -106.431777,
           -71.406856,
           -93.771389,
           -94.3472,
           -95.5306]

    pLy = [
        34.138467,
        35.788889,
        33.861667,
        33.738839,
        29.6461,
        36.343229,
        36.2253,
        31.983587,
        41.861531,
        30.0444,
        41.1136,
        29.9417]

    pNames = [
        "CalTech/10.5MWh",
        "Desert Star/536MWh",
        "Fullerton Mill/21MWh",
        "Inland Empire Energy Center/819MWh",
        "John R Kelly/50MWh",
        "Nevada Cogen Assoc GarnetVly/94.8MWh",
        "Nevada Cogen Assoc Black Mountain/96.3MWh",
        "Newman/290MWh",
        "Pawtucket Power Assoc/41MWh",
        "Sabine Cogen/106MWh",
        "Summit Lake/22.5MWh",
        "T H Wharton/663.6"
    ]

    ax.plot(pLx, pLy, marker="x", markersize=5, transform=ccrs.Geodetic(), linestyle='None')

    geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
    text_transform = offset_copy(geodetic_transform, units='dots', x=+5, y=+5)

    # Get the shapes of the states
    shapename = 'admin_1_states_provinces_lakes'
    states_shp = shpreader.natural_earth(resolution='110m',
                                         category='cultural', name=shapename)
    # Put colour into the states.
    def colorize_state(geometry):
        facecolor = (0.90,1.00,0.95)
        return {'facecolor': facecolor, 'edgecolor': 'black'}
    # Add the state shapes.
    ax.add_geometries(
        shpreader.Reader(states_shp).geometries(),
        ccrs.PlateCarree(),
        styler=colorize_state)

    #for i in range(len(pNames)):
    #    text = ax.text(pLx[i], pLy[i], pNames[i], verticalalignment='center', horizontalalignment='left',
    #                   transform=text_transform,
    #                   bbox=dict(facecolor='lightskyblue', alpha=0.5, boxstyle='round'))
    #    plt.savefig("map_{}.png".format(i), format="png", dpi=300)
    #    text.set_visible(False)
    plt.show()


if __name__ == '__main__':
    main()
