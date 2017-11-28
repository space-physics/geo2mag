import logging
try:
    from matplotlib.pyplot import figure
    import cartopy.crs as ccrs
except (ImportError,RuntimeError) as e:
    logging.error(f'plotting disabled    {e}')
    figure = None

def _sitecol(l):
    if l.name == 'HST':
        c='red'
    elif l.name == 'PFISR':
        c='blue'
    else:
        c='black'

    return c


def plotgeomag(latlon):
    if figure is None or latlon.shape[0] < 2:
        return

    ax = figure().gca()
    for l in latlon:
        ax.scatter(l.loc['mlon'], l.loc['mlat'],
                   s=180, facecolors='none', edgecolors=_sitecol(l))

    ax.set_xlabel('magnetic longitude [deg.]')
    ax.set_ylabel('magnetic latitude [deg.]')
    ax.grid(True)
    ax.set_title('Geomagnetic')
    for l in latlon:
        ax.text(l.loc['mlon'],l.loc['mlat'], l.site.item(),
                ha='center',va='center',fontsize=8)

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
# %% geographic
    ax = figure().gca(projection=ccrs.PlateCarree())
    ax.stock_img()

    for l in latlon:
        ax.scatter(l.loc['glon'], l.loc['glat'],
                   s=180, facecolors='none', edgecolors=_sitecol(l),
                   transform=ccrs.Geodetic())

    ax.set_extent((latlon.loc[:,'glon'].min(), latlon.loc[:,'glon'].max(),
                   latlon.loc[:,'glat'].min(), latlon.loc[:,'glat'].max()))
