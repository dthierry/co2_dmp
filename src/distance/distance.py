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
    d_cI = {}
    d_cII = {}
    d_cIII = {}
    # Phase I.
    for j in range(df_1.shape[0]):
        c_1 = (df_1.loc[j, "Latitude"], df_1.loc[j, "Longitude"])
        for k in coords.keys():
            c_2 = coords[k]
            d_cI[df_1.loc[j, "id"], k] = distance_x_y(c_1, c_2) * 0.6213712  #: from km to mi
    # Phase II.
    for j in range(df_2.shape[0]):
        c_1 = (df_2.loc[j, "Latitude"], df_2.loc[j, "Longitude"])
        for k in coords.keys():
            c_2 = coords[k]
            d_cII[df_2.loc[j, "id"], k] = distance_x_y(c_1, c_2) * 0.6213712  #: from km to mi
    # Phase III.
    for j in range(df_3.shape[0]):
        c_1 = (df_3.loc[j, "Latitude"], df_3.loc[j, "Longitude"])
        for k in coords.keys():
            c_2 = coords[k]
            d_cIII[df_3.loc[j, "id"], k] = distance_x_y(c_1, c_2) * 0.6213712  #: from km to mi

    # Just 2030
    # All NGCC.
    d_2030I = {}
    d_2030II = {}
    d_2030III = {}
    # Phase I.
    for j in range(df_1.shape[0]):
        c_1 = (df_1.loc[j, "Latitude"], df_1.loc[j, "Longitude"])
        for k in coords_2030.keys():
            c_2 = coords_2030[k]
            d_2030I[df_1.loc[j, "id"], k] = distance_x_y(c_1, c_2) * 0.6213712  #: from km to mi
    # Phase II.
    for j in range(df_2.shape[0]):
        c_1 = (df_2.loc[j, "Latitude"], df_2.loc[j, "Longitude"])
        for k in coords_2030.keys():
            c_2 = coords_2030[k]
            d_2030II[df_2.loc[j, "id"], k] = distance_x_y(c_1, c_2) * 0.6213712  #: from km to mi
    # Phase III.
    for j in range(df_3.shape[0]):
        c_1 = (df_3.loc[j, "Latitude"], df_3.loc[j, "Longitude"])
        for k in coords_2030.keys():
            c_2 = coords_2030[k]
            d_2030III[df_3.loc[j, "id"], k] = distance_x_y(c_1, c_2) * 0.6213712  #: from km to mi

    sorted_2030I = sorted(d_cI, key=d_cI.__getitem__)
    sorted_2030II = sorted(d_cII, key=d_cII.__getitem__)
    sorted_2030III = sorted(d_cIII, key=d_cIII.__getitem__)
    df_2030.index = df_2030["Plant Code"]  #
    df_ngcc.index = df_ngcc["Plant Code"]  #

    pname = [df_p.loc[i[1], "Plant Name"] for i in sorted_2030I]
    pyear = [df_ngcc.loc[i[1], "Planned Retirement Year"] for i in sorted_2030I]
    # print(pname)
    # print(pyear)
    i2030_df = pd.DataFrame({"pairs": sorted_2030I,
                             "distance": [d_2030I[i] for i in sorted_2030I],
                             "name": pname,
                             "year": pyear})

    i2030_df.to_csv("./res/i2030.csv")

    pname = [df_p.loc[i[1], "Plant Name"] for i in sorted_2030II]
    pyear = [df_ngcc.loc[i[1], "Planned Retirement Year"] for i in sorted_2030II]
    # print(pname)
    # print(pyear)
    ii2030_df = pd.DataFrame({"pairs": sorted_2030II,
                             "distance": [d_2030II[i] for i in sorted_2030II],
                             "name": pname,
                             "year": pyear})

    ii2030_df.to_csv("./res/ii2030.csv")

    pname = [df_p.loc[i[1], "Plant Name"] for i in sorted_2030III]
    pyear = [df_ngcc.loc[i[1], "Planned Retirement Year"] for i in sorted_2030III]
    iii2030_df = pd.DataFrame({"pairs": sorted_2030III,
                             "distance": [d_2030III[i] for i in sorted_2030III],
                             "name": pname,
                             "year": pyear})

    iii2030_df.to_csv("./res/iii2030.csv")

def distance_x_y(coord_x, coord_y):
    p = np.pi/180.
    r = 6371.
    a = 0.5 - np.cos((coord_x[0] - coord_y[0]) * p) / 2. \
        + np.cos(coord_x[0] * p) * np.cos(coord_y[0] * p) * (1 - np.cos((coord_x[1] - coord_y[1]) * p)) / 2.
    return 2 * r * np.arcsin(np.sqrt(a))


if __name__ == "__main__":
    main()
