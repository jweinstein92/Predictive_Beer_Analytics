import argparse
import jsonpickle as jpickle
import os
import operator
import csv
# import cPickle
from time import sleep
import untappd as UT
import PBAMap
import keywordExtractor as extract
import dataPoints as dp
import labels

parser = argparse.ArgumentParser(prog='PBA')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--users', action='store_true',
                   help='Add to the list of users')
group.add_argument('--reviews', action='store_true',
                   help='Add to the list of users, beers, and breweries')
group.add_argument('--normalizeData', action='store_true',
                   help='Alter Untappd data for privacy')
group.add_argument('--keywords', action='store_true',
                   help='Extract keywords from beer descriptions and attach to beer')
group.add_argument('--dataPoints', action='store_true',
                   help='Create list of data points from user locations, ratings, \
                   beer alchol content, and beer style')
group.add_argument('--styles', action='store_true',
                   help='Create csv file of allowable beer styles to make maps with')
group.add_argument('--abvMap', type=float,
                   help='Create map of ratings using data points on maps \
                   provided alcohol level. Data is split into abv ranges: \
                   0, 0.1 - 3.9, 4.0-4.9, 5.0-5.9, 6.0-6.9, 7.0-7.9, 8.0-8.9, \
                   9.0-9.9, 10.0-10.9, 11.0+ Requires GEOS Library and \
                   mpl_toolkits.basemap')
group.add_argument('--styleMap', type=str,
                   help='Create map of ratings using data points on maps \
                   provided beer style. Styles limited to 20 most common \
                   types of beer - \
                   Requires GEOS Library and \
                   mpl_toolkits.basemap')
group.add_argument('--colorPalette', action='store_true',
                   help='Download label images, clusterize colors, \
                   generate global color rating palette of N colors.')
args = parser.parse_args()

# set the api settings and create an Untappd object
untappd = UT.Untappd()
untappd.settings('../apiConfig.ini')


def readUsers():
    """
    Load already processed users UntappdUser
    """
    try:
        usersFile = open('../data/users.json', 'rb')
    except IOError:
        usersFile = open('../data/users.json', 'wb')

    try:
        f = usersFile.read()
        usersList = jpickle.decode(f)
    except:
        usersList = {}
    usersFile.close()
    return usersList


def readBeers():
    """
    Load already processed beers UntappdBeer
    """
    try:
        beersFile = open('../data/beers.json', 'rb')
    except IOError:
        beersFile = open('../data/beers.json', 'wb')

    try:
        f = beersFile.read()
        beersList = jpickle.decode(f)
    except:
        beersList = {}
    beersFile.close()
    return beersList


def readBreweries():
    """
    Load already processed breweries UntappdBrewery
    """
    try:
        breweriesFile = open('../data/breweries.json', 'rb')
    except IOError:
        breweriesFile = open('../data/breweries.json', 'wb')

    try:
        f = breweriesFile.read()
        breweryList = jpickle.decode(f)
    except:
        breweryList = {}
    breweriesFile.close()
    return breweryList


def readBreweryToBeers():
    """
    Load already processed breweries dictionary
    """
    try:
        breweryToBeersFile = open('../data/breweryToBeers.json', 'rb')
    except IOError:
        breweryToBeersFile = open('../data/breweryToBeers.json', 'wb')

    try:
        f = breweryToBeersFile.read()
        breweryToBeers = jpickle.decode(f)
    except:
        breweryToBeers = {}
    breweryToBeersFile.close()
    return breweryToBeers


def readDataPoints():
    """
    Load dataPoints
    """
    try:
        dataPointsFile = open('../data/dataPoints.json', 'rb')
    except IOError:
        dataPointsFile = open('../data/dataPoints.json', 'wb')

    try:
        f = dataPointsFile.read()
        dataPoints = jpickle.decode(f).points
    except:
        dataPoints = []
    dataPointsFile.close()

    return dataPoints


def readBeerStyles():
    """
    Load most rated beer styles
    """
    styles = []
    with open('../data/styles.csv') as stylesFile:
        reader = csv.DictReader(stylesFile)
        for row in reader:
            if row['style'] not in styles:
                styles.append(row['style'])
    return styles


def writeJSONFile(path, data):
    """
    Write JSON file
    """
    with open(path, 'wb') as jsonFile:
        json = jpickle.encode(data)
        jsonFile.write(json)


def readBeerColors():
    """
    Load the dominant label colors.
    """
    try:
        beerColorsFile = open('../data/beerColors.json', 'rb')
    except IOError:
        beerColorsFile = open('../data/beerColors.json', 'wb')

    try:
        f = beerColorsFile.read()
        beerColorsDict = jpickle.decode(f)
    except:
        beerColorsDict = labels.BeerColorsDict()
    beerColorsFile.close()
    return beerColorsDict


def usersList():
    """
    Parses through data from /thepub to get unique usernames, user ids,
    and locations. Stores this information in a csv file to be used in later api
    requests. Limited to 100 api calls per hour requiring sleep method.
    May be run multiple times to retrieve Continuously run until user stops script
    """

    usersList = readUsers()
    apiCount = 0
    userNameCountAdditions = 0
    while (True):
        # get 25 most recent updates
        data = untappd.getPubFeed()
        apiCount += 1
        print 'apiCount: ' + str(apiCount)
        checkins = data['response']['checkins']['items']
        # each response has 25 items, each with a username
        for checkin in checkins:
            userId = checkin['user']['uid']
            username = checkin['user']['user_name']
            userLocation = checkin['user']['location']
            if hash(str(userId)) not in usersList:
                if userLocation != '':
                    userNameCountAdditions += 1
                    userAttribs = {'uid': str(userId), 'username': username,
                                   'location': {'name': unicode(userLocation).encode("utf-8")}, 'ratings': {}}
                    user = UT.UntappdUser(userAttribs)
                    usersList[hash(str(userId))] = user
        writeJSONFile('../data/users.json', usersList)
        userCount = len(usersList)
        print 'Total Users: ' + str(userCount)
        # Untappd only allows 100 api requests per hour. Sleep for 38
        # seconds between requests
        sleep(37)


def userReviews():
    """
    Parses through user reviews /user/beers/{username}
    Retrieves at most 50 reviews per user, retains review, beer, and
    brewery information. After querying the api, remove username to
    lessen privacy concerns with untappd data
    """
    usersList = readUsers()
    beersList = readBeers()
    breweryList = readBreweries()
    breweryToBeers = readBreweryToBeers()

    total = 0
    totalUsersComplete = 0
    for userHash, user in usersList.iteritems():
        totalUsersComplete += 1
        # if the data has been normalized, old data will not
        # have usernames. Ignore older users which may have
        # already gotten reviews
        if user.username:
            userId = user.uid
            username = user.username
            user.username = None
            userReviewCount = 0
            offsetTotal = 0
            ratings = {}

            print 'Processing ' + str(userId) + ': ' + username
            # each response returns at most 25 reviews. To get more user
            # reviews, call again with an offset get at most 50 reviews
            # from the same user
            while (userReviewCount < 2):
                print username + ': ' + str(userReviewCount + 1)
                data = untappd.getUserReviewData(username, offsetTotal)
                offset = data['response']['beers']['count']
                offsetTotal += offset
                reviews = data['response']['beers']['items']
                for review in reviews:
                    userRating = review['rating_score']
                    if userRating > 0:
                        beerInfo = review['beer']
                        breweryInfo = review['brewery']
                        # fill in beer information
                        if hash(str(beerInfo['bid'])) not in beersList:
                            stylesList = []
                            style = unicode(beerInfo['beer_style']).encode("utf-8")
                            styles = style.lower().title().split('/')
                            for style in styles:
                                style = style.strip()
                                stylesList.append(style)
                            beerAttribs = {
                                'bid': str(beerInfo['bid']),
                                'name': unicode(beerInfo['beer_name']).encode("utf-8"),
                                'label': beerInfo['beer_label'],
                                'abv': beerInfo['beer_abv'],
                                'ibu': beerInfo['beer_ibu'],
                                'style': stylesList,
                                'description': unicode(beerInfo['beer_description']).encode("utf-8"),
                                'rating': beerInfo['rating_score'],
                                'numRatings': 1,
                                'brewery': str(breweryInfo['brewery_id'])
                            }
                            beer = UT.UntappdBeer(beerAttribs)
                            beersList[hash(beer.bid)] = beer
                        else:
                            beersList[hash(str(beerInfo['bid']))].numRatings += 1
                        # fill in brewery information
                        if hash(str(breweryInfo['brewery_id'])) not in breweryList:
                            breweryAttribs = {
                                'breweryId': str(breweryInfo['brewery_id']),
                                'name': unicode(breweryInfo['brewery_name']).encode("utf-8"),
                                'label': breweryInfo['brewery_label'],
                                'country': unicode(breweryInfo['country_name']).encode("utf-8"),
                                'location': unicode(breweryInfo['location']).encode("utf-8")
                            }
                            brewery = UT.UntappdBrewery(breweryAttribs)
                            breweryList[hash(brewery.breweryId)] = brewery

                        # map breweery_id to a list of beers produced there
                        if hash(str(breweryInfo['brewery_id'])) not in breweryToBeers:
                            # store the current beer in a list of beers of
                            # the brewery
                            breweryToBeers[hash(str(breweryInfo['brewery_id']))] = {str(breweryInfo['brewery_id']): [str(beerInfo['bid'])]}
                        else:
                            # add current beer to brewery's list of beers
                            breweryToBeers[hash(str(breweryInfo['brewery_id']))][str(breweryInfo['brewery_id'])].append(str(beerInfo['bid']))

                        # add list of beer ratings to user
                        ratings[str(beerInfo['bid'])] = userRating
                userReviewCount += 1
                user.ratings = ratings

                # store the dictionaries after new data so user doesn't kill process before writing
                # with open('../data/users.json', 'wb') as usersFile:
                #     json = jpickle.encode(usersList)
                #     usersFile.write(json)
                # with open('../data/beers.json', 'wb') as beersFile:
                #     json = jpickle.encode(beersList)
                #     beersFile.write(json)
                # with open('../data/breweries.json', 'wb') as breweriesFile:
                #     json = jpickle.encode(breweryList)
                #     breweriesFile.write(json)
                # with open('../data/breweryToBeers.json', 'wb') as breweryToBeersFile:
                #     json = jpickle.encode(breweryToBeers)
                #     breweryToBeersFile.write(json)

                # if the offset is less than 25, then there are no more reviews to retrieve
                if offset < 25:
                    break
            writeJSONFile('../data/users.json', usersList)
            writeJSONFile('../data/beers.json', beersList)
            writeJSONFile('../data/breweries.json', breweryList)
            writeJSONFile('../data/breweryToBeers.json', breweryToBeers)

            total += len(ratings)
            print str(userId) + ': ' + username + ', Processed: ' + str(len(ratings)) + ' reviews'
            print 'Total Reviews: ' + str(total)
            print 'Total Users Completed: ' + str(totalUsersComplete)
            sleep(37 * (userReviewCount))
        else:
            total += len(user.ratings)


def normalizeUsers():
    """
    Change the user ids so the information can be made public and
    use the googlemaps module to determine the user's location
    """
    usersList = readUsers()
    newUsersList = {}

    i = 1
    newUid = 1
    for hashId, user in usersList.iteritems():
        uid = user.uid
        user.uid = str(newUid)
        location = user.location
        if location['name'] != "" and 'lat' not in location:
            if isinstance(location['name'], unicode):
                location = location['name'].encode('utf-8')
            else:
                location = location['name']

            mapInfo = PBAMap.getLatLong(location, i)
            i += 1
            if mapInfo == 'apiLimit':
                print str(i) + " At daily API limit. Update script and repeat tomorrow"
            elif mapInfo != '':
                user.location = {
                    'name': location,
                    'lat': mapInfo['lat'],
                    'lng': mapInfo['lng'],
                }
                if 'country' in mapInfo:
                    user.location['country'] = mapInfo['country']
                print str(i), user.location
            else:
                print str(i), "checked: none"
                user.location = {'name': ''}
        newUid += 1
        newUsersList[hash(str(uid))] = user

    writeJSONFile('../data/users.json', newUsersList)
    print "User ids, usernames, and locations updated\n"


def beerKeywords():
    beersList = readBeers()
    print 'beers.json LOADED...'

    # List of keywords generation
    keywordsList = {}
    position = 0

    for hashId, beer in beersList.iteritems():
        beer.keywords = []
        beer.keywords = extract.extractKeywords(beer.description)
        for keyword in beer.keywords:
            if keyword in keywordsList:
                keywordsList[keyword][0] += beer.rating
                keywordsList[keyword][1] += 1
            else:
                keywordsList[keyword] = [beer.rating, 1]
        position += 1
        if (position % 100) == 0:
            print 'Processed ' + str(position) + '/' + str(len(beersList)) + ' beers.'

    writeJSONFile('../data/beers.json', beersList)
    writeJSONFile('../data/keywords.json', keywordsList)


def createDataPoints():
    usersList = readUsers()
    beersList = readBeers()
    points = []
    i = 1
    for hashId, user in usersList.iteritems():
        if 'lat' in user.location and user.ratings:
            for bid, rating in user.ratings.iteritems():
                country = None
                if 'country' in user.location:
                    country = user.location['country']
                pointAttribs = {'lat': user.location['lat'], 'lng': user.location['lng'],
                'country': country, 'abv': beersList[str(hash(bid))].abv, 'rating': rating,
                'style': beersList[str(hash(bid))].style}
                point = dp.dataPoint(pointAttribs)
                points.append(point)
                if i % 1000 == 0:
                    print "Points added: " + str(i)
                i += 1
    data = dp.dataPoints(points)
    writeJSONFile('../data/dataPoints.json', data)


def createABVMap():
    print "Drawing user rating maps of beers with an alcohol concentration of " + str(args.abvMap) + '%'
    dataPoints = readDataPoints()
    if len(dataPoints) > 0:
        abv = int(args.abvMap)
        points = []
        for point in dataPoints:
            if int(point.abv) == abv:
                points.append(point)
            elif (abv in [1, 2, 3]) and (int(point.abv) in [1, 2, 3]):
                points.append(point)
            elif (abv > 11 and int(point.abv) > 11):
                points.append(point)
        print str(len(points)) + " points of data"
        PBAMap.drawMap(points, abv)
    else:
        print "No data points found"


def createStyleMap():
    print "Drawing user rating maps of beers with a style of " + str(args.styleMap)
    dataPoints = readDataPoints()
    if len(dataPoints) > 0:
        style = args.styleMap
        points = []
        for point in dataPoints:
            if style in point.style:
                points.append(point)
        print str(len(points)) + " points of data"
        PBAMap.drawMap(points, style)
    else:
        print "No data points found"


def createCommonStyles():
    beersList = readBeers()
    allStyles = {}
    for hashId, beer in beersList.iteritems():
        styles = beer.style
        for style in styles:
            numRatings = beer.numRatings if (hasattr(beer, 'numRatings')) else 0
            if style in allStyles:
                allStyles[style] += numRatings
            else:
                allStyles[style] = numRatings

    sorted_styles = sorted(allStyles.items(), key=operator.itemgetter(1))[-20:]
    with open('../data/styles.csv', 'wb') as stylesCSV:
        csvwriter = csv.writer(stylesCSV, delimiter=',',
                            quotechar='"')
        csvwriter.writerow(["id", "style", "numRatings"])
        i = 1
        for style in sorted_styles:
            csvwriter.writerow([i, unicode(style[0]).encode("utf-8"), style[1]])
            i += 1


def processLabels():
    """
    Download beer bottle labels, extract n dominant colors,
    make the color palette, flag each color and calculate
    average rating of that color.
    """

    beersList = readBeers()
    # beersList = {}
    beerColorsDict = readBeerColors()

    # Path for saving the images
    path = "../data/labels/"

    fileList = os.listdir(path)
    fileList = [item for item in fileList
                if item.split(".")[-1] in ('jpeg', 'jpg', 'png')]

    # Download and save images
    # labels.download(beersList, path, fileList)

    # Number of label colors to cluster
    nColors = 5
    i = 0
    stop = 6  # Then use the whole list.

    # Loop over images in the folder
    for file in fileList[0:stop]:
        i += 1
        bid = unicode(file.split('.')[0])
        if (bid in beerColorsDict and
                len(beerColorsDict[bid].colorPaletteFlags) == nColors):
            continue

        print ("Processing image " + file +
               " [" + str(i - 1) + "/" + str(stop) + "]")
        beerLabel = labels.Image(path + file)

        beerLabel.preprocess()
        beerColor = beerLabel.clusterize(nColors)
        beerColorsDict[bid] = beerColor

        # Only for presentation
        beerLabel.quantizeImage()
        beerLabel.showResults()

    # Generate the color palette with ratings - Classification
    colorPalette = labels.ColorPalette()
    colorPalette.build(beerColorsDict, beersList)

    # Write the colorsFile - dict{ 'bid': beerColor{RGB,intensity}}
    with open('../data/beerColors.json', 'wb') as beerColorsFile:
        string = jpickle.encode(beerColorsDict)
        beerColorsFile.write(string)

    with open('../data/colorPalette.json', 'wb') as colorPaletteFile:
        json = jpickle.encode(colorPalette.palette)
        colorPaletteFile.write(json)

    print 'Color palette saved.'

if args.users:
    usersList()
elif args.reviews:
    userReviews()
elif args.normalizeData:
    normalizeUsers()
elif args.keywords:
    beerKeywords()
elif args.styles:
    createCommonStyles()
elif args.colorPalette:
    processLabels()
elif args.dataPoints:
    createDataPoints()
elif args.abvMap >= 0:
    createABVMap()
elif args.styleMap:
    if args.styleMap in readBeerStyles():
        createStyleMap()
    else:
        print "No support for style: " + args.styleMap
