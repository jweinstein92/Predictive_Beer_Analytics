import urllib
import json
from ConfigParser import SafeConfigParser
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

config = SafeConfigParser()
config.read('../apiConfig.ini')
# set the api setting values
baseUrl = "https://maps.googleapis.com/maps/api/geocode/json?"
apiKey = config.get('googleMaps', 'apiKey')
apiKey2 = config.get('googleMaps', 'apiKey2')

abvMapName = {'0': '0', '1': '.1-3.9', '2': '.1-3.9', '3': '.1-3.9',
                '4': '4.0-4.9', '5': '5.0-5.9', '6': '6.0-6.9', '7': '7.0-7.9',
                '8': '8.0-8.9', '9': '9.0-9.9', '10': '10.0-10.9', '11': '11+'}


def getLatLong(address, calls):
    # Google Geocoding api only allows 2500 api calls a day
    # Update code to handle number of users and api keys
    url = ''
    if calls < 2500:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey)
    elif calls > 5000:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey2)
    if (url != ''):
        data = urllib.urlopen(url).read()
        info = json.loads(data).get("results")
        if info:
            location = info[0].get("geometry").get("location")
        else:
            location = ""
        return location
    else:
        return "apiLimit"


def createMap(lats, lngs, parallels, meridians, states=False):
    # create polar stereographic Basemap instance.
    m = Basemap(projection='stere', lat_0=lats[0], lon_0=lngs[0],
            llcrnrlat=lats[1], urcrnrlat=lats[2],
            llcrnrlon=lngs[1], urcrnrlon=lngs[2],
            rsphere=6371200, resolution='l', area_thresh=10000)
    # draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines()
    m.drawcountries()
    if states:
        m.drawstates()

    # draw parallels.
    m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    # draw meridians
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

    return m


def drawUSMap(points, abv):
    print "Drawing US map with " + str(len(points)) + " data points."
    lats = []
    lngs = []
    ratings = []

    for point in points:
        lats.append(point.lat)
        lngs.append(point.lng)
        ratings.append(point.rating)

    # US middle, lower left, and upper right
    # latitude and longitude coordinates
    usLat = [38, 22, 48]
    usLng = [-97, -125, -59]
    parallels = [30, 40]
    meridians = [280, 270, 260, 250, 240]

    # create polar stereographic Basemap instance.
    m = createMap(usLat, usLng, parallels, meridians, True)

    # overlay the scatter points to see that the density
    # is working as expected
    plt.scatter(*m(lngs, lats), c=ratings)
    plt.colorbar()
    filename = '../graphics/USRating'
    if str(abv) in abvMapName:
        filename += abvMapName[str(abv)] + '.png'
    else:
        filename += abvMapName['11'] + '.png'
    plt.savefig(filename)


def drawEUMap(points, abv):
    print "Drawing EU map with " + str(len(points)) + " data points."
    lats = []
    lngs = []
    ratings = []

    for point in points:
        lats.append(point.lat)
        lngs.append(point.lng)
        ratings.append(point.rating)

    # EU middle, lower left, and upper right
    # latitude and longitude coordinates
    euLat = [51, 27, 71]
    euLng = [20, -16, 45]
    parallels = [30, 40, 50, 60, 70]
    meridians = [350, 0, 10, 20, 30, 40]

    # create polar stereographic Basemap instance.
    m = createMap(euLat, euLng, parallels, meridians)
    
    # overlay the scatter points to see that the density
    # is working as expected
    plt.scatter(*m(lngs, lats), c=ratings, alpha=.5)
    plt.colorbar()
    filename = '../graphics/EURating'
    if str(abv) in abvMapName:
        filename += abvMapName[str(abv)] + '.png'
    else:
        filename += abvMapName['11'] + '.png'
    plt.savefig(filename)


def inEU(lat, lng):
    return lat >= 27 and lat <= 71 and lng >= -16 and lng <= 45


def inUS(lat, lng):
    return lat >= 22 and lat <= 48 and lng >= -125 and lng <= -59


def abvMap(points, abv):
    # lat = []
    # lng = []
    # ratings = []
    # for point in points:
    #     lat.append(point.lat)
    #     lng.append(point.lng)
    #     ratings.append(point.rating)
    # plt.scatter(lng, lat, c=ratings)
    # plt.colorbar()
    # plt.savefig('ratings.png')
    euPoints = []
    usPoints = []

    for point in points:
        if inUS(point.lat, point.lng):
            usPoints.append(point)
        elif inEU(point.lat, point.lng):
            euPoints.append(point)
    drawEUMap(euPoints, abv)
    # drawUSMap(usPoints, abv)
