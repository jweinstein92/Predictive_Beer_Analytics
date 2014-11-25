import urllib
import json
from ConfigParser import SafeConfigParser
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy

config = SafeConfigParser()
config.read('../apiConfig.ini')
# set the api setting values
baseUrl = "https://maps.googleapis.com/maps/api/geocode/json?"
apiKey = config.get('googleMaps', 'apiKey')
apiKey2 = config.get('googleMaps', 'apiKey2')
apiKey3 = config.get('googleMaps', 'apiKey3')
apiKey4 = config.get('googleMaps', 'apiKey4')

abvMapName = {'0': '0', '1': '.1-3.9', '2': '.1-3.9', '3': '.1-3.9',
                '4': '4.0-4.9', '5': '5.0-5.9', '6': '6.0-6.9', '7': '7.0-7.9',
                '8': '8.0-8.9', '9': '9.0-9.9', '10': '10.0-10.9', '11': '11+'}


def getLatLong(address, calls):
    # Google Geocoding api only allows 2500 api calls a day
    # Update code to handle number of users and api keys
    url = ''
    if calls < 2450:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey)
    elif calls > 2450 and calls < 4950:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey2)
    elif calls > 4950 and calls < 7450:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey3)
    elif calls > 7450 and calls < 9950:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey4)

    if (url != ''):
        data = urllib.urlopen(url).read()
        info = json.loads(data).get("results")
        if info:
            location = info[0].get("geometry").get("location")
            address_components = info[0].get("address_components")
            for component in address_components:
                if "country" in component["types"]:
                    country = component["short_name"]
                    print country
                    location["country"] = country
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


def saveMap(abv, numPoints, filePrefix):
    if str(abv) in abvMapName:
        abvRange = abvMapName[str(abv)]
    else:
        abvRange += abvMapName['11']

    title = 'Average Beer Ratings of Beer with Alcohol Concentration of ' + \
        abvRange + '%' + '\n' + str(numPoints) + " Reviews Used"
    plt.suptitle(title)

    filename = filePrefix + abvRange + '.png'
    plt.savefig(filename)
    plt.close()


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

    xs, ys, average = createHistogram(m, lats, lngs, ratings, True)

    # overlay the averages histogram over map
    plt.pcolormesh(xs, ys, average)
    plt.colorbar(orientation='horizontal')
    saveMap(abv, len(points), '../graphics/USRating')


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
    xs, ys, average = createHistogram(m, lats, lngs, ratings)
    #####################################################
    # xs, ys, average data will be stored in db as lists. Need to
    # change back to ndarray later
    # xs = numpy.array(xs.tolist())
    # ys = numpy.array(ys.tolist())
    # average = numpy.array(average.tolist())
    #####################################################

    # overlay the averages histogram over map
    plt.pcolormesh(xs, ys, average)
    plt.colorbar(orientation='horizontal')
    saveMap(abv, len(points), '../graphics/EURating')


def inEU(lat, lng):
    return lat >= 27 and lat <= 71 and lng >= -16 and lng <= 45


def inUS(lat, lng):
    return lat >= 22 and lat <= 48 and lng >= -125 and lng <= -59


def createHistogram(m, lats, lngs, ratings, us=False):
    nx, ny = 10, 10
    if us:
        nx, ny = 20, 20
    # compute appropriate bins to histogram the data into
    lng_bins = numpy.linspace(min(lngs), max(lngs), nx + 1)
    lat_bins = numpy.linspace(min(lats), max(lats), ny + 1)

    # Histogram the lats and lons to produce an array of frequencies in each box.
    frequency, _, _ = numpy.histogram2d(lats, lngs, [lat_bins, lng_bins])

    # Histogram the lats and lons to produce an array of frequencies weighted by
    # ratings in each box.
    weighted, _, _ = numpy.histogram2d(lats, lngs, [lat_bins, lng_bins], weights=ratings)

    # divide the weighted bins by the frequency bins to create bins of average
    # beer ratings in each bin
    with numpy.errstate(invalid='ignore'):
        average = numpy.divide(weighted, frequency)
        average = numpy.nan_to_num(average)

    # Turn the lng/lat bins into 2 dimensional arrays ready
    # for conversion into projected coordinates
    lng_bins_2d, lat_bins_2d = numpy.meshgrid(lng_bins, lat_bins)

    # convert the xs and ys to map coordinates
    xs, ys = m(lng_bins_2d, lat_bins_2d)

    return xs, ys, average


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
    drawUSMap(usPoints, abv)
