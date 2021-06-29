import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import cartopy.io.shapereader as shpreader

import pandas as pd


def plot_states(df, projection, colors, annotation, title, edgecolor):
    ax = plt.axes([0, 0, 1, 1],
                  projection=projection)
    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(False)
    ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

    shapename = 'admin_1_states_provinces_lakes_shp'
    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural', name=shapename)

    reader = shpreader.Reader(shpfilename)
    states = reader.records()
    values = list(df[title].unique())

    for state in states:
        attribute = 'name'
        name = state.attributes[attribute]

        # get classification
        try:
            classification = df.loc[state.attributes[attribute]][title]
        except:
            pass

        ax.add_geometries(state.geometry, ccrs.PlateCarree(),
                          facecolor=(colors[values.index(classification)]),
                          label=state.attributes[attribute],
                          edgecolor='#FFFFFF',
                          linewidth=.25)

    # legend
    import matplotlib.patches as mpatches
    handles = []
    for i in range(len(values)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i]))
        plt.legend(handles, values,
                   loc='lower left', bbox_to_anchor=(0.025, -0.0),
                   fancybox=True, frameon=False, fontsize=5)

    # annotate
    ax.annotate(annotation, xy=(0, 0), xycoords='figure fraction',
                xytext=(0.0275, -0.025), textcoords='axes fraction',
                horizontalalignment='left', verticalalignment='center', fontsize=4,
                )

    plt.title(title, fontsize=8)

    title = title + '.png'
    plt.savefig(title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))


def main():
    # Create a Stamen terrain background instance.
    stamen_terrain = cimgt.Stamen('toner')

    fig = plt.figure()

    # Create a GeoAxes in the tile's projection.
    # ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    # ax = fig.add_subplot(1, 1, 1, projection=ccrs.AlbersEqualArea())
    ax = plt.axes(projection=stamen_terrain.crs)
    # Limit the extent of the map to a small longitude/latitude range.
    ax.set_extent([-125, -63, 50, 23], crs=ccrs.Geodetic())

    #####

    # Add the Stamen data at zoom level 8.
    ax.add_image(stamen_terrain, 6)
    # ax.stock_img()
    ax.coastlines(resolution='50m', color='black', linewidth=1)

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

    for i in range(len(pNames)):
        text = ax.text(pLx[i], pLy[i], pNames[i], verticalalignment='center', horizontalalignment='left',
                       transform=text_transform,
                       bbox=dict(facecolor='lightskyblue', alpha=0.5, boxstyle='round'))
        plt.savefig("map_{}.png".format(i), format="png", dpi=300)
        text.set_visible(False)


if __name__ == '__main__':
    main()
