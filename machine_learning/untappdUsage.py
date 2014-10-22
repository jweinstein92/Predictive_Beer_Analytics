import predictiveBeerAnalytics as PBA
import argparse
import jsonpickle as jpickle
import csv
from time import sleep

parser = argparse.ArgumentParser(prog='PBA')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--users', action='store_true',
                   help='Add to the list of users. Filename required')
group.add_argument('--reviews', action='store_true',
                   help='Add to the list of users, beers, and breweries')
group.add_argument('--normalizeUsers', action='store_true',
                   help='Alter user ids and remove usernames for privacy')
# group.add_argument('--dataUpload', action='store_true',
#                    help='Upload data to database. Requires database configuration filename')
args = parser.parse_args()

# set the api settings and create an Untappd object
untappd = PBA.Untappd()
untappd.settings('apiSettings.csv')

# set the db configuration and create an Analytics object
# analytics = PBA.Analytics()
# analytics.config('dbConfig.csv')


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
    # load already processed users UntappdUser
    try:
        usersFile = open('users.json', 'rb')
    except IOError:
        usersFile = open('users.json', 'wb')

    try:
        f = usersFile.read()
        usersList = jpickle.decode(f)
    except:
        usersList = []
    usersFile.close()

    # load already processed beers UntappdBeer
    try:
        beersFile = open('beers.json', 'rb')
    except IOError:
        beersFile = open('beers.json', 'wb')

    try:
        f = beersFile.read()
        beersList = jpickle.decode(f)
    except:
        beersList = []
    beersFile.close()

    try:
        beerIdsFile = open('beerIds.json', 'rb')
    except IOError:
        beerIdsFile = open('beerIds.json', 'wb')

    try:
        f = beerIdsFile.read()
        beerIds = jpickle.decode(f)
    except:
        beerIds = dict()
    beersFile.close()

    # load already processed breweries UntappdBrewery
    try:
        breweriesFile = open('breweries.json', 'rb')
    except IOError:
        breweriesFile = open('breweries.json', 'wb')

    try:
        f = breweriesFile.read()
        breweryList = jpickle.decode(f)
    except:
        breweryList = []
    breweriesFile.close()

    try:
        breweryIdsFile = open('breweryIds.json', 'rb')
    except IOError:
        breweryIdsFile = open('breweryIds.json', 'wb')

    try:
        f = breweryIdsFile.read()
        breweryIds = jpickle.decode(f)
    except:
        breweryIds = dict()
    breweriesFile.close()

    # load already processed breweries dictionary
    try:
        breweryToBeersFile = open('breweryToBeers.json', 'rb')
    except IOError:
        breweryToBeersFile = open('breweryToBeers.json', 'wb')

    try:
        f = breweryToBeersFile.read()
        breweryToBeers = jpickle.decode(f)
    except:
        breweryToBeers = dict()
    breweryToBeersFile.close()

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
                ratings = []

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
                            if beerInfo['bid'] not in beerIds:
                                beerAttribs = {
                                    'name': unicode(beerInfo['beer_name']).encode("utf-8"),
                                    'label': beerInfo['beer_label'],
                                    'abv': beerInfo['beer_abv'],
                                    'ibu': beerInfo['beer_ibu'],
                                    'style': unicode(beerInfo['beer_style']).encode("utf-8"),
                                    'description': unicode(beerInfo['beer_description']).encode("utf-8"),
                                    'rating': beerInfo['rating_score'],
                                    'brewery': breweryInfo['brewery_id']
                                }
                                beer = PBA.UntappdBeer(beerAttribs)
                                beersList.append(beer)
                                beerIds[beerInfo['bid']] = True

                            # fill in brewery information
                            if breweryInfo['brewery_id'] not in breweryIds:
                                breweryAttribs = {
                                    'name': unicode(breweryInfo['brewery_name']).encode("utf-8"),
                                    'label': breweryInfo['brewery_label'],
                                    'country': unicode(breweryInfo['country_name']).encode("utf-8"),
                                    'location': unicode(breweryInfo['location']).encode("utf-8")
                                }
                                brewery = PBA.UntappdBrewery(breweryAttribs)
                                breweryList.append(brewery)
                                breweryIds[breweryInfo['brewery_id']] = True

                            # map breweery_id to a list of beers produced there
                            if breweryInfo['brewery_id'] not in breweryToBeers:
                                # store the current beer in a list of beers of
                                # the brewery
                                breweryToBeers[breweryInfo['brewery_id']] = [beerInfo['bid']]
                            else:
                                # add current beer to brewery's list of beers
                                breweryToBeers[breweryInfo['brewery_id']].append(beerInfo['bid'])

                            # add list of beer ratings to user
                            ratings.append({beerInfo['bid']: userRating})
                    userReviewCount += 1

                    userAttribs = {'uid': userId, 'username': username,
                        'location': location, 'ratings': ratings}
                    user = PBA.UntappdUser(userAttribs)
                    usersList.append(user)

                    # store the dictionaries
                    with open('users.json', 'wb') as usersFile:
                        json = jpickle.encode(usersList)
                        usersFile.write(json)
                    with open('beers.json', 'wb') as beersFile:
                        json = jpickle.encode(beersList)
                        beersFile.write(json)
                    with open('beerIds.json', 'wb') as beerIdsFile:
                        json = jpickle.encode(beerIds)
                        beerIdsFile.write(json)
                    with open('breweries.json', 'wb') as breweriesFile:
                        json = jpickle.encode(breweryList)
                        breweriesFile.write(json)
                    with open('breweryIds.json', 'wb') as breweryIdsFile:
                        json = jpickle.encode(breweryIds)
                        breweryIdsFile.write(json)
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


# def dataUpload():
#     db = PBA.DatabaseObject()
#     db.config('dbConfig.csv')
#     db.dataToDatabase('foo')

if args.users:
    usersList()
elif args.reviews:
    userReviews()
elif args.normalizeUsers:
    try:
        usersFile = open('users.json', 'rb')
    except IOError:
        usersFile = open('users.json', 'wb')
    try:
        f = usersFile.read()
        usersList = jpickle.decode(f)
    except:
        usersList = []
    print usersList
    users = PBA.normalizeUsers(usersList)
    with open('users.json', 'wb') as usersFile:
        json = jpickle.encode(users)
        usersFile.write(json)
    usersFile.close()

# elif args.dataUpload:
#     dataUpload()
