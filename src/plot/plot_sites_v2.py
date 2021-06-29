import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import cartopy.io.shapereader as shpreader

import pandas as pd
import numpy as np


def main():
    df_1 = pd.read_csv("../resources/phaseI.csv")
    df_2 = pd.read_csv("../resources/phaseII.csv")
    df_3 = pd.read_csv("../resources/phaseIII.csv")

    df_g = pd.read_csv("../resources/3_1_Generator_Y2020_Early_Release.csv")
    df_g.astype({"Plant Code": np.int64})
    # Just the NGCCs.
    df_ngcc = df_g[df_g["Technology"] == "Natural Gas Fired Combined Cycle"]
    df_ngcc["PRYNaN"] = df_ngcc["Planned Retirement Year"].fillna(value=2100)
    df_ngcc["PRY"] = df_ngcc["PRYNaN"].apply(lambda x: 2100 if x == " " else int(x))
    # df_ngcc.index = df_ngcc["Plant Code"]  # The indices are repeated.

    # Get the 2030 plants.
    df_2030 = df_ngcc[df_ngcc["PRY"] < 2030]

    # Get the Plant location information.
    df_p = pd.read_csv("../resources/2___Plant_Y2020_Early_Release.csv")
    df_p = df_p.astype({"Plant Code": np.int64})
    df_p.index = df_p["Plant Code"]

    print(df_ngcc.shape[0])
    print(df_2030.shape[0])

    coords = {}
    coords_2030 = {}
    for i in range(df_ngcc.shape[0]):
        pc = df_ngcc.iloc[i]["Plant Code"]
        coords[pc] = (float(df_p.loc[pc, "Latitude"]), float(df_p.loc[pc, "Longitude"]))

    for i in range(df_2030.shape[0]):
        pc = df_2030.iloc[i]["Plant Code"]
        coords_2030[pc] = (float(df_p.loc[pc, "Latitude"]), float(df_p.loc[pc, "Longitude"]))

    print(coords)
    print(coords_2030)

    # All NGCC.
    cI = []
    cII = []
    cIII = []
    # Phase I.
    for j in range(df_1.shape[0]):
        cI.append((df_1.loc[j, "Latitude"], df_1.loc[j, "Longitude"]))

    # Phase II.
    for j in range(df_2.shape[0]):
        cII.append((df_2.loc[j, "Latitude"], df_2.loc[j, "Longitude"]))

    # Phase III.
    for j in range(df_3.shape[0]):
        cIII.append((df_3.loc[j, "Latitude"], df_3.loc[j, "Longitude"]))

    fig = plt.figure()


    projection = ccrs.LambertConformal()
    ax = fig.add_subplot(1, 1, 1, projection=projection, frameon=False)
    ax.patch.set_visible(True)

    # Limit the extent of the map to a small longitude/latitude range.
    ax.set_extent([-125, -66.5, 20, 50], crs=ccrs.Geodetic())


    # No coastlines.

    #####
    # # Plant Barry Site
    # ax.plot(-88.00, 31.00, marker='o', color='red', markersize=2,
    #         alpha=0.7, transform=ccrs.Geodetic())
    # # Cranfield Site
    # ax.plot(-91.207573, 31.5331, marker='o', color='red', markersize=2,
    #         alpha=0.7, transform=ccrs.Geodetic())
    # # Illinois, Decatur
    # ax.plot(-88.944288, 39.789432, marker='o', color='red', markersize=2,
    #         alpha=0.7, transform=ccrs.Geodetic())
    # # Michigan Basin Site
    # ax.plot(-84.552955, 44.980179, marker='o', color='red', markersize=2,
    #         alpha=0.7, transform=ccrs.Geodetic())
    #
    # # Bell Creek Site
    # ax.plot(-105.093683, 45.112795, marker='o', color='red', markersize=2,
    #         alpha=0.7, transform=ccrs.Geodetic())
    #
    # # Kevin Dome Site
    # ax.plot(-111.969740, 48.746531, marker='o', color='red', markersize=2,
    #         alpha=0.7, transform=ccrs.Geodetic())

    # Site locations
    plIx = [i[1] for i in cI]
    plIy = [i[0] for i in cI]
    plIIx = [i[1] for i in cII]
    plIIy = [i[0] for i in cII]
    plIIIx = [i[1] for i in cIII]
    plIIIy = [i[0] for i in cIII]
    # Points in The Map
    ax.plot(plIx, plIy, marker="o", markersize=2, color="red", transform=ccrs.Geodetic(), linestyle='None',
            label="phaseI")
    ax.plot(plIIx, plIIy, marker="o", markersize=2, color="peru", transform=ccrs.Geodetic(), linestyle='None',
            label="phaseII")
    ax.plot(plIIIx, plIIIy, marker="o", markersize=2, color="magenta", transform=ccrs.Geodetic(), linestyle='None',
            label="phaseIII")
    # Plant locations
    pLx = [i[1] for i in coords.values()]

    pLy = [i[0] for i in coords.values()]

    ax.plot(pLx, pLy, marker="x", markersize=5, transform=ccrs.Geodetic(), linestyle='None', label="NGCC")
    ax.legend()
    ax.set_title('US NGCC and CO2 storage sites')
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
    plt.savefig("map_{}.png".format(i), format="png", dpi=300)

def distance_x_y(coord_x, coord_y):
    p = np.pi/180.
    r = 6371.
    a = 0.5 - np.cos((coord_x[0] - coord_y[0]) * p) / 2. \
        + np.cos(coord_x[0] * p) * np.cos(coord_y[0] * p) * (1 - np.cos((coord_x[1] - coord_y[1]) * p)) / 2.
    return 2 * r * np.arcsin(np.sqrt(a))


if __name__ == '__main__':
    main()
