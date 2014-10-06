import untappd as UT
import argparse
import requests
import json
import csv
from time import sleep

parser = argparse.ArgumentParser(prog='PBA')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--users', action='store_true',
                   help='Add to the list of users. Filename required')
group.add_argument('--userReviews', action='store_true',
                   help='Add to the list of users, beers, and breweries')
args = parser.parse_args()

untappd = UT.Untappd()
untappd.settings('apiSettings.csv')


def usersList():
    """
    Parses through data from /thepub to get unique usernames and user
    ids. Stores this information in a csv file to be used in later api
    requests. Continuously run until user stops script
    """
    usernames = dict()
    with open('foo.csv', 'a+') as usernameFile:
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
    print 'bar'


if args.users:
    usersList()
elif args.userReviews:
    userReviews()
