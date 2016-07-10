from matplotlib.pyplot import figure

def plotgeomag(lla):
    ax = figure().gca()
    for n,l in lla.iterrows():
        if isinstance(n,str):
            if n[:3] == 'HST':
                c='red'
            elif n == 'PFISR':
                c='blue'
            else:
                c='black'
        else:
            c=None

        ax.scatter(l['mlon'],l['mlat'],s=180,facecolors='none',edgecolors=c)

    ax.set_xlabel('magnetic longitude [deg.]')
    ax.set_ylabel('magnetic latitude [deg.]')
    ax.grid(True)
    ax.set_title('Sites vs. GeoMagnetic coordinates')
    for lon,lat,n in zip(lla['mlon'],lla['mlat'],lla.index):
        try:
            ax.text(lon,lat,n,ha='center',va='center',fontsize=8)
        except ValueError:
            pass

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
#%%
    ax = figure().gca()
    for n,l in lla.iterrows():
        if isinstance(n,str):
            if n[:3] == 'HST':
                c='red'
            elif n == 'PFISR':
                c='blue'
            else:
                c='black'
        else:
            c=None

        ax.scatter(l['glon'],l['glat'],s=180,facecolors='none',edgecolors=c)

    ax.set_xlabel('geodetic longitude [deg.]')
    ax.set_ylabel('geodetic latitude [deg.]')
    ax.grid(True)
    ax.set_title('Sites vs. Geodetic coordinates')
    for lon,lat,n in zip(lla['glon'],lla['glat'],lla.index):
        try:
            ax.text(lon,lat,n,ha='center',va='center',fontsize=8)
        except ValueError:
            pass

    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
