import untappd as UT
import PBAMap
import argparse
import jsonpickle as jpickle
import cPickle
import csv
from time import sleep

parser = argparse.ArgumentParser(prog='PBA')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--users', action='store_true',
                   help='Add to the list of users. Filename required')
group.add_argument('--reviews', action='store_true',
                   help='Add to the list of users, beers, and breweries')
group.add_argument('--normalizeData', action='store_true',
                   help='Alter Untappd data for privacy.')
# group.add_argument('--dataUpload', action='store_true',
#                    help='Upload data to database. Requires database configuration filename')
args = parser.parse_args()

# set the api settings and create an Untappd object
untappd = UT.Untappd()
untappd.settings('apiSettings.csv')

# set the db configuration and create an Analytics object
# analytics = UT.Analytics()
# analytics.config('dbConfig.csv')


def readUsers():
    # load already processed users UntappdUser
    try:
        usersFile = open('users.json', 'rb')
    except IOError:
        usersFile = open('users.json', 'wb')

    try:
        f = usersFile.read()
        usersList = jpickle.decode(f)
    except:
        usersList = {}
    usersFile.close()
    return usersList


def readBeers():
    # load already processed beers UntappdBeer
    try:
        beersFile = open('beers.json', 'rb')
    except IOError:
        beersFile = open('beers.json', 'wb')

    try:
        f = beersFile.read()
        beersList = jpickle.decode(f)
    except:
        beersList = {}
    beersFile.close()
    return beersList


def readBreweries():
    # load already processed breweries UntappdBrewery
    try:
        breweriesFile = open('breweries.json', 'rb')
    except IOError:
        breweriesFile = open('breweries.json', 'wb')

    try:
        f = breweriesFile.read()
        breweryList = jpickle.decode(f)
    except:
        breweryList = {}
    breweriesFile.close()
    return breweryList


def readBreweryToBeers():
    # load already processed breweries dictionary
    try:
        breweryToBeersFile = open('breweryToBeers.json', 'rb')
    except IOError:
        breweryToBeersFile = open('breweryToBeers.json', 'wb')

    try:
        f = breweryToBeersFile.read()
        breweryToBeers = jpickle.decode(f)
    except:
        breweryToBeers = {}
    breweryToBeersFile.close()
    return breweryToBeers


def usersList():
    """
    Parses through data from /thepub to get unique usernames and user
    ids. Stores this information in a csv file to be used in later api
    requests. Continuously run until user stops script
    """
    usernames = dict()
    with open('userInfo.csv', 'a+') as usernameFile:
        reader = csv.reader(usernameFile)
        # read the previously written usernames so there are no duplicates
        # if script run multiple times
        for row in reader:
            uid = row[0]
            usernames[uid] = row[1]

    apiCount = 0
    userNameCountAdditions = 0

    with open('userInfo.csv', 'ab') as usernameFile:
        writer = csv.writer(usernameFile)
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
                if str(userId) not in usernames:
                    userNameCountAdditions += 1
                    writer.writerow((userId, username,
                                    unicode(userLocation).encode("utf-8")))
                    usernames[str(userId)] = username
            # Untappd only allows 100 api requests per hour. Sleep for 38
            # seconds between requests
            sleep(38)


def userReviews():
    usersList = readUsers()
    beersList = readBeers()
    breweryList = readBreweries()
    breweryToBeers = readBreweryToBeers()

    lastLineNum = 0

    # keep track how many users have already been processed
    try:
        with open('last_line.txt', 'rb') as lastFile:
            lastLineNum = int(lastFile.read())
    except:
        pass

    total = 0
    with open('userInfo.csv', 'rb') as userNameFile:
        reader = csv.reader(userNameFile)
        for i, line in enumerate(reader):
            userReviewCount = 0
            if i <= lastLineNum:
                continue
            userId = line[0]
            username = line[1]
            location = line[2]
            if (location != ''):
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
                            if str(beerInfo['bid']) not in beersList:
                                beerAttribs = {
                                    'bid': str(beerInfo['bid']),
                                    'name': unicode(beerInfo['beer_name']).encode("utf-8"),
                                    'label': beerInfo['beer_label'],
                                    'abv': beerInfo['beer_abv'],
                                    'ibu': beerInfo['beer_ibu'],
                                    'style': unicode(beerInfo['beer_style']).encode("utf-8"),
                                    'description': unicode(beerInfo['beer_description']).encode("utf-8"),
                                    'rating': beerInfo['rating_score'],
                                    'brewery': str(breweryInfo['brewery_id'])
                                }
                                beer = UT.UntappdBeer(beerAttribs)
                                beersList[str(beer.bid)] = beer

                            # fill in brewery information
                            if str(breweryInfo['brewery_id']) not in breweryList:
                                breweryAttribs = {
                                    'breweryId': str(breweryInfo['brewery_id']),
                                    'name': unicode(breweryInfo['brewery_name']).encode("utf-8"),
                                    'label': breweryInfo['brewery_label'],
                                    'country': unicode(breweryInfo['country_name']).encode("utf-8"),
                                    'location': unicode(breweryInfo['location']).encode("utf-8")
                                }
                                brewery = UT.UntappdBrewery(breweryAttribs)
                                breweryList[str(brewery.breweryId)] = brewery

                            # map breweery_id to a list of beers produced there
                            if breweryInfo['brewery_id'] not in breweryToBeers:
                                # store the current beer in a list of beers of
                                # the brewery
                                breweryToBeers[breweryInfo['brewery_id']] = [str(beerInfo['bid'])]
                            else:
                                # add current beer to brewery's list of beers
                                breweryToBeers[breweryInfo['brewery_id']].append(str(beerInfo['bid']))

                            # add list of beer ratings to user
                            ratings[str(beerInfo['bid'])] = userRating
                    userReviewCount += 1

                    userAttribs = {'uid': str(userId), 'username': username,
                        'location': location, 'ratings': ratings}
                    user = UT.UntappdUser(userAttribs)
                    usersList[user.uid] = user

                    # store the dictionaries
                    with open('users.json', 'wb') as usersFile:
                        json = jpickle.encode(usersList)
                        usersFile.write(json)
                    with open('beers.json', 'wb') as beersFile:
                        json = jpickle.encode(beersList)
                        beersFile.write(json)
                    with open('breweries.json', 'wb') as breweriesFile:
                        json = jpickle.encode(breweryList)
                        breweriesFile.write(json)
                    with open('breweryToBeers.json', 'wb') as breweryToBeersFile:
                        json = jpickle.encode(breweryToBeers)
                        breweryToBeersFile.write(json)

                    # if the offset is less than 25, then there are no more reviews to retrieve
                    if offset < 25:
                        break
                total += len(ratings)
                with open('last_line.txt', 'wb') as lastFile:
                    lastFile.write(str(i))
                print str(userId) + ': ' + username + ', Processed: ' + str(len(ratings)) + ' reviews'
                print 'Total: ' + str(total)
                sleep(38 * (userReviewCount))


def normalizeUsers():
    """
    Change the user ids and usernames so the information can be made public
    """
    usersList = readUsers()
    newUsersList = {}

    i = 1
    for uid, user in usersList.iteritems():
        user.uid = str(i)
        user.username = None
        location = user.location
        if location != "":
            if isinstance(location, unicode):
                location = location.encode('utf-8')
            mapInfo = PBAMap.getLatLong(location, i)
            if mapInfo != "":
                print str(i), location
                user.location = {
                    'name': location,
                    'lat': mapInfo['lat'],
                    'lng': mapInfo['lng']
                }
            else:
                print str(i), "none"
                user.location = ""
        else:
            print str(i), "none"
        newUsersList[str(i)] = user
        i += 1

    with open('users.json', 'wb') as usersFile:
        json = jpickle.encode(newUsersList)
        usersFile.write(json)
    usersFile.close()
    print "User ids, usernames, and locations updated\n"


def normalizeBeersAndBreweries():
    """
    Change the beer and brewery ids so the information can be made public
    """
    usersList = readUsers()
    beersList = readBeers()
    breweryList = readBreweries()

    newBeerId = 1
    newBreweryId = 1
    # create new lists and maps to prevent any id collisions
    beerIdMap = {}
    breweryIdMap = {}
    newBeerList = {}
    newBreweryList = {}
    newBreweryToBeers = {}
    for bid, beer in beersList.iteritems():
        breweryId = beer.brewery
        beerIdMap[bid] = newBeerId
        if breweryId not in breweryIdMap:
            breweryIdMap[breweryId] = newBreweryId
            brewery = cPickle.loads(cPickle.dumps(breweryList[breweryId], -1))
            brewery.breweryId = newBreweryId
            newBreweryList[newBreweryId] = brewery

            newBreweryToBeers[newBreweryId] = [newBeerId]
            newBreweryId += 1
        else:
            newBreweryToBeers[breweryIdMap[breweryId]].append(newBeerId)

        beer.bid = newBeerId
        beer.brewery = breweryIdMap[breweryId]
        newBeerList[beer.bid] = beer

        newBeerId += 1

    for uid, user in usersList.iteritems():
        ratings = user.ratings
        for bid in ratings.keys():
            if bid in beerIdMap:
                ratings[beerIdMap[bid]] = ratings.pop(bid)
            else:
                ratings.pop(bid)
        user.ratings = ratings

    # store the dictionaries
    with open('users.json', 'wb') as usersFile:
        json = jpickle.encode(usersList)
        usersFile.write(json)
    with open('beers.json', 'wb') as beersFile:
        json = jpickle.encode(newBeerList)
        beersFile.write(json)
    with open('breweries.json', 'wb') as breweriesFile:
        json = jpickle.encode(newBreweryList)
        breweriesFile.write(json)
    with open('breweryToBeers.json', 'wb') as breweryToBeersFile:
        json = jpickle.encode(newBreweryToBeers)
        breweryToBeersFile.write(json)

    print "Beer ids updated\n"


# def dataUpload():
#     db = UT.DatabaseObject()
#     db.config('dbConfig.csv')
#     db.dataToDatabase('foo')

if args.users:
    usersList()
elif args.reviews:
    userReviews()
elif args.normalizeData:
    normalizeUsers()
    normalizeBeersAndBreweries()
    

# elif args.dataUpload:
#     dataUpload()
