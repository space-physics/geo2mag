import logging
import pandas

try:
    from matplotlib.pyplot import figure
    import cartopy.crs as ccrs
except (ImportError, RuntimeError) as e:
    logging.error(f"plotting disabled    {e}")
    figure = None


def _sitecol(line: pandas.Series) -> str:
    if line.name == "HST":
        c = "red"
    elif line.name == "PFISR":
        c = "blue"
    else:
        c = "black"

    return c


def plotgeomag(latlon: pandas.DataFrame):
    if figure is None:
        return

    ax = figure().gca()
    for _, c in latlon.iterrows():
        ax.scatter(
            c.at["mlon"], c.at["mlat"], s=180, facecolors="none",
        )
        # edgecolors=_sitecol(l))

    ax.set_xlabel("magnetic longitude [deg.]")
    ax.set_ylabel("magnetic latitude [deg.]")
    ax.grid(True)
    ax.set_title("Geomagnetic")
    #    for _,c in latlon.iterrows():
    #        ax.text(c.at['mlon'], c.at['mlat'], c.site.item(),
    #                ha='center', va='center', fontsize=8)

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    # %% geographic
    if latlon.shape[0] < 2:
        return

    ax = figure().gca(projection=ccrs.PlateCarree())
    ax.stock_img()

    for _, c in latlon.iterrows():
        ax.scatter(
            c.at["glon"],
            c.at["glat"],
            s=180,
            facecolors="none",
            # edgecolors=_sitecol(l),
            transform=ccrs.Geodetic(),
        )

    ax.set_extent(
        (latlon.loc[:, "glon"].min(), latlon.loc[:, "glon"].max(), latlon.loc[:, "glat"].min(), latlon.loc[:, "glat"].max())
    )
